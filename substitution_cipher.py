"""
A simple substitution cipher
"""
from random import randrange

alphabetToReference = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]


def generateAlphabetPermutation() -> list:

    alphabet = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]
    
    permutedLetters = []

    for _ in range(0, len(alphabet)):
        selectedLetter = alphabet.pop(randrange(0, len(alphabet)))
        permutedLetters += selectedLetter

    return permutedLetters

def substitutionCipherEncryption(plaintext: str, key: list[str]) -> str:

    ciphertext = ""

    for character in plaintext:
        if character.isalpha():
            indexValue = ord(character.lower()) - ord("a")
            newCharacter = keyToUse[indexValue]
            ciphertext += newCharacter
        else:
            continue

    return ciphertext

def substitutionCipherDecryption(ciphertext: str, key: list[str]) -> str:

    recoveredPlaintext = ""

    for character in ciphertext:
        if character.isalpha():
            indexValue = key.index(character)
            newCharacter = alphabetToReference[indexValue]
            recoveredPlaintext += newCharacter
        else:
            continue

    return recoveredPlaintext


if __name__ == "__main__":
    print("\n---SUBSTITUTION CIPHER---")
    keyToUse = generateAlphabetPermutation()

    plaintext = input("Enter the message to encrypt:\n")

    ciphertext = substitutionCipherEncryption(plaintext, keyToUse)
    print(ciphertext)
    recoveredPlaintext = substitutionCipherDecryption(ciphertext, keyToUse)
    print(recoveredPlaintext)
