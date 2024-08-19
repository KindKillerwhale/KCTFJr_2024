# flag_encrypt.py

flag = "KCTF_Jr{G4z3_4nd_r3V3rs3_0bFusC4t10N}"
key = 0xAA

# XOR와 시프팅을 이용한 암호화
encrypted_flag = ''.join([chr((ord(char) ^ key) + 3) for char in flag])
encrypted_bytes = [ord(char) for char in encrypted_flag]

print("Encrypted flag bytes:")
print(", ".join(f"0x{byte:02x}" for byte in encrypted_bytes))
