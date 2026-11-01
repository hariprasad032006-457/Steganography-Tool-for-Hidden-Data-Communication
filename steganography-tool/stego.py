from PIL import Image
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import struct

MAGIC = b"STEGv1!!"          # Identifies images created by this application
SALT_LENGTH = 16
HEADER_LENGTH = len(MAGIC) + 4
BITS_PER_CHANNEL = 1
PBKDF2_ITERATIONS = 600_000


class SteganographyError(Exception):
    """Raised when a message cannot be embedded or extracted."""


def _derive_key(password: str, salt: bytes) -> bytes:
    if not password:
        raise SteganographyError("A password is required.")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def _bytes_to_bits(data: bytes):
    for byte in data:
        for shift in range(7, -1, -1):
            yield (byte >> shift) & 1


def _bits_to_bytes(bits):
    output = bytearray()
    current = 0
    count = 0
    for bit in bits:
        current = (current << 1) | bit
        count += 1
        if count == 8:
            output.append(current)
            current = 0
            count = 0
    if count:
        raise SteganographyError("The hidden data is incomplete.")
    return bytes(output)


def _embed_bytes(image: Image.Image, data: bytes) -> Image.Image:
    rgb = image.convert("RGB")
    pixels = bytearray(rgb.tobytes())
    required_bits = len(data) * 8
    if required_bits > len(pixels):
        max_bytes = len(pixels) // 8
        raise SteganographyError(
            f"Message is too large for this image. Approximate maximum payload: {max_bytes} bytes."
        )

    for index, bit in enumerate(_bytes_to_bits(data)):
        pixels[index] = (pixels[index] & 0xFE) | bit

    result = Image.frombytes("RGB", rgb.size, bytes(pixels))
    return result


def _read_bytes(image: Image.Image, byte_count: int) -> bytes:
    rgb = image.convert("RGB")
    pixels = rgb.tobytes()
    required_bits = byte_count * 8
    if required_bits > len(pixels):
        raise SteganographyError("This image is too small or does not contain a valid message.")
    bits = (pixels[index] & 1 for index in range(required_bits))
    return _bits_to_bytes(bits)


def encode_message(image: Image.Image, message: str, password: str) -> Image.Image:
    """Encrypt a text message and hide it in an RGB image."""
    if not message:
        raise SteganographyError("The message cannot be empty.")

    import os
    salt = os.urandom(SALT_LENGTH)
    key = _derive_key(password, salt)
    encrypted = Fernet(key).encrypt(message.encode("utf-8"))
    payload = salt + encrypted

    header = MAGIC + struct.pack(">I", len(payload))
    return _embed_bytes(image, header + payload)


def decode_message(image: Image.Image, password: str) -> str:
    """Read, validate, and decrypt a hidden message."""
    header = _read_bytes(image, HEADER_LENGTH)
    if header[:len(MAGIC)] != MAGIC:
        raise SteganographyError("No message from this application was found in the image.")

    payload_length = struct.unpack(">I", header[len(MAGIC):])[0]
    if payload_length < SALT_LENGTH + 1:
        raise SteganographyError("The hidden data header is invalid.")

    payload = _read_bytes(image, HEADER_LENGTH + payload_length)[HEADER_LENGTH:]
    salt = payload[:SALT_LENGTH]
    encrypted = payload[SALT_LENGTH:]

    try:
        key = _derive_key(password, salt)
        decrypted = Fernet(key).decrypt(encrypted)
        return decrypted.decode("utf-8")
    except (InvalidToken, UnicodeDecodeError):
        raise SteganographyError("Incorrect password or the hidden message is damaged.") from None
