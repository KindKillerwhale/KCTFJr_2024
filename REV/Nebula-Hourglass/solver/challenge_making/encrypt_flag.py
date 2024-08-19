import base64

original_flag = "KCTF_Jr{b1N4rY_4atCh_1n_t1m3_m4k3s_H0urg1a33_c1ust3r}"

encoded_flag = base64.b64encode(original_flag.encode()).decode()
print(f"Encoded Flag: {encoded_flag}")

seed_string = "MyCn18"

seed = sum(ord(char) for char in seed_string)

def generate_flag(encoded_flag, seed):
    transformed_flag = ''.join(chr((ord(char) + seed) % 256) for char in encoded_flag)
    return transformed_flag

encrypted_flag = generate_flag(encoded_flag, seed)
print(f"Encrypted Flag: {encrypted_flag}")
