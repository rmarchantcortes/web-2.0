from flask import(
    json,
    Response,
    request
)

def format_json(result, code = 200):
    if result:
        data = json.dumps({'status': code, 'data': result})
    else:
        data = json.dumps({'status': 404, 'data': ""})
    resp = Response(data, status=code, mimetype='application/json')
    return resp

def request_wants_json():
    best = request.accept_mimetypes \
    .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
    request.accept_mimetypes[best] > \
    request.accept_mimetypes['text/html']
    
def return_forbidden():
    if request_wants_json():
        return format_json("", 403)
    else:
        return render_template('errors/403.html')
