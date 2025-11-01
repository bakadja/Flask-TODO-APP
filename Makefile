.PHONY: venv install-dev test

venv:
	python3 -m venv .venv

install-dev: venv
	. .venv/bin/activate && python -m pip install --upgrade pip && python -m pip install -r requirements-dev.txt

test:
	@if [ -d .venv ]; then \
		. .venv/bin/activate && python -m pytest $(ARGS); \
	else \
		python3 -m pytest $(ARGS); \
	fi
