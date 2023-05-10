setup:
    pipenv sync --dev
    cp -n ./careveillance/.env.example ./careveillance/.env
    pipenv run python manage.py collectstatic --noinput
    pipenv run python manage.py migrate

setup-user:
    pipenv run python manage.py createsuperuser

test:
    pipenv run pytest

vt:
    open ./htmlcov/index.html

run:
    pipenv run python manage.py runserver

manage *COMMAND:
    pipenv run python manage.py {{COMMAND}}

docker-dev *COMMAND:
    docker compose -f docker-compose.dev.yml {{COMMAND}}