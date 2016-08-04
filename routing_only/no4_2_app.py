# python server.py no4_2_app:app
from no4_1_framework import MyWSGIFramework

def get(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b"Hello, world by framework."]

def hoge(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b"hoge by framework"]


app = MyWSGIFramework([
    ('/', get),
    ('/hoge', hoge),
])