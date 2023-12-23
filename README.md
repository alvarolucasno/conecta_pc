python manage.py runserver 0.0.0.0:8880

DEPLOY

-------------------------------------------------

gunicorn --bind 0.0.0.0:8880 conecta_pc.wsgi

-------------------------------------------------

sudo nano /etc/systemd/system/gunicorn2.socket

-------------------------------------------------

[Unit] 
Description=gunicorn2 socket

[Socket] 
ListenStream=/run/gunicorn2.sock

[Install] 
WantedBy=sockets.target

-------------------------------------------------

sudo nano /etc/systemd/system/gunicorn2.service

--------------------------------------------------

[Unit] 
Description=gunicorn2 daemon 
Requires=gunicorn2.socket 
After=network.target

[Service] 
User=botdrfv 
Group=www-data 
WorkingDirectory=/home/botdrfv/conecta_pc
ExecStart=/home/botdrfv/conecta_pc/venv/bin/gunicorn \
--access-logfile - \
--workers 3 \
--bind unix:/run/gunicorn2.sock \
conecta_pc.wsgi:application

[Install] 
WantedBy=multi-user.target 

--------------------------------------------------

sudo systemctl start gunicorn2.socket
sudo systemctl enable gunicorn2.socket

--------------------------------------------------

sudo systemctl status gunicorn2.socket sudo systemctl status gunicorn curl --unix-socket /run/gunicorn2.sock localhost

--------------------------------------------------

sudo nano /etc/nginx/sites-enabled/conecta_pc

--------------------------------------------------

server { listen 8880; server_name localhost;

location = /favicon.ico { access_log off; log_not_found off; }

location /static/ {
    root /home/botdrfv/conecta_pc/data/web/static;
}

location /media {
    alias /home/botdrfv/conecta_pc/data/web/media;
}

location / {
    include proxy_params;
    proxy_pass http://unix:/run/gunicorn2.sock;
}
}