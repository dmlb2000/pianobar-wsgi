from wsgiref.simple_server import make_server
from cgi import parse_qs
from pianobar import start

def pianobar(env, start_response):
    command = env['PATH_INFO'].split('/')[1]
    ret = ""
    if command == "":
        ret = '{ "status": "error", "message": "Try starting the server with the start command." }'
    elif command == "start":
        try:
            request_body_size = int(env.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = env['wsgi.input'].read(request_body_size)
        postdata = parse_qs(request_body)
        res = start(postdata['username'][0], postdata['password'][0], postdata['channel'][0])
        if res == -1:
            ret = '{ "status": "error", "message": "Pianobar is already running." }'
        elif res == -2:
            ret = '{ "status": "error", "message": "Invalid username or password." }'
        else:
            ret = '{ "status": "success", "message": "Started pianobar for %s." }'%(username)
    start_response('200 OK', [('Content-Type','application/json')])
    return ret

if __name__ == "__main__":
    httpd = make_server('10.15.19.13', 8080, pianobar)
    httpd.serve_forever()
