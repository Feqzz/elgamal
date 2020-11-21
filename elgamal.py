import random
import sys, getopt

###############################
## fastModularExponentiation ##
###############################

def fastModularExponentiation(generator, exponent, mod):
    #This function is taken from the course book. 
    x = 1
    power = generator % mod
    binaryString = bin(exponent)

    for i in binaryString[::-1]:
        if i == '1':
            x = (x * power) % mod
        power = (power * power) % mod
    return x


################
## addPadding ##
################

def addPadding(a):
    # Adds padding to the number. If the number is '3', it will be returned as '003'.
    if len(a) % 3 != 0:
        if len(a) % 3 == 1:
            return "00" + a
        else:
            return "0" + a
    else:
        return a

#####################
## constructBlocks ##
#####################


def constructBlocks(message, prime):
    # The limit is implemented so the program can encrypt every ASCII character.
    if prime < 131:
        sys.exit("Your Primenumber is less than the minimum (131).")
        
    # Initializes an empty list. It loops through the message and coverts the character to 
    # a ASCII value and adds padding. It concatenates values together until the value is larger
    # than the prime number. Then it settles for the previous value, and appends it to the list.
    # After the program have iterated through every value of the message, it returns the list.
    retList = []
    i = 0
    while i < len(message):
        tempValue = addPadding(str(ord(message[i])))
        for j, k in enumerate(message[(i+1):len(message)], 1):
            nextChar = addPadding(str(ord(k)))
            concatenateValue = tempValue + nextChar

            if int(concatenateValue) > prime:
                break
            else:
                tempValue = concatenateValue
                i += 1

        retList.append(tempValue)
        i += 1
    return retList;

#######################
## deconstructBlocks ##
#######################

def deconstructBlocks(blocks):
    # From the padding, we know that every value is 3 digits long. An empty string is
    # initialized and the loop iterates through every block, converting the ascii values
    # back to characters and appends them to the string. 
    # When the loop is finished, the string is returned.
    retString = ""
    for i in blocks:
        for j in range(int(len(str(i))/3)):
            retString += chr(int(str(i)[j*3:3*(j+1)]))

    return retString

#############
## encrypt ##
#############

def encrypt(prime, message, privateKey):
    # Follows the encryption as described in the report. The value 'y' is randomly
    # generated as 1 <= y < p.
    # The encrypted variables c1 and c2 are added to a list which at the end is returned.
    q = prime - 1
    generator = 7 

    x = privateKey
    h = fastModularExponentiation(generator, privateKey, prime)

    y = random.randint(1, q)

    s = fastModularExponentiation(h, y, prime)

    c1 = fastModularExponentiation(generator, y, prime)

    c2 = fastModularExponentiation((int(message) * s), 1, prime)

    retList = [c1, c2]

    return retList

################
## decryption ##
################

def decryption(prime, privateKey, encryptedList):
    # Follows the decryption algorithm as described in the report. It needs to use 
    # both c1 and c2 for the decryption. At the end, padding is added to the 
    # decrypted value.
    q = prime - 1
    c1 = encryptedList[0]
    c2 = encryptedList[1]
    x = privateKey

    inverse = fastModularExponentiation(c1, (q - x), prime)
    decryptedMessage = fastModularExponentiation((c2 * inverse), 1, prime)

    return addPadding(str(decryptedMessage))

def main():
    inputFile = "elgamal.py"
    printing = True
    readFromFile = True
    stringMessage = "Diskret? Dette er et lite eksempel som beviser at koden fungerer."

    if readFromFile:
        with open(inputFile, 'r') as file:
                stringMessage = file.read()

    prime = 58021664585639791181184025950440248398226136069516938232493687505822471836536824298822733710342250697739996825938232641940670857624514103125986134050997697160127301547995788468137887651823707102007839
    # Creates some blocks out of the input message.
    blocks = constructBlocks(stringMessage, prime)

    encryptedList = []
    privateKeys = []

    # For every block, a new private key is generated and stored in a list of private keys.
    # This list will become useful under decryption. The blocks are encrypted and stored in
    # a list of encrypted blocks.
    for i in blocks:
        currentPrivateKey = random.randint(1, (prime - 1))
        privateKeys.append(currentPrivateKey)
        encryptedList.append(encrypt(prime, i, currentPrivateKey))

    # For each block in the encrypted list, it is decrypted using the private keys from
    # the private keys list and the encrypted blocks from the encrypted blocks list.
    # When decryption is done, it is appended to a decrypted block list.
    decryptedList = []
    for i, j in enumerate(encryptedList, 0):
        decrypted = decryption(prime, privateKeys[i], j)
        decryptedList.append(decrypted)

    # The decrypted blocks are converted into characters.
    decryptedMessage = deconstructBlocks(decryptedList)
    
    # Just some printing, so debugging is easier.
    if stringMessage == decryptedMessage:
        print("Success!")
    else:
        print("Failed.")

    if printing:
        print("Plaintext:", stringMessage)
        print("Prime Number:", prime, "\n")
        print("Blocks: (", len(blocks), ")")
        for i in blocks:
            print(i, end = " ")
        print("\n")

        print("Encrypted Blocks:")
        for i in encryptedList:
            print(i, end = " ")
        print("\n")

        print("Decrypted Blocks:")
        for i in decryptedList:
            print(i, end = " ")
        print("\n")

        print("Decrypted Message: \n" + decryptedMessage)

if __name__ == '__main__':
    main()
