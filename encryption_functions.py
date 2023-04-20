"""
This module is used for encryption functions implementation. \n
Only functions implementing encryption must be defined in the global namespace of this module.
Helper functions used by the encryption functions must be defined in 'enctyption_utils' module.
Encryption functions in this module can be defined using the following syntax: \n
def encryption_function_name(in_text, key, encrypt, alphabet): \n
    \"\"\"Encryption Method Name\"\"\" \n
    ACTIONS TO PERFORM... \n
    return out_text
"""

import encryption_utils
import math

# Encryption functions
def caesar(in_text, key, encrypt, alphabet):
    """Caesar cipher"""
    out_text = ""
    if encrypt == "encrypt":
        for s in in_text.upper():
            out_text += alphabet[(alphabet.find(s) + int(key)) % len(alphabet)]
    elif encrypt == "decrypt":
        for s in in_text.upper():
            out_text += alphabet[(alphabet.find(s) - int(key)) % len(alphabet)]
    return out_text

def linear(in_text, key, encrypt, alphabet):
    """Linear cipher"""
    out_text = ""
    if encryption_utils.relatively_prime(key, len(alphabet)) == False:
        return "ALPHABET LENGTH AND KEY MUST BE RELATIVELY PRIME NUMBERS"
    if encrypt == "encrypt":
        for s in in_text.upper():
            out_text += alphabet[(alphabet.find(s) * int(key)) % len(alphabet)]
    elif encrypt == "decrypt":
        for s in in_text.upper():
            out_text += alphabet[(alphabet.find(s) * encryption_utils.multiplicative_inverse(key, len(alphabet))) % len(alphabet)]
    return out_text

def affine(in_text, key, encrypt, alphabet):
    """Affine cipher"""
    key = tuple(map(int, key.split(',')))
    out_text = ""
    if encryption_utils.relatively_prime(key[0], len(alphabet)) == False:
        return "Alphabet length and first part of key must be relatively prime numbers"
    elif len(key) != 2:
        return "You need to enter two keys separated by comma"
    if encrypt == "encrypt":
        for s in in_text.upper():
            out_text += alphabet[(alphabet.find(s) * key[0] + key[1]) % len(alphabet)]
    elif encrypt == "decrypt":
        for s in in_text.upper():
            out_text += alphabet[(encryption_utils.multiplicative_inverse(key[0], len(alphabet)) * (alphabet.find(s) - key[1])) % len(alphabet)]
    return out_text
    
