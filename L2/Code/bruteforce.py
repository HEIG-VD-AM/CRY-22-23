from base64 import b64encode, b64decode
from Crypto import Random
from Crypto.Cipher import AES
import sys

KEY_SIZE = 2  # In bytes


def bruteforce(plaintext, ciphertext):
    enc_pairs = dict()
    key_pair = (None, None)

    ## BRUTEFORCE
    for i in range(2 ** (KEY_SIZE * 8)):
        key = bytes([i // 256]) + bytes([i % 256]) + b"\x00" * (32 - KEY_SIZE)
        AES_intermediate = AES.new(key, AES.MODE_ECB)
        enc_pairs[AES_intermediate.encrypt(plaintext)] = key

    for i in range(2 ** (KEY_SIZE * 8)):
        key = bytes([i // 256]) + bytes([i % 256]) + b"\x00" * (32 - KEY_SIZE)
        AES_intermediate = AES.new(key, AES.MODE_ECB)
        intermediate = AES_intermediate.decrypt(ciphertext)

        if intermediate in enc_pairs:
            key_pair = (enc_pairs[intermediate], key)
            print("K1 :", b64encode(enc_pairs[intermediate]))
            print("K2 :", b64encode(key))
            break

    return key_pair


if __name__ == "__main__":
    plaintext = b64decode(b'dSM10HSHHCMQcGXJDqf1Qg==')
    ciphertext = b64decode(b'txBRFflHBiJcLTl34+EPoA==')

    key_pair = bruteforce(plaintext, ciphertext)

    ## CHECK END RESULT
    AES_key1 = AES.new(key_pair[0], AES.MODE_ECB)
    AES_key2 = AES.new(key_pair[1], AES.MODE_ECB)
    ciphertext_decrypted = AES_key2.encrypt(AES_key1.encrypt(plaintext))
    print("Decryption status :", ciphertext_decrypted == ciphertext)
