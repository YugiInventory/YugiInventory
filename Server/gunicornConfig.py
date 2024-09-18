#gunicorn -w 3 --bind 0.0.0.0:8000 app:app in the server folder

bind = "0.0.0.0:8000" #localserver is still localhost
workers = 3
