uwsgi --http 158.143.10.55:5000 --wsgi-file mxwg.py --callable app --master --processes 1 --threads 1 --stats 158.143.10.55:9191 -d /opt/mxwg/mxwg.log
 
