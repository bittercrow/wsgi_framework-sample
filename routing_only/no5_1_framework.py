import re
import io

class MyWSGIFramework(object):
    def __init__(self, routes, css_dir=None, img_dir=None):
        self.routes = routes

        # 静的ファイル向けのディレクトリ設定
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
            # PEP3333より、ファイルオブジェクトはread()やclose()を持っている必要がある
            # https://knzm.readthedocs.io/en/latest/pep-3333-ja.html#optional-platform-specific-file-handling
            # => io.BytesIO()で返すのが良さそう
            # http://docs.python.jp/3/library/io.html#binary-i-o
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
        if re.match(self.static_dir, environ['PATH_INFO']):
            return self.static(environ, start_response) 

        for path, method in self.routes:
            if environ['PATH_INFO'] == path:
                return method(environ, start_response)
        return self.not_found(environ, start_response)
