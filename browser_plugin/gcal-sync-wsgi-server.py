#! /usr/bin/python.27
# coding: utf-8

import cgi
import json
import os


TOKEN = 'gcal-sync-with-ping-t'
SCRIPT = None

def application(environ, start_response):

    start_response('200 OK', [('Content-Type','application/json')])

    method = environ.get('REQUEST_METHOD')

    print_char = ''

    if method == 'POST':
        wsgi_input     = environ['wsgi.input']
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        query = dict(cgi.parse_qsl(wsgi_input.read(content_length)))

        print query
        if 'token' in query and query['token'] == TOKEN:
            os.system(SCRIPT)
            return json.dumps({'code':200, 'msg': 'ok.'})
        else:
            return json.dumps({'code':400, 'msg': 'invalid token.'})

    return json.dumps({'code':500, 'msg': 'invalid method'})



def main():
    global SCRIPT
    import sys
    from wsgiref import simple_server

    if len(sys.argv) < 3:
        f = os.path.basename(__file__)
        print >> sys.stderr, 'usage: %s host port script' % f
        sys.exit()

    host, port, script = sys.argv[1:]
    port = int(port)

    print 'host = %s' % host
    print 'port = %s' % port
    print 'script = %s' % script

    SCRIPT = script

    server = simple_server.make_server(host, port, application)
    server.serve_forever()

# python gcal-sync-wsgi-server.py $(hostname -f) 8080 '../app.sh 8 &'
if __name__ == '__main__':
    main()

