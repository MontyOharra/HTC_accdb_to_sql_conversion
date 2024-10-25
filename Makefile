ifeq ($(shell uname), Darwin)          # Apple
    PYTHON   := python3
    PIP      := pip3
    PYLINT   := pylint
    COVERAGE := coverage
    PYDOC    := pydoc3
    AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Windows
    PYTHON   := python                 # on my machine it's python
    PIP      := pip3
    PYLINT   := pylint
    COVERAGE := coverage
    PYDOC    := pydoc        # on my machine it's pydoc
    AUTOPEP8 := autopep8
else                                   # UTCS
    PYTHON   := python3
    PIP      := pip3
    PYLINT   := pylint3
    COVERAGE := coverage
    PYDOC    := pydoc3
    AUTOPEP8 := autopep8
endif


test: htcConversionTest.py
	$(PYTHON) ./htcConversionTest.py > htcConversionTest.log 2>&1
	touch htcConversion.log

clean: htcConversionTest.py htcConversionFull.py
	rm -r htcConversionTest.log
	rm -r htcConversion.log

full: htcConversionFull.py
	$(PYTHON) ./htcConversionFull.py > htcConversion.log 2>&1
