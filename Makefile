SRC_DIR = app
SRC_FILES = $(shell find $(SRC_DIR) -type f -name '*.py')
TEST_DIR = tests
TEST_FILES = $(shell find $(TEST_DIR) -type f -name '*.py')
SETUP_FILES = setup.cfg pyproject.toml
PORT ?= 8000

all: lint typecheck test

install: $(SRC_FILES)
	pip install -e .

lint: $(SRC_FILES) $(TEST_FILES)
	python -m flake8 $(SRC_DIR) $(TEST_DIR)

typecheck: $(SRC_FILES) $(TEST_FILES)
	python -m mypy $(SRC_DIR) $(TEST_DIR)

test: $(SRC_FILES) $(TEST_FILES)
	python -m pytest

serve: $(SRC_FILES)
	# Run on port 8000 if another isn't specified.
	uvicorn app.main:app --host 0.0.0.0 --port $(PORT)
