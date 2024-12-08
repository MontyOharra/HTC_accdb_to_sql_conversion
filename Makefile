                            # UTCS
PYTHON   := python
PIP      := pip3
PYLINT   := pylint3
COVERAGE := coverage
PYDOC    := pydoc3
AUTOPEP8 := autopep8


test: htcConversionTest.py
	$(PYTHON) -m ./htcConversionTest.py > htcConversionTest.log 2>&1

clean: htcConversionTest.py htcConversionFull.py
	rm -f ./htcConversionTest.log

full: htcConversionFull.py
	$(PYTHON) ./htcConversionFull.py > htcConversion.log 2>&1
