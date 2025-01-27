cd /var/www/html/webapps
source venv/bin/activate
cd /var/www/html/webapps/promises
python manage.py collectstatic
cd /var/www/html/webapps/
nohup uwsgi runserver.ini &
