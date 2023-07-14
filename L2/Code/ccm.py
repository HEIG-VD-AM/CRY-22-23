from Crypto.Cipher import AES
from Crypto.Util import Counter, strxor
from Crypto import Random
from base64 import b64encode, b64decode


def cbcmac(message: bytes, key: bytes) -> bytes: 
    if len(key) !=  16:
        raise Exception("Error. Need key of 128 bits")
    if len(message) % 16 != 0:
        raise Exception("Error. Message needs to be a multiple of 128 bits")
    cipher = AES.new(key,AES.MODE_ECB)
    temp = b"\x00"*16
    blocks = [message[i:i+16] for i in range(0,len(message),16)]
    for b in blocks:
        temp = strxor.strxor(temp,b)
        temp = cipher.encrypt(temp)
    return temp


def ccm(message: bytes, key: bytes) -> tuple:
    """Encrypts with AES128-CCM without authenticated data. """

    if len(key) != 16:
        raise Exception("Only AES-128 is supported")

    cipher = AES.new(key, mode = AES.MODE_CTR)
    tag = cbcmac(message, key)
    ciphertext = cipher.encrypt(message)
    #Encrypt tag for security
    cipher = AES.new(key, mode = AES.MODE_CTR, nonce = cipher.nonce) #Reinitialize counter
    tag = cipher.encrypt(tag)
    return (cipher.nonce, ciphertext, tag)


def decrypt_ccm(ciphertext: bytes, key: bytes, tag: bytes, nonce: bytes) -> bytes:
    """Decrypts with AES128-CCM without authenticated data. """

    if len(key) != 16:
        raise Exception("Only AES-128 is supported")

    plain = AES.new(key, mode = AES.MODE_CTR, nonce = nonce)
    plaintext = plain.decrypt(ciphertext)

    plain = AES.new(key, mode=AES.MODE_CTR, nonce=nonce)
    if tag != plain.encrypt(cbcmac(plaintext, key)):
        raise Exception("Invalid tag")

    return plaintext

def correct_ccm(message: bytes, key: bytes) -> tuple:

    cipher = AES.new(key, mode = AES.MODE_CCM)
    ciphertext, tag = cipher.encrypt_and_digest(message)
    return (cipher.nonce, ciphertext, tag)

def decrypt_correct_ccm(ciphertext: bytes, key: bytes, nonce: bytes, tag: bytes) -> bytes:

    plain = AES.new(key, mode = AES.MODE_CCM, nonce = nonce)
    plaintext = plain.decrypt_and_verify(ciphertext, tag)
    return plaintext

def poc_correct_ccm(m, k):
    print("POC CCM :")
    print("---------")

    iv, cipher, tag = correct_ccm(m, k)
    print(decrypt_correct_ccm(cipher, k, iv, tag))

def ccm_attack(m1, m2, c1, c2, IV1, IV2, tag1, tag2) :
    print("CCM ATTACK :")
    print("------------")

    # On déchiffre le tag du premier message
    tag1_not = strxor.strxor(strxor.strxor(tag1, m1[0:16]), c1[0:16])

    # On retrouve le keystream
    keystream2 = strxor.strxor(m2, c2)

    # On chiffre le tag du premier message avec le keystream du deuxième message
    enc_tag1 = strxor.strxor(tag1_not, keystream2[0:16])

    # On réalise l'attaque d'extension de longueur du CBC-MAC
    plain_mess = m1 + strxor.strxor(tag1_not, m1)

    # On chiffre le message avec le keystream du deuxième message
    enc_mess = strxor.strxor(plain_mess, keystream2)

    print("Chiffré :", b64encode(enc_mess))
    print("Tag :", b64encode(enc_tag1))
    print("IV :", b64encode(IV2))

    return (enc_mess, enc_tag1, IV2)


if __name__ == "__main__":
    m1 = b'Ceci est un test'
    m2 = b'Ceci est un autre test plus long'
    c1 = b64decode(b'BQO8qlj2aA/QVLAGJvsL+g==')
    IV1 = b64decode(b'TdOmiWpSnPs=')
    tag1 = b64decode(b'520MBQ52FPyzkKG0CTJtCQ==')
    c2 = b64decode(b'qnaNVBlYqPI3/NtZDLQTS3VnMtFQ7P7fmDok1ZLdCHA=')
    IV2 = b64decode(b'ETRuSjIOL2g=')
    tag2 = b64decode(b'miq+8q9fd4HUvzSTVzHa6Q==')

    ccm_attack(m1, m2, c1, c2, IV1, IV2, tag1, tag2)

    poc_correct_ccm(m1, b'1337deadbeef1337')



