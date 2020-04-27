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

server {
	listen 80;
    server_name test.test www.test.test;
	# server_name shoor.xyz www.shoor.xyz 111.229.59.77;
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
    project = 'mysite'
    uwsgi['uwsgi'] = {
        'chdir': base,
        'module': f'{project}.wsgi:application',
        'home': f'{base}/.venv',
        'socket': f'/run/{project}.uwsgi.sock',
        'pidfile': f'/run/{project}.uwsgi.pid',
        'master': True,
        'processes': 4,
        'max-request': 5000,
        'harakiri': 60,
        'daemonize': f'/var/log/{project}.uwsgi.log',
        'disable-logging': True,
        'vacuum': True,
    }
    (base)
    with (base / 'uwsgi.ini').open('w', encoding='utf-8`') as fo:
        uwsgi.write(fo)
    nginx = MyTemplate(NGINX_TEMPLATE).safe_substitute(
        uwsgi['uwsgi'],
        base=base,
        project=project,
        front=base.parent / 'mysite_front',
    )
    (base / 'nginx.conf').write_text(nginx, encoding='utf-8')


if __name__ == "__main__":
    main()
