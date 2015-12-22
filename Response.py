from flask import(
    json,
    Response,
    request
)

def format_json(result, code = 200):
    data = json.dumps({'status': code, 'data': result})
    resp = Response(data, status=code, mimetype='application/json')
    return resp

def request_wants_json():
    best = request.accept_mimetypes \
    .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
    request.accept_mimetypes[best] > \
    request.accept_mimetypes['text/html']
