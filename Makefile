test: htcConversionTest.py
	python ./htcConversionTest.py > htcConversionTest.log 2>&1
	type htcConversionTest.log

clean: htcConversionTest.py htcConversionFull.py
	rm -r htcConversionTest.log
	rm -r htcConversion.log

htcConversion: htcConversionFull.py
	python -m ./htcConversionFull.py > htcConversion.log 2>&1
