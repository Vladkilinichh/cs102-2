# -*- coding: utf-8 -*-
def encrypt_caesar(plaintext):
    new_data = []
    for char in plaintext:
        if(ord(char ) >= 97 and ord(char) <= 122): 
            new_char = chr((ord(char) - 97 + 3) % 26 + 97)  # для маленькой
        elif( ord(char) >= 65 and ord(char) <= 90 ):
            new_char = chr((ord(char) - 65 + 3) % 26 + 65) # для большой
        else:
            new_char = char
        new_data.append(new_char)
    return "".join(new_data)
print(encrypt_caesar(input('Введите текст на англе')))





def encrypt_caesar(plaintext):
    new_data = []
    for char in plaintext:
        if(ord(char ) >= 97 and ord(char) <= 122): 
            new_char = chr((ord(char) - 97 - 3) % 26 + 97)  # для маленькой
        elif( ord(char) >= 65 and ord(char) <= 90 ):
            new_char = chr((ord(char) - 65 - 3) % 26 + 65) # для большой
        else:
            new_char = char
        new_data.append(new_char)
    return "".join(new_data)
print(encrypt_caesar(input('Введите текст на англе')))