import time
from pwn import remote
from Crypto.Util.number import bytes_to_long, long_to_bytes
from sage.all import PolynomialRing, Zmod

# Connect to the server
conn = remote('94.237.62.166', 34619)

# Use binary search to find n
low = 0
high = pow(2, 2048)
n = None

# Binary search loop with debug prints and timeout
while low <= high: 
    mid = (high + low) // 2
    conn.recvuntil(b"Option: ", timeout=5) 
    print(f"Sending option 2 with mid = {hex(mid)}")
    conn.sendline(b"2") 
    conn.recvuntil(b"Plaintext: ", timeout=5)
    conn.sendline(hex(mid).encode())
    response = conn.recvline() 
    print("Received response:", response)
    if b"Too many messages!" in response:
        high = mid - 1 
    else:
        low = mid + 1
n = low
print(f"Recovered n: {hex(n)}")

# Get the ciphertext c by selecting option 1
conn.recvuntil(b"Option: ", timeout=5)
conn.sendline(b"1")
output = conn.recvline().decode().strip()
c = int(output.split(": ")[1], 16)
print(f"Ciphertext c: {hex(c)}")

# Close the connection since we no longer need to interact with the server
conn.close()

# Use Stereotyped Message Attack to recover the plaintext (FLAG)
e = 3

# Try different lengths for the flag
for flag_length in range(16, 64):
    message = b"Hey! This is my secret... it is secure because RSA is extremely strong and very hard to break... Here you go: " + b'\x00' * flag_length 
    m = bytes_to_long(message)

    # Construct the polynomial for small roots attack
    P = PolynomialRing(Zmod(n), 'x') 
    x = P.gen()
    pol = (m + x)**e - c

    # Find the small roots 
    roots = pol.small_roots(epsilon=1/30)
    if roots: 
        print("Potential solutions:")
        for root in roots: 
            recovered_message = long_to_bytes(m + int(root)) 
            print("Recovered flag:", recovered_message)
