## Linter and tests status
[![linter](https://github.com/kiselz/candy-delivery-app/actions/workflows/flake8.yml/badge.svg)](https://github.com/kiselz/candy-delivery-app/actions/workflows/flake8.yml) [![tests](https://github.com/kiselz/candy-delivery-app/actions/workflows/tests.yml/badge.svg)](https://github.com/kiselz/candy-delivery-app/actions/workflows/tests.yml)

## Candy delivery app
REST service written on Flask for "Yandex Backend School"

## Installation
```
python3 -m pip install poetry --user
git clone https://github.com/kiselz/candy-delivery-app.git
cd ./candy-delivery-app
poetry install
```

## Running
Development
```
make run-dev
```
Production
```
make run-prod
```

## Running all test
Just write
```
make test
```
