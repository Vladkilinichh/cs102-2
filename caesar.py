# -*- coding: utf-8 -*-
def encrypt_caesar(plaintext):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    new_data = []
    for char in plaintext:
        if 'a' <= char <= 'z':
            new_char = (ord(char) % ord('a') + 3) % 26 + ord('a')
        elif 'A' <= char <= 'Z':
            new_char = (ord(char) % ord('A') + 3) % 26 + ord('A')
        else:
            new_char = char
        new_data.append(new_char)
    return "".join(new_data)


def decrypt_caesar(plaintext):
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    new_data = []
    for char in plaintext:
        if 'a' <= char <= 'z':
            new_char = (ord(char) % ord('a') - 3) % 26 - ord('a')
        elif 'A' <= char <= 'Z':
            new_char = (ord(char) % ord('A') - 3) % 26 - ord('A')
        else:
            new_char = char
        new_data.append(new_char)
    return "".join(new_data)

