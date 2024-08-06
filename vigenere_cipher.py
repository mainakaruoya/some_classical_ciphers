# An implementation of the Vigenère cipher - did this prior to watching the EC-Council video

def vigenereEncryption(plaintext: str, key: str) -> str:
    """
    Takes the plaintext message, converts all letters into lowercase letters, ignores all spaces (to avoid revealing any information to the attacker), and then uses the key to encrypt said message.
    """

    ciphertext = ""

    lengthOfKeyToUse = len(key)

    formattedPlaintext = filter(str.isalpha, plaintext)

    for index, character in enumerate(formattedPlaintext):
        
        keyIndex = index % lengthOfKeyToUse
        
        newCharacterIndex = ord(character.lower()) - ord("a")
        shiftValue = ord(key[keyIndex].lower()) - ord("a")
        newCharacter = chr( ((newCharacterIndex + shiftValue) % 26) + ord("a") )
        ciphertext += newCharacter

    return ciphertext

def vigenereDecryption(ciphertext: str, key: str) -> str:
    """
    Inverts the encryption function, `vigenereEnryption`.
    """

    plaintext = ""

    lengthOfKeyToUse = len(key)

    for index, character in enumerate(ciphertext):
        
        keyIndex = index % lengthOfKeyToUse
        
        newCharacterIndex = ord(character.lower()) - ord("a")
        shiftValue = ord(key[keyIndex].lower()) - ord("a")
        newCharacter = chr( ((newCharacterIndex - shiftValue) % 26) + ord("a") )
        plaintext += newCharacter

    return plaintext

if __name__ == "__main__":

    print("\n---VIGENÈRE CIPHER---\n")
    plaintext = input("Enter the message to encrypt:\n")
    while plaintext == "":
        plaintext = input("Enter the message to encrypt:\n")

    keyToUse = input("Enter the key to use (no spaces):\n")

    while keyToUse.count(" ") != 0 or keyToUse == "":
        keyToUse = input("\nEnter the key to use (no spaces):\n")

    resultingCiphertext = vigenereEncryption(plaintext, keyToUse)
    print(f"\nOur ciphertext is:\n{resultingCiphertext}")

    decryptedMessage = vigenereDecryption(resultingCiphertext, keyToUse)
    print(f"\nOur decrypted ciphertext is:\n{decryptedMessage}")