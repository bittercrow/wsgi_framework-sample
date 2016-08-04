# python server.py no3_router_separately_by_class:app
class MyWSGIApplication(object):
    def __init__(self):
        self.routes = [
            ('/', self.get),
            ('/hoge', self.hoge),
        ]

    def get(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b"Hello, world by class."]

    def hoge(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b"hoge by class"]

    def not_found(self, environ, start_response):
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b"Not found by class."]


    def __call__(self, environ, start_response):
        for path, method in self.routes:
            if path == environ['PATH_INFO']:
                return method(environ, start_response)

        return self.not_found(environ, start_response)

app = MyWSGIApplication()