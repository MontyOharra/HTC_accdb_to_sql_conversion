PYTHON   := python

init:
	python -m venv env
	source env/Scripts/activate && \
	pip install -r requirements.txt && \
	deactivate

migrate-testing:
	source env/Scripts/activate && \
	python -u -m applications.migrate.test && \ 
	deactivate

migrate-production:
	source env/Scripts/activate && \
	python -u -m applications.migrate.main && \ 
	deactivate

normalize-testing:
	source env/Scripts/activate && \
	python -u -m applications.normalize.test && \ 
	deactivate

normalize-production:
	source env/Scripts/activate && \
	python -u -m applications.normalize.main && \ 
	deactivate