#!/bin/bash
set -eo pipefail
#Entering into a bash shell script to run unit-test cases and generating reports

echo "Coding analysis will be performed shortly..."
python3 -m pip install pylint pylint2junit junitparser; \
python3 -m pip install --index-url https://artefact.skao.int/repository/pypi-internal/simple -r requirements.txt; \
pwd

python3 -m pip install .;
mkdir -p ./build/reports; \
pylint --rcfile=.pylintrc --output-format=parseable  ska-tmc-simulators | tee ./build/reports/linting.stdout; \
pylint --rcfile=.pylintrc --output-format=pylint2junit.JunitReporter ska-tmc-simulators > ./build/reports/linting.xml