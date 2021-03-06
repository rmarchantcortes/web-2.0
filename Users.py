from flask import Blueprint
from Model import(
    select,
    insert
)
from Response import (
    format_json,
    request_wants_json,
    return_forbidden
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
                return format_json(data, 400)

@users.route('/users/new/', methods = ['GET'])
def create_user():
    if not validate(get_token()):
        return render_template('public/create_user.html', script = ['bower_components/jsSHA/src/sha.js','js/public/create_user.js'])
    else:
        return render_template('errors/400.html')
        
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

@users.route('/users/me/administration/', methods = ['GET'])
def user_admin():
    if request.method == 'GET':
        if validate(get_token()):
            user = select("SELECT use_name, use_user_type FROM user WHERE use_id = %s" % (get_user_id(get_token())))
            admins = select("SELECT use_name, use_email, use_phone_number, sta_name, cou_name, ust_detail FROM user_state, state, user, country WHERE ust_id=use_user_state AND cou_id=sta_country_id AND  use_state_id=sta_id AND use_user_type = 1")
            moderators = select("SELECT use_name, use_email, use_phone_number, sta_name, cou_name, ust_detail FROM user_state, state, user, country WHERE ust_id=use_user_state AND cou_id=sta_country_id AND  use_state_id=sta_id AND use_user_type = 2")
            users = select("SELECT use_name, use_email, use_phone_number, sta_name, cou_name, ust_detail FROM user_state, state, user, country WHERE ust_id=use_user_state AND cou_id=sta_country_id AND  use_state_id=sta_id AND use_user_type = 3")
            if user[0]['use_user_type'] == 1:                
                return render_template('private/administration.html', user = user, admins = admins, moderators = moderators, users = users)
            elif user[0]['use_user_type'] == 2:
                return render_template('private/administration.html', user = user, moderators = moderators, users = users)
            else:
                return render_template('errors/403.html')
        else:
            return render_template('errors/403.html')
    else:
        return render_template('errors/403.html')

@users.route('/users/me/profile/', methods = ['GET','PUT'])
def user_profile():
    if request.method == 'GET':
        if validate(get_token()):
            user = select("SELECT u.use_name, u.use_user_type, u.use_email, u.use_phone_number, s.sta_name, t.uty_detail, c.cou_name FROM user u, state s, user_type t, country c WHERE c.cou_id=s.sta_country_id AND t.uty_id=u.use_user_type AND u.use_state_id=s.sta_id AND u.use_id = %s" % (get_user_id(get_token())))
            return render_template('private/profile.html', user = user)
        else:
            return render_template('errors/403.html')
    elif request.method == 'PUT':
            name = request.form['name']
            email = request.form['email']
            state = request.form['u_state']
            phone = request.form['phone']
            last_passwd = request.form['last_passwd']
            new_passwd = request.form['new_passwd']
            new_passwd_second = request.form['re_new_passwd']

            if last_passwd and new_passwd and new_passwd_second:
                hashed_password = get_hash(last_passwd, select("SELECT use_salt FROM user WHERE use_id=%s" % (get_user_id(get_token()))))
                if new_passwd == new_passwd_second and hashed_password == select("SELECT use_password FROM user WHERE use_id=%s" % (get_user_id(get_token()))):
                    salt = get_new_salt();
                    hashed_new_password = get_hash(new_passwd, salt)
                    update("UPDATE user SET use_name=%s, use_email=%s, use_state_id=(SELECT sta_id FROM state WHERE sta_name=%s AND use_id=%s), use_phone_number=%s, use_password=%s, use_salt=%s WHERE use_id = %s" % (name, email, state, get_user_id(get_token()), phone, salt, get_user_id(get_token())))
                    return render_template('private/profile.html')
                else:
                    return render_template('errors/403.html')
            else:
                update("UPDATE user SET use_name=%s, use_email=%s, use_state_id=(SELECT sta_id FROM state WHERE sta_name=%s AND use_id=%s), use_phone_number=%s WHERE use_id = %s" % (name, email, state, get_user_id(get_token()), phone, get_user_id(get_token())))
                return render_template('private/profile.html')        
    else:
        return render_template('errors/403.html')

@users.route('/users/me/adoptions/')
def user_adoptions():
    if validate(get_token()):
        adoptions = select("SELECT use_name, pet_name, pst_detail, ado_pet_id, (SELECT pim_url FROM pet_image WHERE ado_pet_id = pim_pet_id) as pet_image, pet_race, pty_detail, pet_state FROM pet, pet_state, user, adoption, adoption_state, pet_type WHERE use_id = ado_user_request and use_id = %i and pet_id = ado_pet_id and pst_id = pet_state AND pty_id = pet_type GROUP BY ado_pet_id ORDER BY ado_updated DESC" % (get_user_id(get_token())))
        if request_wants_json():
            return format_json(adoptions)
        else:
            user = select("SELECT use_name, use_user_type FROM user WHERE use_id = %s" % (get_user_id(get_token())))
            return render_template('private/myadoptions.html', user = user, pets = adoptions)
    else:
        return render_template('errors/403.html')

@users.route('/users/me/pets/')
def user_pets():
    if validate(get_token()):
        pets = select("SELECT pet_id, pet_name, pet_user_id, pet_age, pet_state, pst_detail, pty_detail, pet_race, pet_created, pet_updated, pet_description, (SELECT pim_url FROM pet_image WHERE pim_pet_id = pet_id LIMIT 1) as pet_image FROM pet, pet_state, pet_type WHERE pet_user_id = %i AND pet_state = pst_id AND pet_type = pty_id" % (get_user_id(get_token())))
        if request_wants_json():
            return format_json(pets)
        else:
            user = select("SELECT use_name, use_user_type FROM user WHERE use_id = %s" % (get_user_id(get_token())))
            return render_template('private/mypets.html', user = user, pets = pets, script = ['js/private/mypets.js'])
    else:
        return return_forbidden()

@users.route('/users/me/edit', methods = ['GET'])
def edit_user():
    if validate(get_token()):
        if request.method == 'GET':
            user = select("SELECT u.use_name, u.use_user_type, u.use_email, u.use_phone_number, s.sta_id, s.sta_name, t.uty_detail, c.cou_name FROM user u, state s, user_type t, country c WHERE c.cou_id=s.sta_country_id AND t.uty_id=u.use_user_type AND u.use_state_id=s.sta_id AND u.use_id = %s" % (get_user_id(get_token())))
            return render_template('private/edit_user.html', user = user, script = ['js/private/edit_user.js','bower_components/jsSHA/src/sha.js'])
        else:
            return render_template('errors/403.html')
    else:
        return render_template('errors/403.html')

@users.route('/users/me/messages/', methods=['GET', 'POST'])
def get_destinations():
    if validate(get_token()):
        if request.method == 'GET':
            if request_wants_json():
                data = select("SELECT mes_id, mes_user_to, mes_user_from, mes_message, mes_status FROM message, user WHERE mes_user_from = %i OR mes_user_to = %i GROUP BY mes_id" % (get_user_id(get_token()), get_user_id(get_token())))
                return format_json(data)
            else:
                user = select("SELECT use_name, use_user_type, use_id FROM user WHERE use_id = %s" % (get_user_id(get_token())))
                data = select("SELECT use_name, use_id, max(mes_date) as mes_date FROM message, (SELECT use_name, use_id FROM message, user WHERE (mes_user_to = %i OR mes_user_from = %i) AND (mes_user_to = use_id OR mes_user_from = use_id) GROUP BY use_id ORDER BY mes_date DESC) as tb WHERE (mes_user_from = use_id OR mes_user_to = use_id) AND use_id <> %i GROUP BY use_id ORDER BY mes_date DESC" % (get_user_id(get_token()), get_user_id(get_token()), get_user_id(get_token())))
                return render_template('private/messages.html', user = user, messages = data, script = ['js/private/messages.js'])
        elif request.method == 'POST':
            to = request.form['to']
            message = request.form['message']
            message_id = insert("INSERT INTO message(mes_user_from, mes_user_to, mes_message, mes_status, mes_date) VALUES(%i, %i, '%s', 'No leido', now())" % (get_user_id(get_token()), int(to), message))
            if message_id > 0:
                return format_json(select("SELECT * FROM message WHERE mes_id = %i" % (message_id)),201)
            return forma_json("",400)
    return return_forbidden()

@users.route('/users/me/messages/user/<int:user_id>/', methods=['GET'])
def get_messages(user_id):
    if validate(get_token()):
        data = select("SELECT mes_id, mes_message, mes_user_from, us2.use_name as user2, mes_user_to, us1.use_name as user1, mes_status, mes_date FROM message, user us1, user us2 WHERE ((mes_user_from = %i AND mes_user_to = %i) OR  (mes_user_from = %i AND mes_user_to = %i)) AND us1.use_id = mes_user_to AND us2.use_id = mes_user_from GROUP BY mes_id ORDER BY mes_id DESC" % (get_user_id(get_token()), int(user_id), int(user_id), get_user_id(get_token())))
        return format_json(data)
    return return_forbidden()