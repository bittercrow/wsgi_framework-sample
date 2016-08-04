# python server.py no1_base_app:application
# URLに関係なく、同じ値を返す
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b"Hello, world."]