#!/bin/sh

# Hey, if you're using windows and autoCRLF conversion, you'll run into weird issues with this script even under WSL or docker. Convert it back to LF or use LF only.
python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"