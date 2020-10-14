#include <iostream>
#include <bitset>
#include <stdlib.h> 
#include <random>
#include <gmp.h>

int fastModularExponentiation(int g, int exp, int m)
{
	int x = 1;
	int power = g % m;
	std::string str = std::bitset<8>(exp).to_string();

	//std::cout << str << std::endl;

	for (int i = (str.length() - 1); i >= 0; i--)
	{
		if (str[i] == '1')
		{
			x = (x * power) % m;
			//std::cout << "x (" << i << ") " << x << std::endl;
		}
		power = (power*power) % m;
	}
	return x;
}

int generateLowestAcceptableGenerator(const int prime)
{
	for (int i = 1; i < prime; i++)
	{
		int rand = i;
		int exp = 1;
		int next = rand % prime;

		while (next != 1)
		{
			next = (next * rand) % prime;
			//std::cout << next << std::endl;
			exp++;
		}

		if (exp == (prime - 1))
		{
			return rand;
		}

	}
	return -1;
}

int main(int args, char *argv[])
{
	//int prime = 7
	static const int q = 73;
	static const int g = 5;
	static const int m = 69;

	std::random_device seeder;
	std::mt19937 engine(seeder());
	std::uniform_int_distribution<int> gen(1, (q - 1));

	int x = 4; gen(engine);

	int h = fastModularExponentiation(g, x, q);

	std::cout << generateLowestAcceptableGenerator(q) << std::endl;
	

	int y = 4; gen(engine);

	int s = fastModularExponentiation(h, y, q);

	int c1 = fastModularExponentiation(g, y, q);

	int c2 = fastModularExponentiation((m * s), 1, q);

	int ss = fastModularExponentiation(c1, x, q);

	std::cout << c1 << std::endl;

	int invs = fastModularExponentiation(c1, ((q-1) - x), q);

	int mm = fastModularExponentiation((c2 * invs), 1, q);

	std::cout << "Prime: " << q << std::endl;
	std::cout << "Generator: " << g << std::endl;
	std::cout << "Message: " << m << std::endl;
	std::cout << "Decrypted Message: " << mm << std::endl;
	std::cout << "eea: " << fastModularExponentiation((c2 * -482), 1, q) << std::endl;

	return 0;
}