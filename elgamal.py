import random
import sys

def fastModularExponentiation(generator, exponent, mod):
	x = 1
	power = generator % mod
	binaryString = bin(exponent)

	for i in binaryString[::-1]:

		if i == '1':
			x = (x * power) % mod

		power = (power * power) % mod;

	return x

def generateLowestAcceptableGenerator(prime):
	i = 1
	while i < prime:
		rand = i
		exp = 1
		next = rand % prime

		while next != 1:
			next = (next * rand) % prime
			exp += 1

		if (exp == (prime -1)):
			return rand

		i += 1

	return -1

def constructBlocks(message, prime):
	if prime < 131:
		sys.exit("Your Primenumber is less than the minimum (131).")

	retList = []

	i = 0
	while i < len(message):
		#print("index: ", i)
		tempValue = ord(message[i])
		for j, k in enumerate(message[(i+1):len(message)], 1):
			concatenateValue = int(str(tempValue) + str(ord(k)))

			if concatenateValue > prime:
				break
			else:
				tempValue = concatenateValue
				i += 1
			

		retList.append(tempValue)

		i += 1

	return retList;

def deconstructBlocks(blocks):
	print("hello")

def compressMessage(message):
	retStr = ""
	for i in message:
		retStr += str(ord(i) - 22)

	print(retStr)
	return retStr



def elgamal(prime, message, privateKey):
	q = prime - 1
	generator = generateLowestAcceptableGenerator(prime)

	x = privateKey
	h = fastModularExponentiation(generator, x, prime)

	y = random.randint(1, q)

	s = fastModularExponentiation(h, y, prime)

	c1 = fastModularExponentiation(generator, y, prime)

	c2 = fastModularExponentiation((message * s), 1, prime)

	ss = fastModularExponentiation(c1, x, prime)

	invs = fastModularExponentiation(c1, (q - x), prime)

	mm = fastModularExponentiation((c2 * invs), 1, prime)

	#print("c1: ", c1)
	#print("c2: ", c2)

	#print("Prime: ", prime)
	#print("Generator: ", generator)
	#print("Message: ", message)
	#print("Decrypted messsage: ", mm)

	retList = [c1, c2]

	#return int(str(c1) + str(c2))
	return retList

def decryption(prime, privateKey, encryptedList):
	q = prime - 1
	c1 = encryptedList[0]
	c2 = encryptedList[1]
	x = privateKey

	invs = fastModularExponentiation(c1, (q - x), prime)

	mm = fastModularExponentiation((c2 * invs), 1, prime)

	return mm


		

def main():

	stringMessage = "HELLO"
	#compressedMessage = compressMessage(stringMessage)




	prime = 9923
	

	blocks = constructBlocks(stringMessage, prime)

	print("Plaintext:", stringMessage)
	print("Blocks: (", len(blocks), ")")
	for i in blocks:
		print(i, end = " ")
	print("\n")


	encryptedList = []
	privateKeys = []
	for i in blocks:
		currentPrivateKey = random.randint(1, (prime - 1))
		privateKeys.append(currentPrivateKey)
		encryptedList.append(elgamal(prime, i, currentPrivateKey))

	print("Encrypted Blocks:")
	for i in encryptedList:
		print(i, end = " ")
	print("\n")

	print("Decrypted Blocks:")
	decryptedList = []
	for i, j in enumerate(encryptedList, 0):
		decrypted = decryption(prime, privateKeys[i], j)
		decryptedList.append(decrypted)
		print(decrypted, end = " ")
	print("\n")
	


	

if __name__ == '__main__':
	main()