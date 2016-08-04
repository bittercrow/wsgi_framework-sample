# python server.py no2_router_separately_by_func:application 

def get(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b"Hello, world."]

def hoge(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b"hoge"]

def not_found(environ, start_response):
    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    return [b"Not found."]


# http://web.science.mq.edu.au/~mattr/courses/web_applications/3a_wsgi_and_static_files/notes.html
routes = [
    ('/', get),
    ('/hoge', hoge),
]


def application(environ, start_response):
    for path, func in routes:
        if path == environ['PATH_INFO']:
            return func(environ, start_response)

    return not_found(environ, start_response)