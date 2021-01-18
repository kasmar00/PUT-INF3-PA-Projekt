SHELL := /bin/bash
.PHONY = activate debug clean

	# bash -c "source .env/bin/activate"
	# bash --init-file <(echo "ls; pwd")
run:
	@( \
		source .env/bin/activate; \
		python3 wsgi.py; \
	)

debug:
	@echo "Running with debug variable"
	@( \
		source .env/bin/activate; \
		export FLASK_ENV=development; \
		python3 wsgi.py; \
	)

clean:
	@echo "Cleaning .pyc files"
	@py3clean .

install:
	@echo "Installing dependencies"
	@( \
		source .env/bin/activate; \
		pip install -r requirements.txt; \
	)