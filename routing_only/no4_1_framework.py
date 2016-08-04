class MyWSGIFramework(object):
    def __init__(self, routes):
        self.routes = routes

    def not_found(self, environ, start_response):
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b"Not found by framework."]


    def __call__(self, environ, start_response):
        for path, method in self.routes:
            if environ['PATH_INFO'] == path:
                return method(environ, start_response)
        return self.not_found(environ, start_response)
