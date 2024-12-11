from sympy import Integer
from mpmath import root

# Replace this with the ciphertext you copied
ciphertext_hex = '0x2f1a1896b48acfe92ef5dc065080f6e85'
ciphertext = int(ciphertext_hex, 16)

# Calculate the cube root using mpmath
plaintext = int(root(ciphertext, 3))

# Decode the plaintext
try:
    decoded_message = bytearray.fromhex(hex(plaintext)[2:]).decode()
    print("Decoded Message:", decoded_message)
except ValueError:
    print("Decoding failed. Ensure that the ciphertext is suitable for a cube root attack.")