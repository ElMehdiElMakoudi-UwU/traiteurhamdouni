run:
	- python3 manage.py runserver 0.0.0.0:8000
kill: 
	- pkill -f "python3 manage.py runserver"
always:
	- nohup python3 manage.py runserver 0.0.0.0:8000 > output.log 2>&1 &
