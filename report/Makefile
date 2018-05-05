report:
	pdflatex main
	bibtex main
	pdflatex main
	pdflatex main

final:
	pdflatex final
	bibtex final
	pdflatex final
	pdflatex final

clean:
	rm -f *.aux
	rm -f *.bbl
	rm -f *.blg
	rm -f *.log
	rm -f *.out

clean-all: clean
	rm -f *.pdf

.PHONY: final
