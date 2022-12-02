APPFOLDERPATH=`pwd`
    APPNAME=$1
    DOMAINNAME=$2
    if [ "$APPNAME" = "" ] || [ "$DOMAINNAME" = "" ]; then
        echo "Usage:"
        echo "  $ create_django_project_run_env <project> <domain> "
        exit 1
    fi
apt-update

apt-get -y install python3-dev python3-pip nginx
pip3 install --upgrade pip
pip3 install virtualenv
pip install django gunicorn 
REQ=`find . -type f -name requirement*.txt`
pip install -r $REQ 

deactivate

REQ=`find . -type f -name requirement*.txt`

cat > /etc/systemd/system/gunicorn.socket << EOF
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOF

cat > /etc/systemd/system/gunicorn.service << EOF
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=${APPFOLDERPATH}
ExecStart=${APPFOLDERPATH}/myprojectenv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          ${APPNAME}.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

cat > /etc/nginx/sites-available/${APPNAME} << EOF

proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=custom_cache:10m inactive=60m;

upstream origin_server {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name ${DOMAINNAME};

location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root ${APPFOLDERPATH};
    }

location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
  proxy_cache custom_cache;
        proxy_cache_valid any 10m;
        add_header X-Proxy-Cache $upstream_cache_status;
    }

}
EOF