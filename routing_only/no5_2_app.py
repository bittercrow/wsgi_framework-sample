# python server.py no5_2_app:app
from no5_1_framework import MyWSGIFramework
from jinja2 import Environment, FileSystemLoader

def get(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])

    return [b"Hello, world."]

def hoge(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b"hoge"]

def index(environ, start_response):
    jinja2_env = Environment(loader=FileSystemLoader('./templates', encoding='utf8'))
    template = jinja2_env.get_template('index.html')
    html = template.render({'messages': ['hoge', 'fuga', 'piyo']})

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [html.encode('utf-8')]


app = MyWSGIFramework([
    ('/', get),
    ('/hoge', hoge),
    ('/index', index),
])