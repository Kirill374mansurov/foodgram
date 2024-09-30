python manage.py makemigrations --no-input
python manage.py migrate --no-input
#python manage.py run_import
gunicorn --bind 0:8000 backend.wsgi
docker compose exec backend python manage.py collectstatic
docker compose exec backend cp -r /app/collected_static/. /backend_static/static/