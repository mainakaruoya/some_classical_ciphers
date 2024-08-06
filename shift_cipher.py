"""
This script implements the shift cipher as two separate functions - the forward/encrypting function, and the reverse/decrypting function.

When our shift is `3`, it is the Caesar cipher; when the shift is `13`, we get the ROT13 cipher.
"""
# The encryption function takes the message to shift, as well as the shift for the messages
# The ord() function converts a single character to its equivalent number
# The chr() function converts a number to its equivalent character.
# Since we are working with the alphabet (a..z) and (A..Z), a/A count as the starting index. That means that all our indices must be mod 26, since the alphabet only has 26 letters.
def shiftCipherEncryption(plaintext: str, shiftValue: int) -> str:
    
    ciphertext = ""

    for character in plaintext:
        if character.isupper():
            characterIndex = ord(character) - ord("A")
            newCharacter = chr( (characterIndex + shiftValue) % 26 + ord("A") )
            ciphertext += newCharacter

        elif character.islower():
            characterIndex = ord(character) - ord("a")
            newCharacter = chr( (characterIndex + shiftValue) % 26 + ord("a") )
            ciphertext += newCharacter

        else:
            ciphertext += character

    return ciphertext


# The decryption function: requires the same shift as the encryption function as above
def shiftCipherDecryption(ciphertext: str, shiftValue: int) -> str:
    
    plaintext = ""

    for character in ciphertext:
        if character.isupper():
            characterIndex = ord(character) - ord("A")
            newCharacter = chr( (characterIndex - shiftValue) % 26 + ord("A") )
            plaintext += newCharacter

        elif character.islower():
            characterIndex = ord(character) - ord("a")
            newCharacter = chr( (characterIndex - shiftValue) % 26 + ord("a") )
            plaintext += newCharacter

        else:
            plaintext += character

    return plaintext

if __name__ == '__main__':
    print("---SHIFT CIPHER---\n")
    # The while loops are meant to enforce certain conditions
    # 1. That our plaintext is not blank
    # 2. That the shift entered by the user is not larger than 26
    plaintextToUse = str()
    while len(plaintextToUse) < 1:
        plaintextToUse = input("Enter the plaintext to be encrypted:\n")

    shiftKey = int(input("Enter the shift (a number between 0-25):\n"))
    while shiftKey > 26:
        shiftKey = int(input("Enter the shift (a number between 0-25):\n"))

    print(f"\nOur plaintext is:\n{plaintextToUse}\n")
    print(f"Our selected shift is:\n{shiftKey}\n")
    if shiftKey == 3:
        print("Congratulations! This is now a Caesar cipher.\n")
    if shiftKey == 13:
        print("Congratulations! This is now a ROT13 cipher.\n")

    ourCiphertext = shiftCipherEncryption(plaintextToUse, shiftKey)
    print(f"Our ciphertext is:\n{ourCiphertext}\n")

    decryptedPlaintext = shiftCipherDecryption(ourCiphertext, shiftKey)
    print(f"Our decrypted plaintext is:\n{decryptedPlaintext}")


