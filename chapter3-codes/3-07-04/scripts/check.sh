#!/bin/bash
set -e

echo "Running Black..."
black .

echo "Running isort..."
isort .

echo "Running Flake8..."
flake8 .

echo "Running Mypy..."
mypy .

echo "All checks passed!"
