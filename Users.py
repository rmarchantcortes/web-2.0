from flask import Blueprint
from Model import(
    select,
    insert
)
from Response import (
    format_json,
    request_wants_json
)
from flask import(
    request,
    render_template,
    redirect,
    url_for
)
from Auth import *

users = Blueprint('users', __name__)

@users.route('/users/', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        data = select('SELECT use_id, use_name, use_phone_number, use_email, use_user_state FROM user')
        return format_json(data)
    else:
        name = request.form['name']
        phone = request.form['phone']
        state = request.form['state']
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']
        if name and phone and state and address and email and password:
            salt = get_new_salt();
            hashed_password = get_hash(password, salt)
            user_id = insert("INSERT INTO user(use_name, use_phone_number, use_user_state, use_user_type, use_email, use_password, use_state_id, use_salt) VALUES('%s', '%s', 1, 3, '%s', '%s', %i, '%s')" % (name, phone, email, hashed_password, int(state), salt))
            if user_id > 0:
                data = select('SELECT use_id, use_name, use_email FROM user WHERE use_id = %i' % (user_id))
                return format_json(data, 201)
            else:
                return "error"

@users.route('/users/new/', methods = ['GET'])
def create_user():
    return render_template('public/create_user.html', script = ['bower_components/jsSHA/src/sha.js','js/public/create_user.js'])

@users.route('/users/types/')
def get_user_types():
    data = select("SELECT uty_id, uty_detail FROM user_type")
    return format_json(data)

@users.route('/users/states')
def get_users_states():
    data = select("SELECT * FROM user_state")
    return format_json(data)

@users.route('/users/login/', methods = ['GET', 'POST'])
def user_login():
    if request.method == 'GET' and not validate(get_token()):
        return render_template('public/login.html')
    elif request.method == 'POST' and not validate(get_token()):
        email = request.form['email'];
        password = request.form['password'];
        
        if email and password:
            data = select("SELECT use_salt FROM user WHERE use_email = '%s'" % (email))
            if len(data) > 0:
                hashed_pass = get_hash(password, data[0]['use_salt'])
                user = select("SELECT use_id, use_user_type FROM user WHERE use_email = '%s' AND use_password = '%s' and use_user_state = 1" % (email, hashed_pass))
                if len(user) > 0:
                    set_session(set_token(user[0]['use_id'], user[0]['use_user_type']))
                    return format_json("")
                return format_json("", 401)
            else:
                return format_json("", 401)
    else:
        return redirect(url_for('pets.get_pets'))
            
@users.route('/users/logout/', methods = ['GET'])
def user_logout():
    unset_session()
    return redirect(url_for('pets.get_pets'))

@users.route('/users/me/profile')
def user_profile():
    if validate(get_token()):
        user = select("SELECT use_name, use_user_type, use_email, use_phone_number, use_state_id FROM user WHERE use_id = %s" % (get_user_id(get_token())))
        return render_template('private/profile.html', user = user)
    else:
        return render_template('errors/403.html')

@users.route('/users/me/adoptions')
def user_adoptions():
    if validate(get_token()):
        user = select("SELECT use_name, use_user_type FROM user WHERE use_id = %s" % (get_user_id(get_token())))
        adoptions = select("SELECT use_name, pet_name, ast_detail FROM pet, user, adoption, adoption_state WHERE use_id = ado_user_request and pet_id = ado_pet_id and ast_id = ado_state ORDER BY ado_updated DESC")
        return render_template('private/myadoptions.html', user = user, adoptions = adoptions)
    else:
        return render_template('errors/403.html')

@users.route('/users/me/pets')
def user_pets():
    if validate(get_token()):
        user = select("SELECT use_name, use_user_type FROM user WHERE use_id = %s" % (get_user_id(get_token())))
        pets = select("SELECT * FROM pet WHERE pet_user_id = %i" % (get_user_id(get_token())))
        return render_template('private/mypets.html', user = user, pets = pets)
    else:
        return render_template('errors/403.html')

