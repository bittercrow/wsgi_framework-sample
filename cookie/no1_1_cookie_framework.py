import re
import io
from http.cookies import SimpleCookie

class MyWSGIFramework(object):
    def __init__(self, routes, css_dir=None, img_dir=None):
        self.routes = routes
        self.static_dir = '/static'
        css_dir = css_dir if css_dir else "/css/"
        self.css_dir = '{static}{css}'.format(static=self.static_dir, css=css_dir)
        img_dir = img_dir if img_dir else "/images/"
        self.img_dir = '{static}{img}'.format(static=self.static_dir, img=img_dir)

    def static(self, environ, start_response):
        content_type = []
        if re.match(self.css_dir, environ['PATH_INFO']):
            content_type.append(('Content-Type', 'text/css'))
        elif re.match(self.img_dir, environ['PATH_INFO']):
            content_type.append(('Content-Type', 'image/png'))
        else:
            return self.not_found(environ, start_response)

        try:
            fullpath = './{}'.format(environ['PATH_INFO'])
            with open(fullpath, "rb") as f:
                r = f.read()
            binary_stream = io.BytesIO(r)
        except:
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [b"Internal server error"]

        start_response('200 OK', content_type)
        return binary_stream


    def not_found(self, environ, start_response):
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b"Not found."]


    def __call__(self, environ, start_response):
        # cookieを取得し、Pythonで扱いやすいSimpleCookieオブジェクトにしておく
        # コンストラクタではload()が呼ばれてるので、そのまま渡して良い
        # (文字列はパース、そうでないとdictな前提)
        # https://github.com/python/cpython/blob/master/Lib/http/cookies.py#L505
        self.cookie = SimpleCookie(environ['HTTP_COOKIE']) if 'HTTP_COOKIE' in environ else None
        
        if re.match(self.static_dir, environ['PATH_INFO']):
            return self.static(environ, start_response) 

        for path, method in self.routes:
            if environ['PATH_INFO'] == path:
                return method(environ, start_response)
        return self.not_found(environ, start_response)
