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
        return "the length of the key must be a multiple of the length of the input text"
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

