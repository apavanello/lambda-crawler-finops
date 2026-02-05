.PHONY: setup run clean

setup:
	uv venv
	uv pip install -e .

run:
	uv run python src/crawler/main.py

clean:
	rm -rf .venv
	rm -rf __pycache__
	rm -rf src/crawler/__pycache__
