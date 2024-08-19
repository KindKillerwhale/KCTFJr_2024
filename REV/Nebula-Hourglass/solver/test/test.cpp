#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <cstdlib>

std::string encrypt(const std::string &flag, int seed) {
    std::string encrypted_flag;
    for (char c : flag) {
        encrypted_flag += static_cast<char>((c + seed) % 256);
    }
    return encrypted_flag;
}

std::string decrypt(const std::string &encrypted_flag, int seed) {
    std::string transformed_flag;
    for (char c : encrypted_flag) {
        transformed_flag += static_cast<char>((c - seed + 256) % 256);
    }
    return transformed_flag;
}

std::string base64_encode(const std::string &in) {
    std::string out;
    int val = 0, valb = -6;
    for (unsigned char c : in) {
        val = (val << 8) + c;
        valb += 8;
        while (valb >= 0) {
            out.push_back("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"[(val >> valb) & 0x3F]);
            valb -= 6;
        }
    }
    if (valb > -6) out.push_back("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"[((val << 8) >> (valb + 8)) & 0x3F]);
    while (out.size() % 4) out.push_back('=');
    return out;
}

std::string base64_decode(const std::string &in) {
    std::string out;
    std::vector<int> T(256, -1);
    for (int i = 0; i < 64; i++) T["ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"[i]] = i;

    int val = 0, valb = -8;
    for (unsigned char c : in) {
        if (T[c] == -1) break;
        val = (val << 6) + T[c];
        valb += 6;
        if (valb >= 0) {
            out.push_back(char((val >> valb) & 0xFF));
            valb -= 8;
        }
    }
    return out;
}

void save_to_file(const std::string &filename, const std::string &data) {
    std::ofstream outfile(filename);
    if (outfile.is_open()) {
        outfile << data;
        outfile.close();
    } else {
        std::cerr << "Unable to open file for writing: " << filename << std::endl;
    }
}

std::string load_from_file(const std::string &filename) {
    std::ifstream infile(filename);
    std::string data;
    if (infile.is_open()) {
        std::getline(infile, data, '\0'); // Read the entire file content
        infile.close();
    } else {
        std::cerr << "Unable to open file for reading: " << filename << std::endl;
    }
    return data;
}

int main() {
    std::string flag = "KCTF_Jr{b1N4rY_4atCh_1n_t1m3_m4k3s_H0urg1a33_n3bU14}";
    std::string seed_string = "MyCn18";
    int seed = 0;
    for (char c : seed_string) {
        seed += c;
    }

    std::string encoded_flag = base64_encode(flag);
    std::string encrypted_flag = encrypt(encoded_flag, seed);
    std::cout << "Encrypted flag: " << encrypted_flag << std::endl;

    save_to_file("encrypted_flag", encrypted_flag);

    std::string loaded_encrypted_flag = load_from_file("encrypted_flag");
    std::cout << "Loaded encrypted flag: " << loaded_encrypted_flag << std::endl;

    std::string decrypted_flag = decrypt(loaded_encrypted_flag, seed);
    std::string decoded_flag = base64_decode(decrypted_flag);
    std::cout << "Decrypted flag: " << decoded_flag << std::endl;

    return 0;
}
