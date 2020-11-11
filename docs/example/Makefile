PROG = main
CC = pdflatex

all: build #bibtex build build #clean

build:
	$(CC) $(PROG).tex

clean:
	rm -f *.aux *.log *.bbl *.blg

bibtex:
	bibtex $(PROG)
