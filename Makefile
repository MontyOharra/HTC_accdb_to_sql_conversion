test: htcConversionTest.py
	python ./htcConversionTest.py > htcConversionTest.log 2>&1
	type htcConversionTest.log

htcConversion: htcConversion.py
	python -m ./htcConversionFull.py > htcConversion.log 2>&1
