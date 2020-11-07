import random
import sys, getopt

###############################
## fastModularExponentiation ##
###############################

def fastModularExponentiation(generator, exponent, mod):
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
    if prime < 131:
        sys.exit("Your Primenumber is less than the minimum (131).")

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
    retString = ""
    for i in blocks:
        for j in range(int(len(str(i))/3)):
            retString += chr(int(str(i)[j*3:3*(j+1)]))

    return retString

#############
## encrypt ##
#############

def encrypt(prime, message, privateKey):
    q = prime - 1
    generator = 150 

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
    q = prime - 1
    c1 = encryptedList[0]
    c2 = encryptedList[1]
    x = privateKey

    inverse = fastModularExponentiation(c1, (q - x), prime)
    decryptedMessage = fastModularExponentiation((c2 * inverse), 1, prime)

    return addPadding(str(decryptedMessage))

def main():
    inputFile = ""
    outputFIle = ""
    printing = True

    #with open('main.cpp', 'r') as file:
            #stringMessage = file.read()

    stringMessage = "Diskret?"

    prime = 58021664585639791181184025950440248398226136069516938232493687505822471836536824298822733710342250697739996825938232641940670857624514103125986134050997697160127301547995788468137887651823707102007839
    blocks = constructBlocks(stringMessage, prime)

    encryptedList = []
    privateKeys = []
    for i in blocks:
        currentPrivateKey = random.randint(1, (prime - 1))
        privateKeys.append(currentPrivateKey)
        encryptedList.append(encrypt(prime, i, currentPrivateKey))

    decryptedList = []
    for i, j in enumerate(encryptedList, 0):
        decrypted = decryption(prime, privateKeys[i], j)
        decryptedList.append(decrypted)

    decryptedMessage = deconstructBlocks(decryptedList)

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
