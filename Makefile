# Variables para facilitar cambios futuros
PYTHON = python
PIP = pip
BUILD_DIR = build
DIST_DIR = dist

.PHONY: clean build upload-test upload

# 1. Limpieza usando un "One-Liner" de Python
# Sustituye a tu antigua clase CleanCommand
clean:
	@echo "Cleaning up..."
	$(PYTHON) -c "import shutil, glob; [shutil.rmtree(p, ignore_errors=True) for p in ['$(BUILD_DIR)', '$(DIST_DIR)'] + glob.glob('*.egg-info')]"
	@echo "Clean done."

# 2. Generar el paquete (sdist y wheel)
# Requiere: pip install build
build: clean
	@echo "Building package..."
	$(PYTHON) -m build
	@echo "Build complete. Check the $(DIST_DIR)/ directory."

# 3. Publicar en TestPyPI (Para probar que todo esté bien)
# Requiere: pip install twine
upload-test: build
	@echo "Uploading to TestPyPI..."
	$(PYTHON) -m twine upload --repository testpypi $(DIST_DIR)/*

# 4. Publicar en PyPI (Producción)
upload: build
	@echo "Uploading to PyPI..."
	$(PYTHON) -m twine upload $(DIST_DIR)/*

# 5. Instalación para desarrollo
install:
	$(PIP) install -e .