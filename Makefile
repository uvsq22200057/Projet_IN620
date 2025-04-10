# Makefile for running a Python script

# Variables
PYTHON := python3
SCRIPT := src/main.py

# Default target
run:
	$(PYTHON) $(SCRIPT)

# Clean target (optional, if you have temporary files to remove)
clean:
	rm -rf __pycache__

# Help target
help:
	@echo "Available targets:"
	@echo "  run   - Run the Python script"
	@echo "  clean - Remove temporary files"