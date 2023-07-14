from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad
from base64 import b64encode, b64decode
import secrets
import re
import socket

"""
This function queries the server with the specific key_id to encrypt
the plaintext. It returns the IV and the ciphertext as bytes.
Example:
>>> (IV, ct) = real_oracle(44, b'Hello World!')
>>> print("IV = %s" % b64encode(IV))
IV = b'roVEA/Wt8N7Ojp1GXEdb8w=='
>>> print("ct = %s" % b64encode(ct))
ct = b'HNly5YICj5mPh1LW3SLgNw=='

You can also contact the server manually with netcat:
$ nc iict-mv330-sfa.einet.ad.eivd.ch 8000 
Welcome to USB's encryption server

Please enter the encryption key ID: 44
Please enter the message in hex to encrypt: AAAA            

Encryption successful:
Message w/ padding: aaaa0e0e0e0e0e0e0e0e0e0e0e0e0e0e
IV                : ae854403f5adf0dece8e9d465c475bf0
Ciphertext        : edfab2e3f33b97de070a6c71f3dd0e34

Bye!
"""
def real_oracle(key_id: int, plaintext: bytes, host='iict-mv330-sfa.einet.ad.eivd.ch', port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        # Wait for ID prompt
        while b'ID: ' not in s.recv(1024):
            pass
        s.sendall(str(key_id).encode('ascii') + b'\n')
        s.sendall(plaintext.hex().encode('ascii') + b'\n')
        # Read until we get b'Bye!'
        output = b''
        while b'Bye!' not in output:
            output += s.recv(1024)

        # Read the plaintext, iv and ciphertext
        output = output.decode('ascii')
        pt = re.findall(r'Message.*?: ([0-9a-fA-F]+)\n', output)
        iv = re.findall(r'IV.*?: ([0-9a-fA-F]+)\n', output)
        ct = re.findall(r'Ciphertext.*?: ([0-9a-fA-F]+)\n', output)

        # Ensure that we got exactly 3 regex matches
        if len(pt) + len(iv) + len(ct) != 3:
            raise Exception("Failed to get ciphertext")

        return bytes.fromhex(iv[0]), bytes.fromhex(ct[0])


"""
Incrémente de un la valeur de l'IV passée en paramètre.
"""
def increaseIV(ctr):
    ctr_int = int.from_bytes(ctr, "big")
    ctr_int += 1
    return int(ctr_int).to_bytes(AES.block_size, byteorder="big")


"""
Effectue une requête à l'oracle pour obtenir l'IV courrant et l'incrémente de un pour obtenir l'IV suivant.
"""
def getNextIV(MY_KEY_ID):

    (IV, cipher) = real_oracle(MY_KEY_ID, b"LACRYPTOCESTRIGOLOMAISLACRYPTOCESTPASDELARIGOLADE")
    return increaseIV(IV)


"""
Permet de bruteforce un message en effectuant des requêtes à l'oracle. La structure du message clair doit être connue, ainsi que l'IV utilisé pour chiffrer le message.
"""
def breaker(MY_KEY_ID, ct, iv):

    ct = b64decode(ct)
    IV = b64decode(iv)

    # Récupère la prochaine valeur de l'IV utilisée par l'oracle
    next_IV = getNextIV(MY_KEY_ID)

    # Bruteforce toutes les valeurs possibles du salaire.
    for i in range(0, 3000):

        m = b"Le salaire journalier du dirigeant USB est de " + str(i).encode() + b" CHF"

        """
        Le XOR avec l'IV de référence permet d'avoir la même valeur que celle utilisée par l'oracle pour chiffrer le message de référence.
        Le XOR avec l'IV suivant permet d'annuler le XOR qui va être effectué par l'oracle.
        """
        m = strxor(strxor(next_IV, IV), m[0:16]) + m[16:]

        (_, cipher) = real_oracle(MY_KEY_ID, m)
        next_IV = increaseIV(next_IV)
        if cipher == ct:
            print(i)
            break

if __name__ == "__main__":

    ID = 54
    IV = b'09yBiiuqcuRPgr3akKjqRw=='
    ct = b'C/UHV2UP1LnSfKstbGF2fr3M2/nDtvZ6CmuyYSOEWD2GgBfEg15mezX66NBhoQdPio/hD/KevEVtBoYjvQG3Gw=='

    breaker(ID, ct, IV)


