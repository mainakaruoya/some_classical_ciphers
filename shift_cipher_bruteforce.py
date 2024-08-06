"""
This function relies on the decryption function in the `shift_cipher.py` file.

Since we don't know the exact key, but we do know that the key value range is all values modulo 26 (i.e, 0-25), the code tries all possible values in that range and outputs the results to screen. The user can then infer which is the possible original ciphertext.
"""
from shift_cipher import shiftCipherDecryption

def bruteForceAttempt(ciphertext: str) -> None:

    for possibleKey in range (0, 26):
        print(f"Possible shift/key: {possibleKey}")
        possiblePlaintext = shiftCipherDecryption(ciphertext, possibleKey)
        print(f"Possible plaintext value:\n{possiblePlaintext}\n")

if __name__ == '__main__':
    print("---SHIFT CIPHER: BRUTE-FORCE ATTEMPT---\n")
    ciphertextToCrack = input("Enter the ciphertext to crack:\n")
    bruteForceAttempt(ciphertextToCrack)