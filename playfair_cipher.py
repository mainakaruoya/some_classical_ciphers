"""
An implementation of the Playfair cipher. This version follows Keith Martin, _Everyday Cryptography,_ 2nd Edition (2017), pp. 65-68
"""
from itertools import zip_longest
from re import findall

def findDuplicateLetters(pairsOfLetters: str, letterToInsert="q") -> str:
    """
    This function serves to preprocess the plaintext by splitting any pairs of duplicate letters - e.g., aa, bb, cc, dd, etc.
    It inserts the letter `q`, by default, when splitting letters.
    """

    # The regex looks for any alphabet letter (\w) that is repeated twice (\2)
    consecutiveLetters = findall(r'((\w)\2)', pairsOfLetters)

    listToReturn = pairsOfLetters

    for entry, _ in consecutiveLetters:

        index = listToReturn.find(entry)
        # 'q' is the letter we add in between duplicate letters; could be any other letter, really - but preferrably one that isn't frequently used
        listToReturn = listToReturn[:index + 1] + letterToInsert + listToReturn[index + 1:]
    
    # In principle, this is meant to find any newly-created consecutive letters
    newConsecutiveLetters = findall(r'((\w)\2)', listToReturn)
    while len(newConsecutiveLetters) > 0:
        findDuplicateLetters(listToReturn, letterToInsert="z")
    
    return listToReturn


def preprocessPlaintext(plaintext: str) -> list:
    """
    This function preprocesses the plaintext in the following way:
    1. We disregard spaces and numbers, leaving only characters of the (English) alphabet;
    2. We replace all `J`'s with `I`'s;
    3. We split all consecutive letters - e.g., `aa`, `bb`, `cc`, `dd`, etc. - by adding the letter `q` in between them - the `findDuplicateLetters` function;
    4. We dice up the resulting string into pairs, and if we have an odd number of characters, we add a `q` at the last character.
    """

    stringWithLettersOnly = ""
    newStringToUse = ""

    for character in plaintext:
        if character.isalpha():
            stringWithLettersOnly += character.lower()

    plaintextWithJsReplaced = stringWithLettersOnly.replace("j", "i")

    # This section handles the case where our string ends with q, and has an odd length - it prevents the string from appending q, which would be a problem
    if len(plaintextWithJsReplaced) % 2 == 1 and plaintextWithJsReplaced[-1] == "q":
        newStringToUse = plaintextWithJsReplaced + "z"
    else:
        newStringToUse = plaintextWithJsReplaced

    noConsecutiveLetters = findDuplicateLetters(newStringToUse)

    pairsOfLetters = [
        i + j for i, j in zip_longest(noConsecutiveLetters[::2], noConsecutiveLetters[1::2], fillvalue="q")
        ]
    
    return pairsOfLetters


def createKey(keywordToUse: str) -> list:
    """
    This is the function that generates our key for us, based on the keyword that the user supplies.
    """

    # Since the Playfair square uses 25 letters, we will eventually pop 'j' from this list
    alphabet = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
        ]
    
    # alphabetLength = int(len(alphabet) / 5)
    
    keyToReturn = []

    keyWithLettersReplaced = keywordToUse.lower().replace("j", "i")
    uniqueLetters = "".join(dict.fromkeys(keyWithLettersReplaced))
    
    for character in uniqueLetters:
        alphabet.remove(character)

    newCharacters = list(uniqueLetters) + alphabet

    return newCharacters


def playfairCipherEncryption(message: list, keyToUse: list) -> list:
    """
    This is the function that encrypts our text.
    """
    ciphertext = []

    for letterPair in message:
        firstLetter, secondLetter = letterPair
        indexOfFirstLetter = keyToUse.index(firstLetter)
        indexOfSecondLetter = keyToUse.index(secondLetter)
        isOnSameColumn = abs(indexOfFirstLetter - indexOfSecondLetter) % 5 == 0
        isOnSameRow = (indexOfFirstLetter% 5) == (indexOfSecondLetter % 5)

        # This condition checks if the two elements in the pair are in the same column, and shifts them to the next row.
        # This guarantees wrapping around for a given column
        if isOnSameColumn:
            newFirstLetter = keyToUse[(indexOfFirstLetter + 5) % 25]
            newSecondLetter = keyToUse[(indexOfSecondLetter + 5) % 25]
            valueToReturn = newFirstLetter + newSecondLetter
            ciphertext.append(valueToReturn)
            valueToReturn = ""

        # This condition checks if the bigram letters lie in the same row, and shifts them to the right
        # This ensures that the values wrap around in a given row
        elif isOnSameRow:
            rowCeiling, _ = divmod(indexOfFirstLetter, 5)
            newFirstLetterIndex = rowCeiling * 5 + ((indexOfFirstLetter + 1) % 5)
            newSecondLetterIndex = rowCeiling * 5 + ((indexOfSecondLetter + 1) % 5)
            newFirstLetter = keyToUse[newFirstLetterIndex]
            newSecondLetter = keyToUse[newSecondLetterIndex]
            valueToReturn = newFirstLetter + newSecondLetter
            ciphertext.append(valueToReturn)
            valueToReturn = ""

        # This handles all other possible combinations - where the letters aren't on the same row or column
        else:
            firstLetterRow, firstLetterColumn = divmod(indexOfFirstLetter, 5)
            secondLetterRow, secondLetterColumn = divmod(indexOfSecondLetter, 5)
            newFirstLetterIndex = (5 * firstLetterRow) + secondLetterColumn
            newSecondLetterIndex = (5 * secondLetterRow) + firstLetterColumn
            newFirstLetter = keyToUse[newFirstLetterIndex]
            newSecondLetter = keyToUse[newSecondLetterIndex]
            valueToReturn = newFirstLetter + newSecondLetter
            ciphertext.append(valueToReturn)
            valueToReturn = ""
    
    return ciphertext


