import random
import string

def generate_random_function_name():
    first_char = random.choice(string.ascii_letters)
    other_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=9))
    return first_char + other_chars

def generate_random_function_calls(function_names):
    num_calls = random.randint(1, 3)  # Each function calls 1 to 3 other functions
    calls = random.sample(function_names, num_calls)
    return '\n    '.join([f"{call}();" for call in calls])

fake_function_template = """
void {0}() {{
    asm volatile("" ::: "memory");
    {1}
}}
"""

function_names = [generate_random_function_name() for _ in range(20000)]

with open("fake_functions.c", "w") as f:
    for name in function_names:
        calls = generate_random_function_calls(function_names)
        f.write(fake_function_template.format(name, calls))
