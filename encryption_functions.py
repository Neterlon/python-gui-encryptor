import encryption_utils

# Encryption functions

def caesar(in_text, key, encrypt, alphabet):
    """Caesar cipher"""
    out_text = ""
    if encrypt == "encrypt":
        for s in in_text.upper():
            out_text += alphabet[(alphabet.find(s) + int(key)) % len(alphabet)]
        return out_text
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
        print(len(alphabet), key)
        for s in in_text.upper():
            out_text += alphabet[(alphabet.find(s) * int(key)) % len(alphabet)]
        return out_text
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
            out_text += alphabet[(alphabet.find(s) * int(key[0]) + int(key[1])) % len(alphabet)]
        return out_text
    elif encrypt == "decrypt":
        for s in in_text.upper():
            out_text += alphabet[(encryption_utils.multiplicative_inverse(key[0], len(alphabet)) * (alphabet.find(s) - key[1])) % len(alphabet)]
        return out_text