def playfair(in_text, key, encrypt, alphabet):
    """Playfair cipher"""
    in_text = in_text.upper()
    key = key.upper()
    out_text = ""
    alphabet_check = encryption_utils.check_against_alphabet(alphabet, key, in_text)
    if alphabet_check != True:
        return alphabet_check
    def corners_replacement(): # Function that is used both for encryption and decryption of bigrams located in different rows and columns
        nonlocal out_text
        if matrix_alphabet[bigram[0]][1] > matrix_alphabet[bigram[1]][1]:
            column_difference = matrix_alphabet[bigram[0]][1] - matrix_alphabet[bigram[1]][1]     
            new_first_bigram_letter_coord = (matrix_alphabet[bigram[0]][0], matrix_alphabet[bigram[0]][1] - column_difference)
            new_first_bigram_letter = list(matrix_alphabet.keys())[list(matrix_alphabet.values()).index(new_first_bigram_letter_coord)]
            new_second_bigram_letter_coord = (matrix_alphabet[bigram[1]][0], matrix_alphabet[bigram[1]][1] + column_difference)
            new_second_bigram_letter = list(matrix_alphabet.keys())[list(matrix_alphabet.values()).index(new_second_bigram_letter_coord)]
            out_text = out_text + new_first_bigram_letter + new_second_bigram_letter
        elif matrix_alphabet[bigram[0]][1] < matrix_alphabet[bigram[1]][1]:
            column_difference = matrix_alphabet[bigram[1]][1] - matrix_alphabet[bigram[0]][1]
            new_first_bigram_letter_coord = (matrix_alphabet[bigram[0]][0], matrix_alphabet[bigram[0]][1] + column_difference)
            new_first_bigram_letter = list(matrix_alphabet.keys())[list(matrix_alphabet.values()).index(new_first_bigram_letter_coord)]
            new_second_bigram_letter_coord = (matrix_alphabet[bigram[1]][0], matrix_alphabet[bigram[1]][1] - column_difference)
            new_second_bigram_letter = list(matrix_alphabet.keys())[list(matrix_alphabet.values()).index(new_second_bigram_letter_coord)]
            out_text = out_text + new_first_bigram_letter + new_second_bigram_letter

    if not encryption_utils.is_perfect_square(len(alphabet)):
        return "The number of characters in the alphabet must be a perfect square"
    elif not all(char in alphabet for char in key):
        return "The key contains a character that is not presented in the alphabet"
    alphabet_with_key = "".join(dict.fromkeys(key + alphabet)) # Alphabet with key (Duplicate characters are deleted)
    matrix_alphabet = encryption_utils.matrix_alphabet(alphabet_with_key)
    matrix_dimension = int(math.sqrt(len(alphabet)))

    if encrypt == "encrypt":
        in_text = encryption_utils.ins_btw_rpt_char(in_text, alphabet) # Insert additional characters into the text if the same characters follow each other
        in_text = encryption_utils.bigrams(in_text, alphabet) # Split the text into bigrams
        for bigram in in_text:
            # If the letters of bigram are in one row
            if matrix_alphabet[bigram[0]][0] == matrix_alphabet[bigram[1]][0]: 
                new_first_bigram_letter_coord = (matrix_alphabet[bigram[0]][0], (matrix_alphabet[bigram[0]][1] + 1) % matrix_dimension)
                new_first_bigram_letter = list(matrix_alphabet.keys())[list(matrix_alphabet.values()).index(new_first_bigram_letter_coord)]
                new_second_bigram_letter_coord = (matrix_alphabet[bigram[1]][0], (matrix_alphabet[bigram[1]][1] + 1) % matrix_dimension)
                new_second_bigram_letter = list(matrix_alphabet.keys())[list(matrix_alphabet.values()).index(new_second_bigram_letter_coord)]
                out_text = out_text + new_first_bigram_letter + new_second_bigram_letter
            # If the letters of bigram are in one column
            elif matrix_alphabet[bigram[0]][1] == matrix_alphabet[bigram[1]][1]:
                new_first_bigram_letter_coord = ((matrix_alphabet[bigram[0]][0] + 1) % matrix_dimension, matrix_alphabet[bigram[0]][1])
                new_first_bigram_letter = list(matrix_alphabet.keys())[list(matrix_alphabet.values()).index(new_first_bigram_letter_coord)]
                new_second_bigram_letter_coord = ((matrix_alphabet[bigram[1]][0] + 1) % matrix_dimension, matrix_alphabet[bigram[1]][1])
                new_second_bigram_letter = list(matrix_alphabet.keys())[list(matrix_alphabet.values()).index(new_second_bigram_letter_coord)]
                out_text = out_text + new_first_bigram_letter + new_second_bigram_letter
            # If the letters of bigram are in different columns and rows
            else:
                corners_replacement()

    elif encrypt == "decrypt":
        in_text = encryption_utils.bigrams(in_text, alphabet) # Split the text into bigrams
        for bigram in in_text:
            # If the letters of bigram are in one row
            if matrix_alphabet[bigram[0]][0] == matrix_alphabet[bigram[1]][0]: 
                new_first_bigram_letter_coord = (matrix_alphabet[bigram[0]][0], (matrix_alphabet[bigram[0]][1] - 1) % matrix_dimension)
                new_first_bigram_letter = list(matrix_alphabet.keys())[list(matrix_alphabet.values()).index(new_first_bigram_letter_coord)]
                new_second_bigram_letter_coord = (matrix_alphabet[bigram[1]][0], (matrix_alphabet[bigram[1]][1] - 1) % matrix_dimension)
                new_second_bigram_letter = list(matrix_alphabet.keys())[list(matrix_alphabet.values()).index(new_second_bigram_letter_coord)]
                out_text = out_text + new_first_bigram_letter + new_second_bigram_letter
            # If the letters of bigram are in one column
            elif matrix_alphabet[bigram[0]][1] == matrix_alphabet[bigram[1]][1]:
                new_first_bigram_letter_coord = ((matrix_alphabet[bigram[0]][0] - 1) % matrix_dimension, matrix_alphabet[bigram[0]][1])
                new_first_bigram_letter = list(matrix_alphabet.keys())[list(matrix_alphabet.values()).index(new_first_bigram_letter_coord)]
                new_second_bigram_letter_coord = ((matrix_alphabet[bigram[1]][0] - 1) % matrix_dimension, matrix_alphabet[bigram[1]][1])
                new_second_bigram_letter = list(matrix_alphabet.keys())[list(matrix_alphabet.values()).index(new_second_bigram_letter_coord)]
                out_text = out_text + new_first_bigram_letter + new_second_bigram_letter
            # If the letters of bigram are in different columns and rows
            else:
                corners_replacement()
    return out_text

