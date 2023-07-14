# IMPORTANT
# IL EST PRIMORDIAL DE NE PAS CHANGER LA SIGNATURE DES FONCTIONS
# SINON LES CORRECTIONS RISQUENT DE NE PAS FONCTIONNER CORRECTEMENT

import unidecode
from statistics import mean
import math

NB_LETTERS = 26
LETTER_A = ord('A')
MAX_KEY_SIZE = 20


def caesar_encrypt(text, key):
    """
    Parameters
    ----------
    text: the plaintext to encrypt
    key: the shift which is a number

    Returns
    -------
    the ciphertext of <text> encrypted with Caesar under key <key>
    """

    text = text_cleaner(text)

    if not text or not key:
        return text

    # Implements the Caesar encryption by adding the key to each letter
    return ''.join([chr((ord(letter) - LETTER_A + key) % NB_LETTERS + LETTER_A) for letter in text])


def caesar_decrypt(text, key):
    """
    Parameters
    ----------
    text: the ciphertext to decrypt
    key: the shift which is a number

    Returns
    -------
    the plaintext of <text> decrypted with Caesar under key <key>
    """

    text = text_cleaner(text)

    if not text or not key:
        return text

    # Implements the Caesar decryption by subtracting the key to each letter
    return ''.join([chr((ord(letter) - LETTER_A - key) % NB_LETTERS + LETTER_A) for letter in text])


def freq_analysis(text):
    """
    Parameters
    ----------
    text: the text to analyse

    Returns
    -------
    list
        the frequencies of every letter (a-z) in the text.

    """

    text = text_cleaner(text)

    if not text:
        return [0] * NB_LETTERS

    # Computes the frequencies of each letter in the text
    return [letter / len(text) for letter in [text.count(chr(LETTER_A + letter_index)) for letter_index in range(0, NB_LETTERS)]]


def caesar_break(text, ref_freq):
    """
    Parameters
    ----------
    text: the ciphertext to break
    ref_freq: the output of the freq_analysis function on a reference text

    Returns
    -------
    a number corresponding to the caesar key
    """

    text = text_cleaner(text)

    if not text or not ref_freq:
        return 0

    min_key = 0
    min_dist = float('inf')

    freqs = freq_analysis(caesar_decrypt(text, 0))

    # Computes the distance between the frequencies of the text and the reference frequencies for each possible key
    for key in range(0, NB_LETTERS):
        dist = sum(pow(freqs[(i + key) % NB_LETTERS] - ref_freq[i], 2) / ref_freq[i] for i in range(len(list(freqs))))

        if dist < min_dist:
            min_dist = dist
            min_key = key

    return min_key


def vigenere_encrypt(text, key):
    """
    Parameters
    ----------
    text: the plaintext to encrypt
    key: the keyword used in Vigenere (e.g. "pass")

    Returns
    -------
    the ciphertext of <text> encrypted with Vigenere under key <key>
    """

    text = text_cleaner(text)

    if not text or not key:
        return text

    # Implements the Vigenere encryption by adding the key to each text letter by letter
    return ''.join([chr((ord(letter) - LETTER_A + ord(key[index % len(key)]) - LETTER_A) % NB_LETTERS + LETTER_A) for index, letter in enumerate(text)])


def vigenere_decrypt(text, key):
    """
    Parameters
    ----------
    text: the ciphertext to decrypt
    key: the keyword used in Vigenere (e.g. "pass")

    Returns
    -------
    the plaintext of <text> decrypted with Vigenere under key <key>
    """

    text = text_cleaner(text)

    if not text or not key:
        return text

    # Implements the Vigenere decryption by subtracting the key to each text letter by letter
    return ''.join([chr((ord(letter) - LETTER_A - ord(key[index % len(key)]) - LETTER_A) % NB_LETTERS + LETTER_A) for index, letter in enumerate(text)])


def coincidence_index(text):
    """
    Parameters
    ----------
    text: the text to analyse

    Returns
    -------
    the index of coincidence of the text
    """

    text = text_cleaner(text)

    # If the length is less than 2, the index of coincidence has no meaning
    if len(text) < 2 or not text:
        return 0

    freqs = [text.count(chr(LETTER_A + index)) for index in range(0, NB_LETTERS)]

    # Computes the index of coincidence
    sumni = 0
    for freq in freqs:
        sumni += freq * (freq - 1)
    sumni = sumni * NB_LETTERS
    sumN = sum(freqs)

    ic = sumni / (sumN * (sumN - 1))

    return ic


