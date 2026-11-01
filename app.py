import io
import streamlit as st
from PIL import Image
from stego import encode_message, decode_message, SteganographyError

st.set_page_config(page_title="Steganography Tool", page_icon="🔐", layout="centered")

st.title("🔐 Steganography Tool")
st.caption("Hide encrypted text messages inside images using LSB steganography.")

encode_tab, decode_tab, about_tab = st.tabs(["Hide a message", "Extract a message", "About"])

with encode_tab:
    st.subheader("Encode a secret message")
    cover_file = st.file_uploader("Choose a cover image", type=["png", "jpg", "jpeg"], key="encode_image")
    message = st.text_area("Secret message", placeholder="Type the message you want to hide...")
    password = st.text_input("Create a password", type="password", key="encode_password")
    confirm = st.text_input("Confirm password", type="password")
    if cover_file is not None:
        try:
            cover = Image.open(cover_file)
            st.image(cover, caption="Selected cover image", use_container_width=True)
            if st.button("Hide message", type="primary"):
                if not message.strip():
                    st.error("Please enter a message.")
                elif not password:
                    st.error("Please enter a password.")
                elif password != confirm:
                    st.error("The passwords do not match.")
                else:
                    output = encode_message(cover, message, password)
                    buffer = io.BytesIO()
                    output.save(buffer, format="PNG")
                    st.success("Your encrypted message has been hidden in the image.")
                    st.download_button(
                        "Download encoded PNG",
                        data=buffer.getvalue(),
                        file_name="stego_image.png",
                        mime="image/png",
                    )
        except Exception as exc:
            st.error(f"Could not open this image: {exc}")

with decode_tab:
    st.subheader("Extract a secret message")
    stego_file = st.file_uploader("Choose an image containing a hidden message", type=["png"], key="decode_image")
    decode_password = st.text_input("Password", type="password", key="decode_password")
    if stego_file is not None:
        try:
            stego_image = Image.open(stego_file)
            st.image(stego_image, caption="Selected encoded image", use_container_width=True)
            if st.button("Extract message", type="primary"):
                if not decode_password:
                    st.error("Please enter the password.")
                else:
                    secret = decode_message(stego_image, decode_password)
                    st.success("Message extracted successfully.")
                    st.text_area("Hidden message", value=secret, height=150)
        except SteganographyError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Could not process this image: {exc}")

with about_tab:
    st.subheader("How it works")
    st.markdown("""
    1. The message is encrypted using a key derived from your password.
    2. The encrypted bytes are embedded in the image's pixel values using the Least Significant Bit (LSB) method.
    3. The receiver uploads the PNG and enters the same password to extract and decrypt the message.

    **Important:** Use PNG for the encoded output. Saving it as JPEG can damage the hidden data because JPEG compression is lossy.
    """)
