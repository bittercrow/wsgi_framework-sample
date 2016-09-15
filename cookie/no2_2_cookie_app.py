# python server.py no2_2_cookie_app:app
from no2_1_cookie_framework import MyWSGIFramework

def cookie(environ, start_response):
    visit_in_html = 1
    headers = [('Content-Type', 'text/plain'),]

    if app.cookie:
        v = app.get_cookie('visit')
        if v:
            visit_in_html = int(v.value) + 1
            app.set_cookie('visit', visit)
        else:
            app.set_cookie('visit', 1)
        app.set_cookie('fuga', 'fugafuga', httponly=True)

    else:
        app.set_cookie('visit', 1)

        # Cookie値の他、max-age属性もセットしてみる
        app.set_cookie('hoge', 'hogehoge', max_age=10)

        # Cookie値の他、httponly属性もセットしてみる
        app.set_cookie('fuga', 'fugafuga', httponly=True)

    # ここまでで作成したCookieをCookieヘッダに設定する
    # リストにリストを追加するので、append()ではなくextend()を使う
    headers.extend(app.generate_cookie_header())

    start_response('200 OK', headers)
    return ["Hello, No.{}".format(visit_in_html).encode('utf-8')]


# URLルーティング設定
app = MyWSGIFramework([
    ('/', cookie),
])