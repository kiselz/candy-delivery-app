run-dev:
	poetry run python3 -m candy_delivery_app.run --dev

run-test:
	poetry run python3 -m candy_delivery_app.run --test

run-prod:
	poetry run python3 -m candy_delivery_app.run --prod

linter:
	poetry run flake8 candy_delivery_app

test:
	poetry run pytest