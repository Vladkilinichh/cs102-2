# -*- coding: utf-8 -*-
def encrypt_vigenere(plaintext, keyword):
    '''
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    "PYTHON"
    >>> encrypt_vigenere("python", "a")
    "python"
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    '''
    ciphertext = ''
    keyword = keyword.lower()
    for i in range(len(plaintext)):
        shift = ord(keyword[i % len(keyword)]) % ord('a')
        if 'a' <= plaintext[i] <= 'z':
            new_charcode = (ord(plaintext[i]) % ord('a')+shift) % 26 + ord('a')
        elif 'A' <= plaintext[i] <= 'Z':
            new_charcode = (ord(plaintext[i]) % ord('A')+shift) % 26 + ord('A')
        else:
            new_charcode = ord(plaintext[i])
        ciphertext += chr(new_charcode)
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    keyword = keyword.lower()
    for i in range(len(ciphertext)):
        shift = ord(keyword[i] % len(keyword)) % ord('a')
        if 'a' <= plaintext[i] <= 'z':
            new_charcode = (ord(plaintext[i]) % ord('a')-shift) % 26 + ord('a')
        elif 'A' <= plaintext[i] <= 'Z':
            new_charcode = (ord(plaintext[i]) % ord('A')-shift) % 26 + ord('A')
        else:
            new_charcode = ord(plaintext[i])
        ciphertext += chr(new_charcode)
    return plaintext
