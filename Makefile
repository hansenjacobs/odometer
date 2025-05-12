# This file was created for use on/with: Windows 10; Git Bash; Python3

# This is needed to make sure 'make <command>' does not skip if we have a dir that matches the target name
.PHONY: setup _venv

# This is the default command that runs if you run just 'make'
.DEFAULT: help

help:
	@# add " sort | " before awk for alaphabetical sorting, change the -10s to make the command text spacing wider
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' ${MAKEFILE_LIST} | awk 'BEGIN {FS = ": .*?## "}; {n=split($$1,cmd,"Makefile:")}; {printf "\033[36m%-16s\033[0m %s\n", cmd[n], $$2}'

_venv: 
	@# If the venv doesn't exist or `pip freeze` doesn't match the constraints file, do make setup.
	test -x _venv/Scripts/pip \
	&& test "`cat test-constraints.txt`" = "`_venv/Scripts/pip freeze`" \
	|| (rm -rf _venv \
		&& python3 -m venv --upgrade-deps _venv \
		&& _venv/Scripts/pip install --disable-pip-version-check -r test-constraints.txt)

setup: ## Rebuild the venv even if it doesn't seem necessary
	rm -rf _venv
	make _venv

freeze: ## Rebuild constraint files using latest requirements
	rm -rf _venv
	python3 -m venv _venv
	_venv/Scripts/python -m pip install --upgrade pip
	@#App-only dependencies
	_venv/Scripts/pip install --disable-pip-version-check -r requirements.txt
	_venv/Scripts/pip check
	_venv/Scripts/pip freeze > constraints.txt
	@#Dev dependencies
	_venv/Scripts/pip install --disable-pip-version-check -r test-requirements.txt
	_venv/Scripts/pip check
	_venv/Scripts/pip freeze > test-constraints.txt
	@#Ensure the modified time is newer than constraints so `make _venv` won't rebuild
	touch _venv

lint: _venv
	./_venv/Scripts/flake8 --max-line-length=120 src/ tests/

test: _venv lint
	_venv/Scripts/python -m pytest
