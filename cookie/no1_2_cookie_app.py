# python server.py no1_2_cookie_app:app
from http.cookies import SimpleCookie
from no1_1_cookie_framework import MyWSGIFramework


# Cookieまわりの参考
# http://pwp.stevecassidy.net/wsgi/cookies.html
def cookie(environ, start_response):
    visit_in_html = 1
    headers = [('Content-Type', 'text/plain'),]

    # 今回、"visit"というCookieは一つしかない前提、実際には複数設定されることもある
    # http://www.yunabe.jp/docs/cookie_and_security.html#cookie-
    if app.cookie:
        if 'visit' in app.cookie:
            app.cookie['visit'] = visit_in_html = int(app.cookie['visit'].value) + 1
        else:
            app.cookie['visit'] = 1

        # RFC6265より、UAからはCookieの属性は送信されないため、サーバ側で毎回属性をセットする
        # https://triple-underscore.github.io/RFC6265-ja.html#section-4.2.2
        app.cookie['visit']['httponly'] = True

        # 複数のCookieへのサーバ側での対応
        # RFC6265より、複数のCookieがある場合、その分Set-Cookie応答ヘッダを用意する必要がある
        # https://triple-underscore.github.io/RFC6265-ja.html#section-4.1.1
        # そこで、複数のCookieがあるapp.cookie(SimpleCookieオブジェクト)の値を、output(header='')で確認すると、
        # http://docs.python.jp/3/library/http.cookies.html#http.cookies.BaseCookie.output
        print('-'*10)
        print('app_cookie:\n{}\n'.format(app.cookie.output(header='')))
        print('-'*10)
        # """
        # ----------
        # app_cookie:
        #  hoge=fuga
        #  visit=2; HttpOnly
        # 
        # ----------
        # """
        # と、「CRLF + 半角スペース」で連結された状態で取得できる
        # 今回、HTTPレスポンスヘッダは
        # "headers.append(('Set-Cookie', '<Cookie名>=<Cookie値>'))"
        # のようにして作ることから、以下のような処理となる
        server_cookies = app.cookie.output(header='').split('\r\n')
        for sc in server_cookies:
            headers.append(('Set-Cookie', sc))

    else:
        cookie_visit = SimpleCookie('visit=1')
        cookie_visit['visit']['httponly'] = True
        headers.append(('Set-Cookie', cookie_visit.output(header='')))
        headers.append(('Set-Cookie', 'hoge=fuga'))

    
    start_response('200 OK', headers)
    return ["Hello, No.{}".format(visit_in_html).encode('utf-8')]


# URLルーティング設定
app = MyWSGIFramework([
    ('/', cookie),
])