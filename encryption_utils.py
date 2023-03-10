# Helper functions used by the encryption functions 
# in the encryption_functions module

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
    