PYTHON   := python

init:
	rm -rf env venv
	python -m venv env
	source env/Scripts/activate && \
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