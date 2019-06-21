import pyaes


def encryption(key , plaintext):
    key = key.encode('utf-8')
    aes = pyaes.AESModeOfOperationCTR(key)
    ciphertext = aes.encrypt(plaintext)
    return ciphertext

def decryption(key , ciphertext):
    key = key.encode('utf-8')
    aes = pyaes.AESModeOfOperationCTR(key)
    decrypted = aes.decrypt(ciphertext).decode('utf-8')
    return decrypted
