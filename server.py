from wsgiref.simple_server import make_server
from cgi import parse_qs
from pianobar import PianoBar

def pianobar(env, start_response):
    command = env['PATH_INFO'].split('/')[1]
    ret = ""
    p = PianoBar()
    if command in ['love', 'ban', 'info', 'pause', 'next', 'start', 'stop', 'change', 'channels']:
        if command == "start":
            try:
                request_body_size = int(env.get('CONTENT_LENGTH', 0))
            except (ValueError):
                request_body_size = 0
            request_body = env['wsgi.input'].read(request_body_size)
            postdata = parse_qs(request_body)
            p.start(postdata['username'][0], postdata['password'][0], postdata['channel'][0])
            ret = '{ "status": "success", "message": "Started pianobar for %s." }'%(postdata['username'][0])
        elif command == "info":
            from json import dumps
            ret = dumps({"info":p.info()})
        elif command == "channels":
            from json import dumps
            ret = dumps({"channels":p.channels()})
        elif command == "change":
            new_channel = env['PATH_INFO'].split('/')[2]
            p.change(new_channel)
            ret = '{ "status": "success", "message": "Changed channel to %s." }'%(new_channel)
        elif command == "stop":
            p.stop()
            ret = '{ "status": "success", "message": "Ran %s." }'%(command)
        else:
            p.__dict__[command]()
            ret = '{ "status": "success", "message": "Ran %s." }'%(command)
    else:
        ret = '{ "status": "error", "message": "Try starting the server with the start command." }'
    start_response('200 OK', [('Content-Type','application/json')])
    return ret

if __name__ == "__main__":
    httpd = make_server('10.15.19.13', 8080, pianobar)
    httpd.serve_forever()
