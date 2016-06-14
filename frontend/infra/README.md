# README 1: UBUNTU

## General commands

See Upstart processes: `sudo initctl list`

Control Upstart process: `sudo service frontend-uwsgi <start/stop/restart/status>`

Restart NGINX: `sudo nginx -s reload`

## Config file locations

frontend-nginx:
/etc/nginx/sites-available/frontend-nginx
/etc/nginx/sites-enabled/frontend-nginx (create link using `ln -s <source> <target>`)

frontend-uwsgi.conf:
/etc/init/frontend-uwsgi.conf

frontend-uwsgi.ini:
/etc/frontend/frontend-uwsgi.ini

# README 2: CENTOS

Mostly commands and file locations needed to administer the frontend.

## Key config files

| file path | description |
|-----------|-------------|
| /etc/nginx/sites-available/frontend-nginx | config file for nginx |
| /etc/systemd/system/frontend.service  | systemd unit file for frontend |
| twitter_research/frontend/infra/frontend-uwsgi-centos.ini  | uwsgi ini file for frontend |

## Key commands

### sudo systemctl <command> <service>

Services: `nginx`, `frontend`

Commands: `status`, `restart`

### sudo uwsgi --ini frontend-uwsgi-centos.ini

Call from the `/home/daniel/twitter_research/frontend/infra` directory.

## SELinux

Basically SELinux is a layer of security that is almost completely inscrutable. Here are the commands I ran that let things work. Had I not stumbled across these commands on the internet, this site would never have gone up.

Allowing nginx to serve static files: `sudo setenforce 0`