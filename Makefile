PYTHON   := python

init:
	python -m venv env
	source env/Scripts/activate && \
	pip install -r requirements.txt && \
	deactivate

migration-test:
	source env/Scripts/activate && \
	python -u -m applications.migrate.test && \
	deactivate

migration:
	source env/Scripts/activate && \
	python -u -m applications.migrate.main && \ 
	deactivate

normalization-test:
	source env/Scripts/activate && \
	python -u -m applications.normalize.test && \ 
	deactivate

normalization:
	source env/Scripts/activate && \
	python -u -m applications.normalize.main && \ 
	deactivate