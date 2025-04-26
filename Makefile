# Makefile for running a Python script

# Variables
PYTHON := python3
SCRIPT_TURING := src/Turing.py
SCRIPT_AUTOMATE := src/Automate.py
ZIP_FILE := ND_GAUTEUR_Mathilde-CRAMETTE_Noe.zip
ZIP_DIR := ND_GAUTEUR_Mathilde-CRAMETTE_Noe

# Default target
run:
	@echo "Quel programme voulez-vous lancer ? (0 pour Automate cellulaire ou 1 pour Turing)"
	@read choice; \
	if [ $$choice = 0 ]; then \
		echo "Fichiers disponibles dans automata/ :"; \
		ls automata/*.txt | sed 's|automata/||g'; \
		echo "Quel fichier voulez-vous utiliser ?"; \
		read file; \
		echo "Quels modes voulez-vous utiliser pour arrêter le calcul ?"; \
		echo "Nombre de pas de calcul (entre 1 et 1000)"; \
		read steps; \
		echo "Après une transition particulière"; \
		echo "0 pour (0,0,0), 1 pour (0,1,0), 2 pour (1,0,0), 3 pour (1,1,0), 4 pour (0,0,1), 5 pour (0,1,1), 6 pour (1,0,1), 7 pour (1,1,1)"; \
		echo "Si aucune transition n'est choisi, tapez 8"; \
		read transition; \
		echo "S'arrêter si le système est stable (0 pour False ou 1 pour True)"; \
		read stable; \
		echo "Votre choix : $$steps, $$transition, $$stable" ; \
		$(PYTHON) $(SCRIPT_AUTOMATE) automata/$$file $$steps $$transition $$stable; \
	elif [ $$choice = 1 ]; then \
		echo "Fichiers disponibles dans turing/ :"; \
		ls turing/*.txt | sed 's|turing/||g'; \
		echo "Quel fichier voulez-vous utiliser ?"; \
		read file; \
		$(PYTHON) $(SCRIPT_TURING) turing/$$file; \
	else \
		echo "Choix invalide. Veuillez répondre 0 pour Automate cellulaire ou 1 pour Turing."; \
fi; \
echo "Fin de l'exécution."

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