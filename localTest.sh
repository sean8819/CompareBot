#!/bin/bash

echo "Black test"
black main.py src/
echo -e "\n"

echo "MyPy test"
mypy main.py src/
echo -e "\n"

echo "PyLint test"
pylint main.py src/
echo -e "\n"

echo "flake8 test"
flake8 main.py src/
echo -e "\n"

echo "isort test"
isort main.py src/handlers.py
isort --check main.py src/
echo -e "\n"
