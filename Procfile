web: PYTHONPATH=$PYTHONPATH:$PWD/project gunicorn src.config.wsgi
release: python project/manage.py migrate --no-input; python project/manage.py clear_cache;
