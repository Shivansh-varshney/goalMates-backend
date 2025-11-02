set -o errexit  

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input --clear
python manage.py makemigrations --noinput
python manage.py migrate --noinput