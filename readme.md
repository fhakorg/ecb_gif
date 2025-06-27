# What does it do:
Generates an animated GIF by encrypting an image, and capturing frames of the image ias it is being decrypted

# Why:
Demonstrates the fact that even if something is encrypted with AES, meaningful data can still be extracted

# How to run:
```
sudo apt update
sudo apt install python3 python3-venv python3-pip
python3 -m venv ecbv
source ecbv/bin/activate
pip install Pillow PyCryptodome numpy
python3 dec_ecb.py
```

should produce a file called decrypt_penguin.gif
