
# Steganography Tool for Hidden Data Communication
URL:https://steganography-hidden-data.streamlit.app/

A Python application that encrypts text and hides it inside an image using Least Significant Bit (LSB) steganography. A receiver can extract the message with the correct password.

## Features

- Hide text messages inside images.
- Encrypt messages using Fernet authenticated encryption.
- Derive encryption keys from passwords using PBKDF2-HMAC-SHA256.
- Extract and decrypt messages with the correct password.
- Simple Streamlit user interface.
- Capacity and invalid-image checks.

## Technology stack

- Python
- Streamlit
- Pillow
- Cryptography (Fernet)

## How it works

1. The application generates a random salt.
2. PBKDF2 derives an encryption key from the user's password and salt.
3. Fernet encrypts the message.
4. The app stores the salt and encrypted message in the image's RGB least significant bits.
5. The receiver uploads the PNG and enters the same password to decrypt it.

## Project structure

```text
Steganography-Tool-for-Hidden-Data-Communication/
├── app.py
├── stego.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

Python 3.10 or newer is recommended.

```bash
git clone https://github.com/YOUR-USERNAME/Steganography-Tool-for-Hidden-Data-Communication.git
cd Steganography-Tool-for-Hidden-Data-Communication

python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install dependencies and start the app:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will show a local URL, usually `http://localhost:8501`.

## Usage

### Hide a message
1. Open the **Hide a message** tab.
2. Upload a cover image.
3. Enter the secret text and a password.
4. Confirm the password.
5. Click **Hide message** and download the generated PNG.

### Extract a message
1. Open the **Extract a message** tab.
2. Upload the generated PNG.
3. Enter the same password.
4. Click **Extract message**.

## Important notes and limitations

- Use PNG for the encoded image. JPEG compression can destroy hidden LSB data.
- The output image is converted to RGB.
- The message must fit within the image's pixel capacity.
- Do not resize, crop, filter, or recompress the encoded image.
- This is an educational project, not a substitute for a professionally reviewed secure communication system.
- Anyone who suspects steganography may analyze an image; LSB embedding does not guarantee that the presence of a message is undetectable.

## Future improvements

- Support hiding files, not just text.
- Add image capacity estimation before encoding.
- Add drag-and-drop and preview improvements.
- Add automated unit tests.
- Explore more robust steganography methods.

## License

MIT
