.PHONY: install prepare-data figures tables publication-assets validate test clean-generated

PYTHON ?= python

install:
	$(PYTHON) -m pip install -e ".[test]"

prepare-data:
	$(PYTHON) scripts/prepare_data.py

figures:
	$(PYTHON) scripts/generate_all_figures.py

tables:
	$(PYTHON) scripts/generate_all_tables.py

publication-assets: figures tables validate

validate:
	$(PYTHON) scripts/validate_release.py

test:
	$(PYTHON) -m pytest

clean-generated:
	rm -f figures/generated/*.pdf figures/generated/*.png
	rm -f tables/generated/*.tex tables/machine_readable/*.csv
