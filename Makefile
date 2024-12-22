                            # UTCS
PYTHON   := python
PIP      := pip3
PYLINT   := pylint3
COVERAGE := coverage
PYDOC    := pydoc3
AUTOPEP8 := autopep8


test: htcConversionTest.py
	$(PYTHON) -u -m htcConversionTest | tee htcConversion.log

clean: htcConversionTest.py htcConversionFull.py
	rm -f ./htcConversion.log

full: htcConversionFull.py
	$(PYTHON) -u -m htcConversionFull | tee htcConversion.log

migration: htcMigrationTest.py
	$(PYTHON) -u -m htcMigrationTest | tee htcMigration.log