def vigenere_break(text, ref_freq, ref_ci):
    """
    Parameters
    ----------
    text: the ciphertext to break
    ref_freq: the output of the freq_analysis function on a reference text
    ref_ci: the output of the coincidence_index function on a reference text

    Returns
    -------
    the keyword corresponding to the encryption key used to obtain the ciphertext
    """

    text = text_cleaner(text)

    if not text or not ref_freq or not ref_ci:
        return text

    final_ics = [abs(mean([coincidence_index(text[j::i]) for j in range(i)]) - ref_ci) for i in range(1, min(MAX_KEY_SIZE + 1, len(text) + 1))]

    # Seeking the key length with the smallest distance between the index of coincidence of the text and the reference index of coincidence
    key_length = final_ics.index(min(final_ics)) + 1

    # Find the Vigenere key with the key length found previously
    key_vigenere = vigenere_letters_break(text, key_length, ref_freq)

    return key_vigenere


def vigenere_caesar_encrypt(text, vigenere_key, caesar_key):
    """
    Parameters
    ----------
    text: the plaintext to encrypt
    vigenere_key: the keyword used in Vigenere (e.g. "pass")
    caesar_key: a number corresponding to the shift used to modify the vigenere key after each use.

    Returns
    -------
    the ciphertext of <text> encrypted with improved Vigenere under keys <key_vigenere> and <key_caesar>
    """

    text = text_cleaner(text)

    if not text or not vigenere_key:
        return text

    # Uses the key_encrypt function to create the full Vigenere key then encrypts the text with it
    return vigenere_encrypt(text, key_encrypt(text, vigenere_key, caesar_key))


def vigenere_caesar_decrypt(text, vigenere_key, caesar_key):
    """
    Parameters
    ----------
    text: the plaintext to decrypt
    vigenere_key: the keyword used in Vigenere (e.g. "pass")
    caesar_key: a number corresponding to the shift used to modify the vigenere key after each use.

    Returns
    -------
    the plaintext of <text> decrypted with improved Vigenere under keys <key_vigenere> and <key_caesar>
    """

    text = text_cleaner(text)

    if not text or not vigenere_key:
        return text

    # Uses the key_encrypt function to create the full Vigenere key then decrypts the text with it
    return vigenere_decrypt(text, key_encrypt(text, vigenere_key, caesar_key))


