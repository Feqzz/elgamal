PROG = main
NAME = elgamal
CC = g++

all: build run

build:
	$(CC) -lgmp $(PROG).cpp -o $(NAME)

run:
	./$(NAME)