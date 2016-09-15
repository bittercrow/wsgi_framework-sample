# python server.py cookie_test_set_max_age:app
from http.cookies import SimpleCookie
from no1_1_cookie_framework import MyWSGIFramework

def cookie(environ, start_response):
    visit_in_html = 1
    headers = [('Content-Type', 'text/plain'),]

    if app.cookie:
        visit_in_html = int(app.cookie['http_only'].value) + 1
    else:
        http_only = SimpleCookie('http_only=1')
        http_only['http_only']['max-age'] = 5
        headers.append(('Set-Cookie', http_only.output(header='')))
    
    start_response('200 OK', headers)
    return ["Hello, No.{}".format(visit_in_html).encode('utf-8')]


# URLルーティング設定
app = MyWSGIFramework([
    ('/', cookie),
])