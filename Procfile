web: gunicorn myflaskapp:app
web: gunicorn routes:app
 waitress-serve --listen=*:8000 myflaskapp.wsgi:application
web: gunicorn myflaskapp.wsgi --log-file -