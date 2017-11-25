
all: paper.pdf

paper.pdf: *.tex figures
		pdflatex paper.tex > paper.log
		bibtex paper > paper.log
		pdflatex paper.tex paper.bbl > paper.log
		pdflatex paper.tex paper.bbl > paper.log

figures:
	make -C figures

clean:
	rm *.log *.bbl *.aux *.pdf *.blg
