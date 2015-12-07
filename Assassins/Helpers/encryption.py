from hashlib import md5

def encrypt(unique_key, salt):
	m = md5()
	m.update((unique_key + salt).encode('utf-8'))
	return m.hexdigest()