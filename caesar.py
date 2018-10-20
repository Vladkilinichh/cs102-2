def encrypt_caesar(plaintext, shift = 3):
	'''
	Encrypts plaintext using a Caesar cipher.
	>>> encrypt_caesar("PYTHON")
	'SBWKRQ'
	>>> encrypt_caesar("python")
	'sbwkrq'
	>>> encrypt_caesar("Python3.6")
	'Sbwkrq3.6'
	>>> encrypt_caesar("")
	''
	'''
	cipher = ''
	for char in plaintext:
		if 'a' <= char <= 'z':
			new_charcode = (ord(char) % ord('a') + shift) % 26 + ord('a')  # for upper case
		elif 'A' <= char <= 'Z':
			new_charcode = (ord(char) % ord('A') + shift) % 26 + ord('A')  # for lower case
		else:
			new_charcode = ord(char)  # for other symbols
		cipher += chr(new_charcode)
	return cipher


def decrypt_caesar(cipher, shift = 3):
	"""
	Decrypts a ciphertext using a Caesar cipher.
	>>> decrypt_caesar("SBWKRQ")
	'PYTHON'
	>>> decrypt_caesar("sbwkrq")
	'python'
	>>> decrypt_caesar("Sbwkrq3.6")
	'Python3.6'
	>>> decrypt_caesar("")
	''
	"""
	plaintext = ''
	for char in cipher:
		if 'a' <= char <= 'z':
			new_charcode = (ord(char) % ord('a') - shift) % 26 + ord('a')  # for upper case
		elif 'A' <= char <= 'Z':
			new_charcode = (ord(char) % ord('A') - shift) % 26 + ord('A')  # for lower case
		else:
			new_charcode = ord(char)  # for other symbols
		plaintext += chr(new_charcode)
	return plaintext
