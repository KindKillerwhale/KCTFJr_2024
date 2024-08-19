def decrypt_password(encrypted):
    decrypted = []
    for i, value in enumerate(encrypted):
        if i % 2 == 0:
            original_value = value - 0x4F
        else:
            original_value = value + 0x58
        decrypted.append(chr(original_value))
    return ''.join(decrypted)

# Example usage
encrypted = [154, -21, 163, -18, 174, -14, 193, 35, 128, 27, 174, -39, 163, 7, 130, -23, 194, 1, 174, 15, 127, 7, 162, -39, 188, 24, 128, -19, 174, 26, 130, -2, 180, -6, 132, -39, 189, -17, 204]  # Given encrypted values

decrypted_password = decrypt_password(encrypted)
print("Decrypted password:", decrypted_password)
