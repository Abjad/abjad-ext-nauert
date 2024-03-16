.PHONY: docs build

black-check:
	black --check --diff .

black-reformat:
	black .

build:
	python setup.py sdist

clean:
	find . -name '*.pyc' | xargs rm
	find . -name __pycache__ | xargs rm -Rf
	rm -Rif *.egg-info/
	rm -Rif .cache/
	rm -Rif .tox/
	rm -Rif build/
	rm -Rif dist/
	rm -Rif htmlcov/
	rm -Rif prof/

flake_ignore = --ignore=E203,E266,E501,W503
flake_options = --isolated --max-line-length=88

flake8:
	flake8 ${flake_ignore} ${flake_options}

isort-check:
	isort \
	--case-sensitive \
	--check-only \
	--diff \
	--line-width=88 \
	--multi-line=3 \
	--project=abjad \
	--project=abjadext \
	--thirdparty=ply \
	--thirdparty=uqbar \
	--trailing-comma \
	--use-parentheses \
	.

isort-reformat:
	isort \
	--case-sensitive \
	--line-width=88 \
	--multi-line=3 \
	--project=abjad \
	--project=abjadext \
	--thirdparty=ply \
	--thirdparty=uqbar \
	--trailing-comma \
	--use-parentheses \
	.

mypy:
	mypy abjadext
	mypy tests

project = abjadext

pytest:
	pytest .

pytest-coverage:
	rm -Rf htmlcov/
	pytest \
	--cov-config=.coveragerc \
	--cov-report=html \
	--cov=${project} \
	.

pytest-x:
	pytest -x .

reformat:
	make black-reformat
	make isort-reformat

release:
	make clean
	make build
	pip install -U twine
	twine upload dist/*.tar.gz

check:
	make black-check
	make flake8
	make isort-check
	make mypy

test:
	make black-check
	make flake8
	make isort-check
	make mypy
	make pytest
