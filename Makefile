# Makefile for running a Python script

# Variables
PYTHON := python3
SCRIPT := src/main.py
ZIP_FILE := ND_GAUTEUR_Mathilde-CRAMETTE_Noe.zip
ZIP_DIR := ND_GAUTEUR_Mathilde-CRAMETTE_Noe

# Default target
run:
	$(PYTHON) $(SCRIPT)

# Clean target (optional, if you have temporary files to remove)
clean:
	rm -rf __pycache__

# Create ZIP archive target
zip: clean
	@echo "Creating ZIP archive"
	mkdir -p $(ZIP_DIR)
	cp -r $(SCRIPT) Makefile README.MD automate.txt $(ZIP_DIR)/
	zip -r $(ZIP_FILE) $(ZIP_DIR)
	rm -rf $(ZIP_DIR)

# Help target
help:	
	@echo "Available targets:"
	@echo "  run   - Run the Python script"
	@echo "  zip   - Create a ZIP archive of the project"
	@echo "  clean - Remove temporary files"