def playfairCipherDecryption(message: list, keyToUse: list) -> list:
    """
    This is the function that decrypts our text.
    """
    recoveredPlaintext = []

    for letterPair in message:
        firstLetter, secondLetter = letterPair
        indexOfFirstLetter = keyToUse.index(firstLetter)
        indexOfSecondLetter = keyToUse.index(secondLetter)
        isOnSameColumn = abs(indexOfFirstLetter - indexOfSecondLetter) % 5 == 0
        isOnSameRow = (indexOfFirstLetter% 5) == (indexOfSecondLetter % 5)

        # This condition checks if the two elements in the pair are in the same column, and shifts them to the next row.
        # This guarantees wrapping around for a given column
        # To decrypt, we remove the column shift value (-5)
        if isOnSameColumn:
            newFirstLetter = keyToUse[(indexOfFirstLetter - 5) % 25]
            newSecondLetter = keyToUse[(indexOfSecondLetter - 5) % 25]
            valueToReturn = newFirstLetter + newSecondLetter
            recoveredPlaintext.append(valueToReturn)
            valueToReturn = ""

        # This condition checks if the bigram letters lie in the same row, and shifts them to the right
        # This ensures that the values wrap around in a given row
        # To decrypt, we subtract 1 so that we return to the original one
        elif isOnSameRow:
            rowCeiling, _ = divmod(indexOfFirstLetter, 5)
            newFirstLetterIndex = rowCeiling * 5 + ((indexOfFirstLetter - 1) % 5)
            newSecondLetterIndex = rowCeiling * 5 + ((indexOfSecondLetter - 1) % 5)
            newFirstLetter = keyToUse[newFirstLetterIndex]
            newSecondLetter = keyToUse[newSecondLetterIndex]
            valueToReturn = newFirstLetter + newSecondLetter
            recoveredPlaintext.append(valueToReturn)
            valueToReturn = ""

        # This handles all other possible combinations - where the letters aren't on the same row or column
        else:
            firstLetterRow, firstLetterColumn = divmod(indexOfFirstLetter, 5)
            secondLetterRow, secondLetterColumn = divmod(indexOfSecondLetter, 5)
            newFirstLetterIndex = (5 * firstLetterRow) + secondLetterColumn
            newSecondLetterIndex = (5 * secondLetterRow) + firstLetterColumn
            newFirstLetter = keyToUse[newFirstLetterIndex]
            newSecondLetter = keyToUse[newSecondLetterIndex]
            valueToReturn = newFirstLetter + newSecondLetter
            recoveredPlaintext.append(valueToReturn)
            valueToReturn = ""
    
    return "".join(recoveredPlaintext).upper()

if __name__ == "__main__":
    # Get message to encrypt from user
    plaintext = input("Enter the message to encrypt (only letters, no numbers or special characters):\n")

    # Get the keyword to use. This is slightly different from the variant used in Martin, 2017
    keywordToUse = input("Enter the keyword to use (no spaces, only small or capital letters):\n")

    while keywordToUse.isalpha() is False:
        keywordToUse = input("Enter the keyword to use (no spaces, only small or capital letters):\n")

    preprocessedPlaintext = preprocessPlaintext(plaintext)

    # Generate key using the keyword supplied by the user
    createdKey = createKey(keywordToUse)

    # Encrypt the message by applying the Playfair Cipher for encryption, then print it out
    ciphertext = playfairCipherEncryption(preprocessedPlaintext, createdKey)
    print(f"Our ciphertext is:\n>>>\t{"".join(ciphertext).upper()}\n")

    # Decrypt the message by applying the inverse of the Playfair Cipher, then print it out
    recoveredPlaintext = playfairCipherDecryption(ciphertext, createdKey)
    print(f"Our recovered plaintext (still with the filler letters) is:\n>>>\t{recoveredPlaintext}\n")