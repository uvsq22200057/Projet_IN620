# Makefile for running a Python script

# Variables
#SHELL := /bin/bash
SHELL := bash
PYTHON := python3
SCRIPT_TURING := src/Turing.py
SCRIPT_AUTOMATE := src/Automate.py
SCRIPT_SIMULATION := src/Simulation.py
ZIP_FILE := ND_GAUTEUR_Mathilde-CRAMETTE_Noe.zip
ZIP_DIR := ND_GAUTEUR_Mathilde-CRAMETTE_Noe

# Default target
run:
	@echo "Quel programme voulez-vous lancer ? (0 pour Automate cellulaire, 1 pour Turing, 2 pour simuler un code Turing avec un automate cellulaire)"
	@read choice; \
	if [ $$choice = 0 ]; then \
		echo "Fichiers disponibles dans automata/ :"; \
		files=($$(ls automata/*.txt)); \
		for i in $$(seq 0 $$(( $${#files[@]} - 1 ))); do \
			name=$$(basename $${files[$$i]}); \
			echo "[$$i] $$name"; \
		done; \
		echo "Tapez le numéro du fichier à utiliser :"; \
		read index; \
		file=$${files[$$index]}; \
		echo "Quels modes voulez-vous utiliser pour arrêter le calcul ?"; \
		echo "Nombre de pas de calcul (entre 1 et 1000)"; \
		read steps; \
		echo "Après une transition particulière"; \
		echo "0 pour (0,0,0), 1 pour (0,1,0), 2 pour (1,0,0), 3 pour (1,1,0), 4 pour (0,0,1), 5 pour (0,1,1), 6 pour (1,0,1), 7 pour (1,1,1)"; \
		echo "Si aucune transition n'est choisi, tapez 8"; \
		read transition; \
		echo "S'arrêter si le système est stable (0 pour False ou 1 pour True)"; \
		read stable; \
		echo "Sur quelle configuration initiale l'automate doit-il tourner ?"; \
		read config; \
		echo "Votre choix : $$steps, $$transition, $$stable, $$config" ; \
		$(PYTHON) $(SCRIPT_AUTOMATE) $$file $$steps $$transition $$stable $$config; \
	elif [ $$choice = 1 ]; then \
		echo "Fichiers disponibles dans turing/ :"; \
		files=($$(ls turing/*.txt)); \
		for i in $$(seq 0 $$(( $${#files[@]} - 1 ))); do \
			name=$$(basename $${files[$$i]}); \
			echo "[$$i] $$name"; \
		done; \
		echo "Tapez le numéro du fichier à utiliser :"; \
		read index; \
		file=$${files[$$index]}; \
		echo "Sur quel mot la machine doit-elle tourner ?"; \
		read word; \
		$(PYTHON) $(SCRIPT_TURING) $$file $$word; \
	elif [ $$choice = 2 ]; then \
		echo "Fichiers disponibles dans turing/ :"; \
		files=($$(ls turing/*.txt)); \
		for i in $$(seq 0 $$(( $${#files[@]} - 1 ))); do \
			name=$$(basename $${files[$$i]}); \
			echo "[$$i] $$name"; \
		done; \
		echo "Tapez le numéro du fichier à utiliser :"; \
		read index; \
		file=$${files[$$index]}; \
		echo "Sur quel mot la machine doit-elle tourner ?"; \
		read word; \
		$(PYTHON) $(SCRIPT_SIMULATION) $$file $$word; \
	else \
		echo "Choix invalide. Veuillez répondre 0 pour Automate cellulaire, 1 pour Turing ou 2 pour simuler Turing sur automate cellulaire."; \
fi; \
echo "Fin de l'exécution."

# Clean target (optional, if you have temporary files to remove)
clean:
	rm -rf __pycache__

# Create ZIP archive target
zip: clean
	@echo "Creating ZIP archive"
	mkdir -p $(ZIP_DIR)
	cp -r src $(ZIP_DIR)/
	cp -r automata $(ZIP_DIR)/
	cp -r turing $(ZIP_DIR)/
	cp -f README.md $(ZIP_DIR)/
	cp -f IN620_DM_2025.pdf $(ZIP_DIR)/ 2>/dev/null || true
	cp -f Makefile $(ZIP_DIR)/
	zip -r $(ZIP_FILE) $(ZIP_DIR)
	rm -rf $(ZIP_DIR)

# Help target
help:	
	@echo "Available targets:"
	@echo "  run   - Run the Python script"
	@echo "  zip   - Create a ZIP archive of the project"
	@echo "  clean - Remove temporary files"