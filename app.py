# -*- coding: utf-8 -*-

import sys, os
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for)

from Pets import pets
from Countries import countries
from Users import users

UPLOAD_FOLDER = 'static/images'

app = Flask(__name__)

app.secret_key = '7KUh+e35}7PR{cl9zM[:u;naw5Cg2W0;!t0P=U=@M86&4iYhfqnx+9+%+[x,zo$'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.register_blueprint(pets)
app.register_blueprint(countries)
app.register_blueprint(users)


if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0', debug=True)