def hill(in_text, key, encrypt, alphabet):
    """Hill cipher (9-characters long key)"""
    in_text = in_text.upper()
    key = key.upper()
    out_text = ""
    alphabet_check = encryption_utils.check_against_alphabet(alphabet, key, in_text)
    if alphabet_check != True:
        return alphabet_check
    if len(key) != 9:
        return "Key length should be equal to 9"
    # Converting the key to a matrix
    key_matrix = [[0 for j in range(3)] for i in range(3)] # Initialization of the matrix
    for i in range(9):
        key_matrix[i//3][i%3] = key[i]
    # Converting key characters in the matrix to numeric representations
    key_matrix = encryption_utils.matrix_characters_to_numbers(key_matrix, alphabet)
    # Check whether the key can be used for encryption
    if encryption_utils.matrix_det_3x3(key_matrix) == 0:
        return "This key cannot be used. Determinant of this key is equal to 0"
    elif encryption_utils.gcd(encryption_utils.matrix_det_3x3(key_matrix), len(alphabet)) != 1:
        return "GCD of the key determinant and alphabet length should have no common factors (except 1)."
    # Split the input text by 3 characters
    if len(in_text) % 3 != 0:
        return "The number of characters in the input text must be divisible by 3 without a remainder"
    splitted_text = [list(in_text[i:i+3]) for i in range(0, len(in_text), 3)]
    # Converting text characters in the matrix to numeric representations
    splitted_text = encryption_utils.matrix_characters_to_numbers(splitted_text, alphabet)

    if encrypt == "encrypt":
        encrypted = []
        # Multiply the set of character numbers by the character numbers of the key
        for char_set in splitted_text:
            encrypted.append(encryption_utils.matrix_multiplication([char_set], key_matrix))
        # Apply the modulus to each number of the matrix
        for char_set in range (len(encrypted)):
            encrypted[char_set] = encryption_utils.matrix_elements_modules(encrypted[char_set], len(alphabet))
        # Unpack the sets of numbers
        encrypted = [char_set[0] for char_set in encrypted]
        # Converting numbers in the matrix to its character representations
        encrypted = encryption_utils.matrix_numbers_to_characters(encrypted, alphabet)
        # Encryption Result
        for char_sets in encrypted:
            for char_set in char_sets:
                out_text += char_set
    elif encrypt == "decrypt":
        decrypted = []
        # Invert the key matrix
        key_matrix = encryption_utils.matrix_mod_inverse_3x3(key_matrix, len(alphabet))
        # Multiply the set of character numbers by the character numbers of the key
        for char_set in splitted_text:
            decrypted.append(encryption_utils.matrix_multiplication([char_set], key_matrix))
        # Apply the modulus to each number of the matrix
        for char_set in range (len(decrypted)):
            decrypted[char_set] = encryption_utils.matrix_elements_modules(decrypted[char_set], len(alphabet))
        # Unpack the sets of numbers
        decrypted = [char_set[0] for char_set in decrypted]
        # Converting numbers in the matrix to its character representations
        decrypted = encryption_utils.matrix_numbers_to_characters(decrypted, alphabet)
        # Encryption Result
        for char_sets in decrypted:
            for char_set in char_sets:
                out_text += char_set
    return out_text

def vigenere(in_text, key, encrypt, alphabet):
    """Vigenere cipher"""
    in_text = in_text.upper()
    key = key.upper()
    enc_data = []
    out_text = ""
    alphabet_check = encryption_utils.check_against_alphabet(alphabet, key, in_text)
    if alphabet_check != True:
        return alphabet_check
    if len(key) > len(in_text):
        return "The length of the key cannot be less than the length of the input text"
    # Convert input text to list
    in_text = list(in_text)
    # Convert key to list 
    key = list(key)
    key_list = []
    key_len = len(key)
    for i in range(len(in_text)):
        key_list.append(key[i % key_len])
    # Convert characters in lists to its numeric representations based on alphabet
    in_text = encryption_utils.list_characters_to_numbers(in_text, alphabet)
    key_list = encryption_utils.list_characters_to_numbers(key_list, alphabet)

    if encrypt == "encrypt":
        for i in range(len(in_text)):
            enc_data.append((in_text[i] + key_list[i]) % len(alphabet))
    elif encrypt == "decrypt":
        for i in range(len(in_text)):
            enc_data.append((in_text[i] - key_list[i]) % len(alphabet))
    out_text = encryption_utils.list_numbers_to_characters(enc_data, alphabet)
    out_text = ''.join(out_text)
    return out_text

def single_permutation(in_text, key, encrypt, alphabet = None):
    """Single permutation cipher"""
    out_text = len(in_text) * "-"
    key = key.split(",")
    key = [int(i) for i in key]
    if len(in_text) != len(key):
        return "The length of the input text and the length of the key must be the same"
    elif all([isinstance(i, int) for i in key]) == False:
        return "The key must consist of numbers separated by commas"
    if encrypt == "encrypt":
        for i in range(len(in_text)):
            out_text = out_text[:i] + in_text[key[i] - 1] + out_text[i + 1:]
    elif encrypt == "decrypt":
        for i in range(len(in_text)):
            out_text = out_text[:key[i] - 1] + in_text[i] + out_text[key[i]:]
    return out_text

def block_permutation(in_text, key, encrypt, alphabet = None):
    """Block permutatuon cipher"""
    out_text = ""
    key = key.split(",")
    key = [int(i) for i in key]
    if len(in_text) % len(key) != 0:
        return "The length of the key must be a multiple of the length of the input text"
    elif all([isinstance(i, int) for i in key]) == False:
        return "The key must consist of numbers separated by commas"
    if encrypt == "encrypt":
        for i in range(0, len(in_text), len(key)):
            chunk = in_text[i:i + len(key)]
            changed_chunk = len(chunk) * "-"
            for j in range(len(chunk)):
                changed_chunk = changed_chunk[:j] + chunk[key[j] - 1] + changed_chunk[j + 1:]
            out_text += changed_chunk
    elif encrypt == "decrypt":
        for i in range(0, len(in_text), len(key)):
            chunk = in_text[i:i + len(key)]
            changed_chunk = len(chunk) * "-"
            for j in range(len(chunk)):
                changed_chunk = changed_chunk[:key[j] - 1] + chunk[j] + changed_chunk[key[j]:]
            out_text += changed_chunk
    return out_text

def columnar_transposition(in_text, key, encrypt, alphabet):
    """Columnar transposition cipher"""
    out_text = ""
    if len(set(key)) != len(key):
        return "Characters in the key must not be repeated"
    elif len(in_text) % len(key) != 0:
        return "The length of the key must be a multiple of the length of the input text"
    # Converting a key to a list showing the order in which letters appear
    key = list(key.upper())
    key = encryption_utils.list_characters_to_numbers(key, alphabet)
    key = encryption_utils.increasing_numbers_order(key)
    if encrypt == "encrypt":
        # Conversion of input text into a matrix
        in_text = [list(in_text[i:i + len(key)]) for i in range(0, len(in_text), len(key))]
        # Encryption
        temp_key = key.copy()
        for i in range(len(key)):
            min_key_value = min(temp_key)
            column = key.index(min_key_value)
            temp_key.remove(min_key_value)
            for j in range(len(in_text)):
                out_text += in_text[j][column]
    elif encrypt == "decrypt":
        rows_number = len(in_text) // len(key)
        # Initialization of the matrix for decryption
        decrypted_matrix = [len(key) * [0] for i in range(rows_number)]
        # Decryption
        for i in range(len(in_text)):
            column = key.index(i // rows_number)
            decrypted_matrix[i % rows_number][column] = in_text[i]
        for i in decrypted_matrix:
            for j in i:
                out_text += j
    return out_text

def double_transposition(in_text, key, encrypt, alphabet):
    """Double transposition cipher"""
    out_text = ""
    key = key.upper()
    key = key.split("\n")
    # Checking the correctness of keys
    if len(key) != 2 :
        return "Write the two keys on two different lines.\nThe first key is used for columns transposition, and the second one is used for rows transposition"
    elif len(in_text) % len(key[0]) != 0:
        return "The length of the first key must be a multiple of the length of the input text"
    elif (len(set(key[0])) != len(key[0])) or (len(set(key[1])) != len(key[1])):
        return "Characters in the keys must not be repeated"
    elif len(in_text) % len(key[1]) != 0:
        return "The length of the second key must be a multiple of the length of the input text"
    elif len(key[0]) * len(key[1]) != len(in_text):
        return "The product of the length of the two keys must be equal to the length of the input text"
    # Converting the keys to lists showing the order in which letters appear
    key1 = encryption_utils.list_characters_to_numbers(list(key[0]), alphabet)
    key1 = encryption_utils.increasing_numbers_order(key1)
    key2 = encryption_utils.list_characters_to_numbers(list(key[1]), alphabet)
    key2 = encryption_utils.increasing_numbers_order(key2)
    if encrypt == "encrypt":
        # Conversion of the input text into a matrix
        in_text = [list(in_text[i:i + len(key1)]) for i in range(0, len(in_text), len(key1))]
        # Encryption (columns transposition)
        columns_transposed_text = ""
        temp_key = key1.copy()
        for i in range(len(key1)):
            min_key_value = min(temp_key)
            column = key1.index(min_key_value)
            temp_key.remove(min_key_value)
            for j in range(len(in_text)):
                columns_transposed_text += in_text[j][column]
        # Conversion of changed text into a matrix
        columns_transposed_text = [list(columns_transposed_text[i:i + len(key2)]) for i in range(0, len(columns_transposed_text), len(key2))]
        # Encryption (rows transposition)
        for i in range(len(columns_transposed_text)):
            temp_key = key2.copy()
            for j in range(len(key2)):
                min_key_value = min(temp_key)
                row = key2.index(min_key_value)
                temp_key.remove(min_key_value)
                out_text += columns_transposed_text[i][row]
    elif encrypt == "decrypt":
        rows_number = len(in_text) // len(key1)
        columns_number = len(in_text) // rows_number
        # Initialization of the matrix for decryption
        decrypted_matrix = [len(key1) * [0] for i in range(rows_number)]
        # Decryption (rows transposition)
        rows_transposed_text = ""
        for i in range(len(in_text)):
            column = i // rows_number
            row = key2.index(i % rows_number)
            decrypted_matrix[row][column] = in_text[i]
        for i in range(len(decrypted_matrix[0])):
            for j in range(len(decrypted_matrix)):
                rows_transposed_text += decrypted_matrix[j][i]
        # Decryption (columns transposition)
        for i in range(len(rows_transposed_text)):
            column = key1.index(i // rows_number)
            decrypted_matrix[i % rows_number][column] = rows_transposed_text[i]
        for i in decrypted_matrix:
            for j in i:
                out_text += j
    return out_text

def cardan_grille(in_text, key, encrypt, alphabet = None):
    """Cardan grille cipher (square)"""
    out_text = ""
    key_matrix = [list(i) for i in key.split("\n")]
    key_matrix = [[int(j) for j in i] for i in key_matrix]
    key_matrix_dimension = len(key_matrix)
    key_matrix_size = key_matrix_dimension * key_matrix_dimension
    grille_pierces = key.count("1")
    # Checking the correctness of the key
    key_error = "The key can only be a square matrix consisting of 0 and 1 (1 means a grille pierce).\n You can only choose a matrix of such a dimension that the total number of matrix elements can be divided by 4 without a remainder"
    pierce_coincidence_error = "When the grille is turned over, the pierces coincide. Place the pierces in a different order"
    if all([all([True if j==0 or j==1 else False for j in i]) for i in key_matrix]) == False:
        return key_error
    elif all([len(row) == len(key_matrix) for row in key_matrix]) == False:
        return key_error
    elif len(in_text) != key_matrix_size:
        return "The number of characters of the initial text must be equal to the number of elements of the key matrix"
    elif key_matrix_size % 4 != 0:
        return key_error
    elif len(key_matrix) < 4:
        return "The minimum dimension of the matrix is 4"
    elif key_matrix_size  % grille_pierces != 0:
        return "The number of grille pierces '1' must be divisible by the total number of elements of the matrix without a remainder" 
    for i in range(key_matrix_dimension):
        for j in range(key_matrix_dimension):
            if key_matrix[i][j] == 1:
                if key_matrix[i][key_matrix_dimension - 1 - j] == 1:
                    return pierce_coincidence_error
    for i in range(key_matrix_dimension):
        for j in range(key_matrix_dimension):
            if key_matrix[i][j] == 1:
                if key_matrix[key_matrix_dimension - 1 - i][key_matrix_dimension - 1 - j]:
                    return pierce_coincidence_error
    for i in range(key_matrix_dimension):
        for j in range(key_matrix_dimension):
            if key_matrix[i][j] == 1:
                if key_matrix[key_matrix_dimension - 1 - i][j] == 1:
                    return pierce_coincidence_error
                
    if encrypt == "encrypt" or encrypt == "decrypt":
        character_counter = 0
        result_matrix = [key_matrix_dimension * [0] for i in range(key_matrix_dimension)]
        def write_iteration_to_matrix():
            nonlocal character_counter
            for i in range(key_matrix_dimension):
                for j in range(key_matrix_dimension):
                    if buff_key_matrix[i][j] == 1:
                        result_matrix[i][j] = in_text[character_counter]
                        character_counter += 1
        # Initial grille
        buff_key_matrix = key_matrix.copy()
        write_iteration_to_matrix()
        buff_key_matrix = [key_matrix_dimension * [0] for i in range(key_matrix_dimension)]
        for i in range(key_matrix_dimension):
            for j in range(key_matrix_dimension):
                if key_matrix[i][j] == 1:
                    buff_key_matrix[i][key_matrix_dimension - 1 - j] = 1
        # The first turn of the grille
        write_iteration_to_matrix()
        buff_key_matrix = [key_matrix_dimension * [0] for i in range(key_matrix_dimension)]
        for i in range(key_matrix_dimension):
            for j in range(key_matrix_dimension):
                if key_matrix[i][j] == 1:
                    buff_key_matrix[key_matrix_dimension - 1 - i][key_matrix_dimension - 1 - j] = 1
        # The second turn of the grille
        write_iteration_to_matrix()
        buff_key_matrix = [key_matrix_dimension * [0] for i in range(key_matrix_dimension)]
        for i in range(key_matrix_dimension):
            for j in range(key_matrix_dimension):
                if key_matrix[i][j] == 1:
                    buff_key_matrix[key_matrix_dimension - 1 - i][j] = 1
        # The third turn of the grille
        write_iteration_to_matrix()
        # Result output
        for i in range(key_matrix_dimension):
            for j in range(key_matrix_dimension):
                out_text += result_matrix[j][i]
    return out_text
