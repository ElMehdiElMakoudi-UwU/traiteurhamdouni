run:
	- python3 manage.py runserver 0.0.0.0:8007
kill: 
	- pkill -f "gunicorn --workers 3 --bind 127.0.0.1:8007 system_traiteur.wsgi:application"
always:
	- nohup gunicorn --workers 3 --bind 127.0.0.1:8007 system_traiteur.wsgi:application > output.log 2>&1 &

venv:
	- source venv/bin/activate