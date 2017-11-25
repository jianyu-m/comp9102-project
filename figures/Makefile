GNUPLOT := `which gnuplot`
EPS2PDF := `which epstopdf`

PYTHON := python3
EPSFILES = $(wildcard *.eps)
PYFILES = $(wildcard *.py)
PYPDFS = $(PYFILES:%.py=%.ppy)
PDFFILES = $(EPSFILES:%.eps=%.pdf)

all: $(PDFFILES) $(PYPDFS) Makefile

%.pdf: %.eps
	$(EPS2PDF) $*.eps

%.ppy: %.py
	$(PYTHON) $*.py > $*.ppy

clean:
	@rm -f *.pdf
	@rm -f *.ppy
