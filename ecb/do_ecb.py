from PIL import Image
from Crypto.Cipher import AES
import os

# Load the Tux image
input_image = "tux.png"
img = Image.open(input_image)

# Convert image to RGB if it has an alpha channel
if img.mode == 'RGBA':
    img = img.convert('RGB')

# Get image dimensions
width, height = img.size

# Convert image to raw bytes (RGB pixels)
pixel_data = img.tobytes()

# Generate a random 16-byte key for AES (128-bit)
key = os.urandom(16)

# Pad the data to be a multiple of 16 bytes (AES block size)
block_size = 16
padding_length = (block_size - len(pixel_data) % block_size) % block_size
padded_data = pixel_data + b'\x00' * padding_length

# Encrypt with AES-ECB
cipher = AES.new(key, AES.MODE_ECB)
encrypted_data = cipher.encrypt(padded_data)

# Truncate encrypted data to original length (remove padding)
encrypted_data = encrypted_data[:len(pixel_data)]

# Create a new image from encrypted data
encrypted_img = Image.frombytes('RGB', (width, height), encrypted_data)

# Save the encrypted image
encrypted_img.save('ecb_penguin.png')
print("Encrypted image saved as 'ecb_penguin.png'")