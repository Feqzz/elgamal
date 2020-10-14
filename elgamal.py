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
		tempList = []
		tempValue = ord(message[i])
		print("TempValue: ", tempValue)
		for j, k in enumerate(message[(i+1):len(message)], 1):
			concatenateValue = int(str(tempValue) + str(ord(k)))

			if concatenateValue > prime:
				break
			else:
				tempValue = concatenateValue
				print("adding to index: ", 1)
				i += 1
			
			print(concatenateValue)

		print("adding: ", tempValue)
		retList.append(tempValue)

		i += 1


	print("Printing blocks list")
	for i in retList:
		print(i)

	print("Printing orignal message")
	for i in message:
		print(ord(i))

def compressMessage(message):
	retStr = ""
	for i in message:
		retStr += str(ord(i) - 22)

	print(retStr)
	return retStr



def elgamal():
	print("")


		

def main():

	stringMessage = "HELLO"
	#compressedMessage = compressMessage(stringMessage)




	prime = 999983
	q = prime - 1
	generator = generateLowestAcceptableGenerator(prime)

	constructBlocks(stringMessage, prime)




	message = 800000

	x = random.randint(1, q)
	h = fastModularExponentiation(generator, x, prime)

	y = random.randint(1, q)

	s = fastModularExponentiation(h, y, prime)

	c1 = fastModularExponentiation(generator, y, prime)

	c2 = fastModularExponentiation((message * s), 1, prime)

	ss = fastModularExponentiation(c1, x, prime)

	invs = fastModularExponentiation(c1, (q - x), prime)

	mm = fastModularExponentiation((c2 * invs), 1, prime)

	print("Prime: ", prime)
	print("Generator: ", generator)
	print("Message: ", message)
	print("Decrypted messsage: ", mm)

if __name__ == '__main__':
	main()