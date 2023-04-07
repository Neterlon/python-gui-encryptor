"""
Helper functions used by the encryption functions in the encryption_functions module
"""

import math

# Check whether the characters of the key and the input text are in the alphabet
def check_against_alphabet(alphabet, key, text):
    if not all(char in alphabet for char in key):
        return "The key contains a character that is not presented in the alphabet"
    if not all(char in alphabet for char in text):
        return "Input text contains a character that is not presented in the alphabet"
    return True

# Finding the greatest common divisor
def gcd(a, b):
    a = abs(int(a))
    b = abs(int(b))
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

# Breake a string into bigrams
def bigrams(text, alphabet):
    if len(text) % 2 != 0:
        text = text + alphabet[-1]
    bigram_list = [text[i:i + 2] for i in range(0, len(text), 2)]
    return bigram_list

# Matrix multiplication
def matrix_multiplication(matrix_a, matrix_b):
    if len(matrix_a[0]) != len(matrix_b) or len({len(i) for i in matrix_a}) != 1 or len({len(i) for i in matrix_b}) != 1:
        return "Matrices cannot be multiplied"
    matrix_res = [[0 for i in range(len(matrix_b[0]))] for j in range(len(matrix_a))] # Initialization of the resulting matrix
    for i in range(len(matrix_a)): # iterate through rows of matrix_a
        for j in range(len(matrix_b[0])): # iterate through columns of matrix_b
            for k in range(len(matrix_b)): # iterate through rows of matrix_b
                matrix_res[i][j] += matrix_a[i][k] * matrix_b[k][j]
    return matrix_res

# Matrix multiplication by a scalar
def matrix_scalar_multiplication(matrix, scalar):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            matrix[i][j] *= scalar
    return matrix

# Find modules of matrix elements
def matrix_elements_modules(matrix, mod):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = matrix[i][j] % mod
    return matrix

# Find the determinant of 2x2 Matrix
def matrix_det_2x2(matrix):
    if len(matrix) != len(matrix[0]) or len({len(i) for i in matrix}) != 1:
        return "Matrix size is wrong"
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

# Find the determinant of 3x3 Matrix
def matrix_det_3x3(matrix):
    if len(matrix) != len(matrix[0]) or len({len(i) for i in matrix}) != 1:
        return "Matrix size is wrong"
    return matrix[0][0] * matrix[1][1] * matrix[2][2] + \
        matrix[0][1] * matrix[1][2] * matrix[2][0] + \
        matrix[0][2] * matrix[1][0] * matrix[2][1] - \
        matrix[0][2] * matrix[1][1] * matrix[2][0] - \
        matrix[0][1] * matrix[1][0] * matrix[2][2] - \
        matrix[0][0] * matrix[1][2] * matrix[2][1]

# Find the inverse of a matrix with module
def matrix_mod_inverse_3x3(matrix, mod):
    if len(matrix) != len(matrix[0]) or len({len(i) for i in matrix}) != 1:
        return "Matrix size is wrong"
    # Find determinant
    det = matrix_det_3x3(matrix)
    if det == 0:
        return "The determinant of the matrix is equal to zero. The inverse of the matrix cannot be found"
    # Transpose matrix
    matrix_t = [[matrix[j][i] for j in range(3)] for i in range(3)]
    # Matrix of cofactors
    matrix_c = [[0 for column in range(3)] for row in range(3)] # Initialization of a matrix
    for i in range(3):
        for j in range(3):
            minor = [[matrix_t[m][n] for n in range(3) if n != j] for m in range(3) if m != i]
            matrix_c[i][j] = (-1)**(i+j) * matrix_det_2x2(minor)
    # Modulus of the inverted determinant
    if det > 0:
        det_minv = multiplicative_inverse(det, mod)
        minus_sign = 1
    elif det < 0:
        det_minv = multiplicative_inverse(-det, mod)
        minus_sign = -1
    if type(det_minv) == str:
        return det_minv
    # Multiply the transposed matrix by the modulus of the inverted determinant
    matrix_inv = [[((matrix_c[i][j] * det_minv) * minus_sign) % mod for j in range(3)] for i in range(3)]
    return matrix_inv

# Convert text characters in a matrix to its numeric representations in alphabet
def matrix_characters_to_numbers(matrix, alphabet):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = alphabet.index(matrix[i][j])
    return matrix

# Convert numbers in matrix to its character representations in alphabet
def matrix_numbers_to_characters(matrix, alphabet):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = alphabet[matrix[i][j]]
    return matrix

# Convert characters in list to its numeric representations based on alphabet
def list_characters_to_numbers(lst, alphabet):
    for i in range(len(lst)):
        lst[i] = alphabet.index(lst[i])
    return lst
# Convert numbers in list to its character representations based on alphabet
def list_numbers_to_characters(lst, alphabet):
    for i in range(len(lst)):
        lst[i] = alphabet[lst[i]]
    return lst

# Transform the list so that it displays the order of increasing numbers
def increasing_numbers_order(lst):
    temp_list = lst.copy()
    converted_list = [None for i in range(len(lst))]
    for i in range(len(lst)):
        min_number = min(temp_list)
        min_number_index = lst.index(min_number)
        converted_list[min_number_index] = i
        temp_list.remove(min_number)
    return converted_list