
all: paper.pdf

paper.pdf: *.tex
		pdflatex paper.tex > paper.log
		bibtex paper > paper.log
		pdflatex paper.tex paper.bbl > paper.log
		pdflatex paper.tex paper.bbl > paper.log

clean:
	rm *.log *.bbl *.aux *.pdf *.blg
