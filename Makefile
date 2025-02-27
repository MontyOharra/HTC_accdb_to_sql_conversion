PYTHON   := python

init:
	rm -rf env venv
	python -m venv env
	source env/Scripts/activate && \
	pip install wheel && \
	pip install -r requirements.txt && \
	deactivate

cli-test:
	source env/Scripts/activate && \
	python -u -m applications.cli.test && \
	deactivate

cli:
	source env/Scripts/activate && \
	python -u -m applications.cli.main && \
	deactivate

clear-logs:
	rm -rf logs/*

show-errors:
	source env/Scripts/activate && \
	python -m applications.cli.show_errors && \
	deactivate