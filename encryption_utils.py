"""
Helper functions used by the encryption functions in the encryption_functions module
"""

import math

# Finding the greatest common divisor
def gcd(a, b):
    a = int(a)
    b = int(b)
    if b > a:
        a, b = b, a
    if b != 0:
        return gcd(b, a % b)
    else:
        return a

# Euler's function 
def eulsers_func(n):
    n = int(n)
    relatively_prime_sum = 0
    for i in range(1, n):
        if gcd(n, i) == 1:
            relatively_prime_sum += 1
    return relatively_prime_sum

# Finding the modular multiplicative inverse
def multiplicative_inverse(num, mod_div):
    num = int(num)
    mod_div = int(mod_div)
    if gcd(num, mod_div) != 1:
        return f"Error. The numbers {num} and {mod_div} have a greatest common divisor that is not equal to one"
    inversed_num = num**(eulsers_func(mod_div) - 1) % mod_div
    return inversed_num

# Determining whether the numbers are relatively prime
def relatively_prime(a, b):
    a = int(a)
    b = int(b)
    if gcd(a, b) != 1:
        return False
    elif gcd(a,b) == 1: 
        return True
    
# Determing whether the number is a perfect square
def is_perfect_square(num):
    sqrt = math.sqrt(num)
    return (sqrt - int(sqrt)) == 0

# Create an alphabet matrix
def matrix_alphabet(alphabet):
    matrix = {}
    if is_perfect_square(len(alphabet)):
        matrix_dimension = int(math.sqrt(len(alphabet)))
        for i in range(len(alphabet)):
            matrix[alphabet[i]] = (i // matrix_dimension, i % matrix_dimension)
        return matrix
    else:
        return "Alphabet length is wrong"
    
# Insert the last aplhabet character between repeating characters
def ins_btw_rpt_char(text, alphabet):
    repeat_indexes = []
    # Indexes searching that must be followed by an additional letter
    for i in range(len(text) - 1):
        if text[i] == text[i + 1]:
            repeat_indexes.append(i)
    # Letters adding and dynamically indexes shifting 
    for i in repeat_indexes:
        text = text[:i + 1] + alphabet[-1] + text[i + 1:]
        for j in range(len(repeat_indexes)):
            repeat_indexes[j] += 1
    return text

#print(ins_btw_rpt_char("BAA", "FEGRth!"))

# Breake a string into bigrams
def bigrams(text, alphabet):
    if len(text) % 2 != 0:
        text = text + alphabet[-1]
    bigram_list = [text[i:i + 2] for i in range(0, len(text), 2)]
    return bigram_list
