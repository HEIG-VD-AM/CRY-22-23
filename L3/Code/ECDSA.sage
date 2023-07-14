from hashlib import sha256

def params():
    p256 = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
    a256 = p256 - 3
    b256 = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B

    gx = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
    gy = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5
    n = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
    E = EllipticCurve(GF(p256), [a256, b256])
    G = E(gx, gy)
    return (G, E, n)

def keyGen(G, n):
    a = ZZ.random_element(n)
    A = a*G
    return (a, A)

def fastInverse(k, n):
    return power_mod(k, n-2, n)

def H(M, n):
    return int(sha256(M).hexdigest(),16) % n


def verify(M, sig, A, G, n):
    (r, s) = sig
    s_inv = fastInverse(s, n)
    u1 = s_inv*H(M, n)
    u2 = s_inv*r
    return ((u1*G + u2*A)[0].lift() % n) == r


def sign(M, a, G, n):
    r = s = 0
    while r == 0 or s == 0:
        k = (Integers(n).random_element(n)).lift()
        R = k*G
        r = R[0].lift() % n
        s = (fastInverse(k, n)*(H(M, n) + a*r)) % n
    return (r, s)


if __name__ == "__main__":

    (G, E, n) = params()
    (a, A) = keyGen(G, n)

    # Test de a fonction de signature
    M = "Hello world!".encode('utf-8')
    sig = sign(M, a, G, n)
    print("Auto-sign and verification working :", verify(M, sig, A, G, n))

    # Signature d'un message dont on ne possède pas la clé privée
    A = E(55905830027884905354978183397537383989063544607984559106569339985682369077478, 53270761127172205119737710253883827168896592567994403790063620048303729158900)
    m = "Je dois 10000CHF à Alexandre Duc".encode('utf-8')
    print("Exploit working :", verify(m, (0,0), A, G, n))