from string import Template
from configparser import ConfigParser
from pathlib import Path


class MyTemplate(Template):
    pattern = r'''
    \$\{(?: 
    (?P<escaped>\{) | # Escape sequence of two delimiters 
    (?P<named>[_a-z][_a-z0-9]*)\} | # delimiter and a Python identifier 
    {(?P<braced>[_a-z][_a-z0-9]*)}\} | # delimiter and a braced identifier 
    (?P<invalid>) # Other ill-formed delimiter exprs 
    ) 
    '''


NGINX_TEMPLATE = '''
upstream ${project} {
	server unix://${socket};
}

upstream ${project}_channels {
    server ${channels_socket};
}

server {
	listen 80;
	listen [::]:80;
	server_name shoor.xyz www.shoor.xyz 111.229.59.77;
	charset utf-8;

	client_max_body_size 10M;

	location /media {
		alias ${base}/media;
	}

	location /static {
		alias ${base}/collected_static;
	}

	location ~ ^/(admin/|api|schema/|__debug__/|rss/) {
		include /etc/nginx/uwsgi_params;
		uwsgi_pass ${project};
	}

	location /ws/ {
        proxy_pass http://mysite_channels;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
    }

	location / {
		root ${front}/dist;
		try_files $uri $uri/ /index.html;
		gzip_static on; # 使用事先压缩的gzip
	}
}
'''


def main():
    uwsgi = ConfigParser()
    base = Path.cwd()
    base_str = base.as_posix()
    project = 'mysite'
    uwsgi['uwsgi'] = {
        'chdir': base,
        'module': f'{project}.wsgi:application',
        'home': f'{base}/.venv',
        'socket': f'{base_str}/.run/socket/uwsgi.sock',
        'pidfile': f'{base_str}/.run/pid/uwsgi.pid',
        'master': True,
        'processes': 4,
        'max-request': 5000,
        'harakiri': 60,
        'daemonize': f'{base_str}/.run/log/uwsgi.log',
        'disable-logging': True,
        'vacuum': True,
    }
    supervisor = ConfigParser(interpolation=None)
    supervisor['fcgi-program:mysite_channels'] = {
        'socket':'tcp://localhost:8010',
        'directory':base_str,
        'command': f'{base_str}/.venv/bin/daphne --fd 0 --access-log - --proxy-headers {project}.asgi:application',
        'numprocs':4,
        'process_name':'mysite_channels%(process_num)d',
        'autostart':True,
        'autorestart':True,
        'stdout_logfile': f'{base_str}/.run/log/channels.log',
        'redirect_stderr':True,
    } 
    path = base / '.run' / 'config'
    path.mkdir(parents=True, exist_ok=True)
    (base / '.run' / 'pid').mkdir(exist_ok=True)
    (base / '.run' / 'socket').mkdir(exist_ok=True)
    (base / '.run' / 'log').mkdir(exist_ok=True)
    with (path / 'uwsgi.ini').open('w', encoding='utf-8`') as fo:
        uwsgi.write(fo)
    with (path / 'supervisor.ini').open('w', encoding='utf-8`') as fo:
        supervisor.write(fo)
    nginx = MyTemplate(NGINX_TEMPLATE).safe_substitute(
        uwsgi['uwsgi'],
        base=base,
        project=project,
        front=base.parent / 'mysite_front',
        channels_socket=supervisor['fcgi-program:mysite_channels']['socket'][6:]
    )
    (path / 'nginx.conf').write_text(nginx, encoding='utf-8')


if __name__ == "__main__":
    main()
