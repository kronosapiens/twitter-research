## General commands

See Upstart processes: `sudo initctl list`

Control Upstart process: `sudo service frontend <start/stop/restart/status>`

Restart NGINX: `sudo nginx -s reload`

## Config file locations

frontend-nginx:
/etc/nginx/sites-available/frontend-nginx
/etc/nginx/sites-enabled/frontend-nginx (create link)

frontend-uwsgi.conf:
/etc/init/frontend-uwsgi.conf

frontend-uwsgi.ini:
/etc/frontend/frontend-uwsgi.ini