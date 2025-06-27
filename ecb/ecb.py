from PIL import Image
from Crypto.Cipher import AES
import os
import numpy as np

# input_image = "tux_dark.png"
input_image = "light_tux.png"

try:
    img = Image.open(input_image)
except FileNotFoundError:
    print("Error: tux.png not found in current directory")
    exit(1)

if img.mode == 'RGBA':
    img = img.convert('RGB')

orig_width, orig_height = img.size

# Calculate target width for 16:10 aspect ratio
target_ratio = 16 / 10
target_width = int(orig_height * target_ratio)

padded_img = Image.new('RGB', (target_width, orig_height), (255, 255, 255))  # White background
offset = (target_width - orig_width) // 2
padded_img.paste(img, (offset, 0))

width, height = padded_img.size
if width / height != target_ratio:
    print(f"Warning: Aspect ratio is {width/height:.2f}, not exactly 16:10")

original_data = padded_img.tobytes()

# Generate a random 16-byte key for AES (128-bit)
key = os.urandom(16)

with open('aes_key.bin', 'wb') as key_file:
    key_file.write(key)
print("Encryption key saved as 'aes_key.bin'")

block_size = 16
padding_length = (block_size - len(original_data) % block_size) % block_size
padded_data = original_data + b'\x00' * padding_length

# Encrypt with AES-ECB
cipher = AES.new(key, AES.MODE_ECB)
encrypted_data = cipher.encrypt(padded_data)

encrypted_data = encrypted_data[:len(original_data)]

# Create and save the encrypted image
encrypted_img = Image.frombytes('RGB', (width, height), encrypted_data)
encrypted_img.save('ecb_penguin.png')
print("Encrypted image saved as 'ecb_penguin.png'")

# Generate GIF animation of decryption
num_frames = 50
frames = []

enc_pixels = np.frombuffer(encrypted_data, dtype=np.uint8).reshape(-1, 3)
orig_pixels = np.frombuffer(original_data, dtype=np.uint8).reshape(-1, 3)

# Generate forward and reverse frames
for i in range(num_frames + 1):
    t = i / num_frames
    interpolated_pixels = (1 - t) * enc_pixels + t * orig_pixels
    interpolated_pixels = interpolated_pixels.astype(np.uint8)
    
    frame_data = interpolated_pixels.tobytes()
    frame_img = Image.frombytes('RGB', (width, height), frame_data)
    frames.append(frame_img)

# Add reverse frames (skip the last frame to avoid duplication)
for i in range(num_frames - 1, -1, -1):
    t = i / num_frames
    interpolated_pixels = (1 - t) * enc_pixels + t * orig_pixels
    interpolated_pixels = interpolated_pixels.astype(np.uint8)
    
    frame_data = interpolated_pixels.tobytes()
    frame_img = Image.frombytes('RGB', (width, height), frame_data)
    frames.append(frame_img)

# Save as GIF
frames[0].save(
    'decrypt_penguin.gif',
    save_all=True,
    append_images=frames[1:],
    duration=100,  # milliseconds per frame (100ms = 10fps)
    loop=0  # Loop forever
)
print("GIF saved as 'decrypt_penguin.gif'")