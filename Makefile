PYTHON   := python

test: htcConversionTest.py
	$(PYTHON) -u -m htcConversionTest | tee htcConversion.log

clean: htcConversionTest.py htcConversionFull.py
	rm -f ./htcConversion.log

full: htcConversionFull.py
	$(PYTHON) -u -m htcConversionFull | tee htcConversion.log

migration-test: htcMigrationTest.py
	$(PYTHON) -u -m htcMigrationTest | tee htcMigration.log

migration-full: htcMigrationFull.py
	$(PYTHON) -u -m htcMigrationFull | tee htcMigration.log