#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>
#include <csignal>
#include <unistd.h>
#include <vector>
#include <algorithm>
#include <fstream>

#define TARGET_TIME (11 * 3600 + 59 * 60)

void handler(int signum) {
    std::cout << "Bomb!! The sand on the Hourglass has run out of sand!!" << std::endl;
    exit(1);
}

std::string decrypt(const std::string &encrypted_flag, int seed) {
    std::string transformed_flag;
    for (char c : encrypted_flag) {
        transformed_flag += static_cast<char>((c - seed + 256) % 256);
    }
    return transformed_flag;
}

void generate_problem(int &a, int &b, char &op) {
    const char ops[] = {'+', '-'};
    op = ops[rand() % 2];
    a = 100 + rand() % 1000000;
    b = 100 + rand() % 1000000;
    if (op == '-' && a < b) {
        std::swap(a, b);
    }
}

int solve_problem(int a, int b, char op) {
    if (op == '+') {
        return a + b;
    } else if (op == '-') {
        return a - b;
    }
    return 0;
}


std::string custom_base64_decode(const std::string &in) {
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

std::string load_from_file(const std::string &filename) {
    std::ifstream infile(filename);
    std::string data;
    if (infile.is_open()) {
        std::getline(infile, data, '\0');
        infile.close();
    } else {
        std::cerr << "Unable to open file for reading: " << filename << std::endl;
    }
    return data;
}

int main() {
    signal(SIGALRM, handler);
    alarm(TARGET_TIME);

    srand(static_cast<unsigned int>(time(nullptr)));
    time_t start_time = time(nullptr);

    while (true) {
        time_t current_time = time(nullptr);
        double elapsed_time = difftime(current_time, start_time);
        double remaining_time = TARGET_TIME - elapsed_time;

        int a, b;
        char op;
        generate_problem(a, b, op);
        int correct_answer = solve_problem(a, b, op);

        std::cout << "Times Tickin like bomb..." << std::endl;
        std::cout << a << " " << op << " " << b << " = ?" << std::endl;

        int user_answer;
        std::cout << "Answer: ";
        std::cin >> user_answer;

        if (user_answer == correct_answer) {
            std::cout << "Correct!!" << std::endl;
        } else {
            std::cout << "Incorrect!!! Bomb!!" << std::endl;
            break;
        }

        if (remaining_time <= 0) {
            std::cout << "The hourglass is broken.." << std::endl;
            std::string seed_string = "MyCn18";
            int seed = 0;
            for (char c : seed_string) seed += c;

            std::string loaded_encrypted_flag = load_from_file("Hourglass");

            std::string decrypted_flag = decrypt(loaded_encrypted_flag, seed);
            std::string decoded_flag = custom_base64_decode(decrypted_flag);

            std::cout << "Decrypted flag: " << decoded_flag << std::endl;
            break;
        }
    }

    std::cout << "The hourglass is broken.." << std::endl;
    return 0;
}
