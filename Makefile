                            # UTCS
PYTHON   := python
PIP      := pip3
PYLINT   := pylint3
COVERAGE := coverage
PYDOC    := pydoc3
AUTOPEP8 := autopep8


test: htcConversionTest.py
	$(PYTHON) -u -m htcConversionTest | tee htcConversionTest.log
	cat htcConversionTest.log

clean: htcConversionTest.py htcConversionFull.py
	rm -f ./htcConversionTest.log

full: htcConversionFull.py
	$(PYTHON) ./htcConversionFull.py > htcConversion.log 2>&1
