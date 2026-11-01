import unittest
from PIL import Image
from stego import encode_message, decode_message, SteganographyError


class SteganographyTests(unittest.TestCase):
    def setUp(self):
        self.image = Image.new("RGB", (400, 400), color=(120, 160, 200))

    def test_encode_and_decode(self):
        encoded = encode_message(self.image, "Hello, hidden world!", "correct horse")
        self.assertEqual(
            decode_message(encoded, "correct horse"),
            "Hello, hidden world!",
        )

    def test_wrong_password(self):
        encoded = encode_message(self.image, "Secret", "right-password")
        with self.assertRaises(SteganographyError):
            decode_message(encoded, "wrong-password")

    def test_image_without_message(self):
        with self.assertRaises(SteganographyError):
            decode_message(self.image, "password")


if __name__ == "__main__":
    unittest.main()
