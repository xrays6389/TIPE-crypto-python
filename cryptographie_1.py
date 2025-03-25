from cryptography.AES import AES

key = AES.generate_key(16)
k = AES(key) 

print(k)