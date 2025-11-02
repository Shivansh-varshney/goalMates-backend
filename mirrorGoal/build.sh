set -o errexit  

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input --clear
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Create superuser if it doesn't exist
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='${DJANGO_SUPERUSER_EMAIL}').exists() or User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')"