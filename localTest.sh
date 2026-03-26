#!/bin/bash
echo -e "\n========================== LOCAL TEST STARTED ========================== \n"
echo "Black test"
black main.py src/ tests/
echo -e "\n"

echo "MyPy test"
mypy main.py src/ tests/
echo -e "\n"

echo "PyLint test"
pylint main.py src/ tests/
echo -e "\n"

echo "flake8 test"
flake8 main.py src/ tests/
echo -e "\n"

echo "isort test"
isort main.py src/ tests/
isort --check main.py src/
echo -e "\n"

echo "Pytest test"
pytest tests/ -v --cov=src --cov-report=term-missing
echo -e "\n"