PYTHON   := python

venv:
	python -m venv env
	source env/Scripts/activate && \
	pip install -r requirements.txt && \
	deactivate

migrate-testing:
	source env/Scripts/activate && \
	python applications/migrate/main.py && \
	deactivate

migrate-production:
	source env/Scripts/activate && \
	python applications/migrate/main.py && \
	deactivate

normalize-testing:
	source env/Scripts/activate && \
	python -u -m applications.normalize.test && \ 
	deactivate

normalize-production:
	source env/Scripts/activate && \
	python applications/normalize/main.py && \
	deactivate