def vigenere_caesar_break(text, ref_freq, ref_ci):
    """
    Parameters
    ----------
    text: the ciphertext to break
    ref_freq: the output of the freq_analysis function on a reference text
    ref_ci: the output of the coincidence_index function on a reference text

    Returns
    -------
    pair
        the keyword corresponding to the vigenere key used to obtain the ciphertext
        the number corresponding to the caesar key used to obtain the ciphertext
    """

    min_ics = ["CaesarDecrypted", float("inf"), 0, 0]

    # Loops through all possibilities of key length and caesar key to find the one with the smallest distance between the index of coincidence of the text and the reference index of coincidence
    # It decrypts the text block by block with the caesar key corresponding to the current iteration and then computes the index of coincidence on chunks of text
    for i in range(1, MAX_KEY_SIZE + 1):
        for j in range(NB_LETTERS):
            final_text = ''.join([caesar_decrypt(text[k:k + i], ((j * (k // i)) % NB_LETTERS)) for k in range(0, len(text), i)])
            ic = abs(mean_ic(final_text, i) - ref_ci)
            if ic < min_ics[1]:
                min_ics = [final_text, ic, j, i]

    key_caesar, key_length = min_ics[2], min_ics[3]
    key_vigenere = vigenere_letters_break(min_ics[0], key_length, ref_freq)

    return key_vigenere, key_caesar


def vigenere_letters_break(text, key_length, ref_freq):
    """
    Parameters
    ----------
    text: the ciphertext to break
    key_length: the length of the key used to encrypt the text
    ref_freq: the output of the freq_analysis function on a reference text

    Returns
    -------
    the keyword corresponding to the encryption key used to obtain the ciphertext
    """

    if not text or not ref_freq or key_length <= 0:
        return text

    key_vigenere = ""

    # Create blocks spaced by the key length and decrypt them with the caesar_break function.
    # This works because the key is repeated every key_length letters
    for m in range(key_length):
        letters = text[m::key_length]
        key_vigenere += chr(LETTER_A + caesar_break(letters, ref_freq))
    return key_vigenere


def mean_ic(text, key_length):
    """
    Parameters
    ----------
    text: the ciphertext to break
    key_length: the length of the key used to encrypt the text

    Returns
    -------
    the mean index of coincidence of the text
    """

    ics = []

    # Create blocks spaced by the key length and compute the index of coincidence of each block
    for i in range(key_length):
        block = text[i::key_length]
        ics.append(coincidence_index(block))
    return mean(ics)


def text_cleaner(text):
    """
    Parameters
    ----------
    text: the text to clean

    Returns
    -------
    the text without accents, spaces and punctuation, in uppercase
    """

    return ''.join([char for char in unidecode.unidecode(text).upper() if char.isalpha()])


def ref_values():
    """
    Returns
    -------
    pair
        the output of the freq_analysis function on the reference text
        the output of the coincidence_index function on the reference text
    """

    with open("les_miserables.txt", "r") as f:
        text = f.read()

    ref_freq = freq_analysis(text)
    ref_ci = coincidence_index(text)

    return ref_freq, ref_ci


def key_encrypt(text, vigenere_key, caesar_key):
    """
    Parameters
    ----------
    text: the text to encrypt
    vigenere_key: the keyword used in Vigenere (e.g. "pass")
    caesar_key: a number corresponding to the shift used to modify the vigenere key after each use.

    Returns
    -------
    the full Vigenere key used to encrypt the text
    """

    final_key = ""
    for i in range(math.ceil(float(len(text)) / len(vigenere_key))):
        final_key += vigenere_key
        vigenere_key = caesar_encrypt(vigenere_key, caesar_key)
    return final_key


def display(cipher, broken, key):
    print("Cipher :", cipher)
    print("Break :", broken)
    print("Key :", key)


def test(ref_freq, ref_ci):

    """
    Parameters
    ----------
    ref_freq: the output of the freq_analysis function on a reference text
    ref_ci: the output of the coincidence_index function on a reference text
    """

    caesar_keys = [i for i in range(NB_LETTERS)]
    vigenere_keys = ["A", "AA", "AAAAAAAAAA", "AAAAAAAAAAAAAAAAAAAA", "JESUISUNCLESECURISE", "ABCEFGHILMNORTSUWXYZ", "", "ALPHANUMERIQUE"]

    with open("plaintext.txt", "r") as f:
        text = f.read()

    cleaned = text_cleaner(text)
    for caesar_key in caesar_keys:
        plain = text
        caesar_cipher = caesar_encrypt(plain, caesar_key)
        caesar_key_break = caesar_break(caesar_cipher, ref_freq)
        caesar_plain_break = caesar_decrypt(caesar_cipher, caesar_key_break)
        if caesar_plain_break != cleaned:
            print(caesar_plain_break == cleaned)
    print("CAESAR FINI")

    for vigenere_key in vigenere_keys:
        plain = text
        vigenere_cipher = vigenere_encrypt(plain, vigenere_key)
        vigenere_key_break = vigenere_break(vigenere_cipher, ref_freq, ref_ci)
        vigenere_plain_break = vigenere_decrypt(vigenere_cipher, vigenere_key_break)
        if vigenere_plain_break != cleaned:
            print(vigenere_plain_break == cleaned)
    print("VIGENERE FINI")

    for caesar_key in caesar_keys:
        for vigenere_key in vigenere_keys:
            plain = text
            vigenere_caesar_cipher = vigenere_caesar_encrypt(plain, vigenere_key, caesar_key)
            vigenere_key, caesar_key = vigenere_caesar_break(vigenere_caesar_cipher, ref_freq, ref_ci)
            vigenere_caesar_plain_break = vigenere_caesar_decrypt(vigenere_caesar_cipher, vigenere_key, caesar_key)
            if vigenere_caesar_plain_break != cleaned:
                print(vigenere_caesar_plain_break == cleaned)
    print("VIGENERE CAESAR FINI")


def demonstration(ref_freq, ref_ci):

    """
    Parameters
    ----------
    ref_freq: the output of the freq_analysis function on a reference text
    ref_ci: the output of the coincidence_index function on a reference text
    """

    with open("plaintext.txt", "r") as f:
        caesar_plain = f.read()

    print("\n------------------- Caesar breaker -------------------")
    key = 5

    caesar_cipher = caesar_encrypt(caesar_plain, key)
    key = caesar_break(caesar_cipher, ref_freq)
    caesar_plain_break = caesar_decrypt(caesar_cipher, key)

    display(caesar_cipher, caesar_plain_break, key)

    # ------------------- Vigenere ------------------

    with open("vigenere.txt", "r") as f:
        vigenere_cipher = f.read()

    print("\n------------------- Vigenere breaker -------------------")

    key = vigenere_break(vigenere_cipher, ref_freq, ref_ci)
    vigenere_plain_break = vigenere_decrypt(vigenere_cipher, key)

    display(vigenere_cipher, vigenere_plain_break, key)

    # -------------- Vigenere Empowered ---------------

    print("\n------------- Vigenere Empowered breaker ---------------")

    with open("vigenereAmeliore.txt", "r") as f:
        vigenere_caesar_cipher = f.read()

    (key1, key2) = vigenere_caesar_break(vigenere_caesar_cipher, ref_freq, ref_ci)
    vigenere_caesar_plain_break = vigenere_caesar_decrypt(vigenere_caesar_cipher, key1, key2)
    display(vigenere_caesar_cipher, vigenere_caesar_plain_break, [key1, key2])


def main():
    print("Welcome to the Vigenere breaking tool")

    # True = test : test all the possible keys and edges cases (takes a lot of time)
    # False = demonstration : Demonstration of a more common case
    EXECUTION_MODE = False

    ref_freq, ref_ci = ref_values()

    if EXECUTION_MODE:
        test(ref_freq, ref_ci)
    else:
        demonstration(ref_freq, ref_ci)


if __name__ == "__main__":
    main()
