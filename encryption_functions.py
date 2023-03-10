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

    out_text = ""
    if not encryption_utils.is_perfect_square(len(alphabet)):
        return "The number of characters in the alphabet must be a perfect square"
    elif not all(char in alphabet for char in key):
        return "The key contains a character that is not presented in the alphabet"
    alphabet_with_key = "".join(dict.fromkeys(key + alphabet)) # Alphabet with key (Duplicate characters are deleted)
    matrix_alphabet = encryption_utils.matrix_alphabet(alphabet_with_key)
    print(matrix_alphabet)
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

