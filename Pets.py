from flask import(
    Blueprint,
    current_app,
    redirect,
    url_for
)
from Model import(
    select,
    insert,
    update,
    delete
)
from Response import (
    format_json,
    request_wants_json,
    return_forbidden
)
from Countries import (
    get_countries
)
from flask import(
    request,
    render_template
)
from Auth import *
import os

from math import ceil

pets = Blueprint('pets', __name__)

ITEMS_PER_PAGE = 20

@pets.route('/')
@pets.route('/pets/', methods = ['GET', 'POST'])
@pets.route('/pets/page/<int:page>/', methods = ['GET'])
def get_pets(page = 0):
    if request.method == 'GET':
        data = select("SELECT pet_id, pet_name, pet_age, pty_detail, pet_user_id, use_name, pet_description, (SELECT pim_url FROM pet_image WHERE pim_pet_id = pet_id LIMIT 1) as pet_image FROM user, pet, pet_type WHERE pty_id = pet_type AND pet_state = 2 AND pet_user_id = use_id ORDER BY pet_id DESC LIMIT %i,%i" % (page*ITEMS_PER_PAGE, ITEMS_PER_PAGE))
        total = int(ceil(select("SELECT count(pet_id) as total FROM pet")[0]['total']/ITEMS_PER_PAGE))
        if page > total:
            return redirect(url_for('pets.get_pets'))
        if request_wants_json():
            return format_json(data)
        else:
            if validate(get_token()):
                user = select("SELECT use_name, use_user_type, use_id FROM user WHERE use_id = %s" % (get_user_id(get_token())))
                return render_template('index.html', user = user, script = ['js/public/index.js'], pets = data, total = total, page = page)
            else:
                return render_template('index.html', script = ['js/public/index.js'], pets = data, total = total, page = page)
    else:
        name = request.form['name']
        age = request.form['age']
        pet_type = request.form['type']
        race = request.form['race']
        description = request.form['description']
        if name and age and pet_type and race:
            pet_id = insert("INSERT INTO pet(pet_name, pet_age, pet_user_id, pet_state, pet_type, pet_race, pet_description, pet_created, pet_updated) VALUES('%s', '%s', %i, 1, %i, '%s', '%s', now(), now())" % (name, age, get_user_id(get_token()), int(pet_type), race, description))
            return format_json({'pet_id': pet_id},201)
        else:
            return format_json(name, 400)

@pets.route('/pets/<int:pet_id>/', methods = ['GET', 'PUT', 'DELETE'])
def get_pet(pet_id):
    if request.method == 'GET':
        if validate(get_token()):            
            user = select("SELECT use_id, use_name, use_user_type FROM user WHERE use_id = %s" % (get_user_id(get_token())))
            if user[0]['use_user_type'] < 3 or user[0]['use_id'] == pet[0]['pet_user_id']:
                data = select("SELECT pet_id, pet_name, pet_age, pet_type, use_name, pet_user_id, pet_race, pty_detail, pet_created, pet_description, pet_state FROM user, pet, pet_type WHERE pty_id = pet_type AND (pet_state = 2 OR pet_state = 3) AND pet_user_id = use_id AND pet_id = %s" % (pet_id))
        else:
            data = select("SELECT pet_id, pet_name, pet_age, pet_type, use_name, pet_user_id, pet_race, pty_detail, pet_created, pet_description, pet_state FROM user, pet, pet_type WHERE pty_id = pet_type AND pet_state = 2 AND pet_user_id = use_id AND pet_id = %s" % (pet_id))
        images = select("SELECT pim_id, pim_url FROM pet_image WHERE pim_pet_id = %s" % (pet_id))
        comments = select('SELECT que_id, use_name, que_question, que_answer, que_date FROM question, user WHERE que_pet = %i AND que_user = use_id ORDER BY que_date DESC' % (int(pet_id)))
        if request_wants_json():
            return format_json(data)
        else:
            if validate(get_token()):
                return render_template('public/pet.html', user = user, pet = data[0], images = images, comments = comments, script = ['js/public/pet.js'])
            else:
                return render_template('public/pet.html', pet = data[0], images = images, comments = comments, script = ['js/public/pet.js'])
    elif request.method == 'PUT' and validate(get_token()):
        name = request.form['name']
        age = request.form['age']
        pet_type = request.form['type']
        race = request.form['race']
        description = request.form['description']        
        affected = update("UPDATE pet SET pet_name='%s', pet_age='%s', pet_type=%i, pet_race='%s', pet_description='%s', pet_updated=now(), pet_state = 2 WHERE pet_id = %i" % (name, age, int(pet_type), race, description, int(pet_id)))
        if affected > 0:
            return format_json("")
        return format_json("",400)
    elif request.method == 'DELETE' and validate(get_token()):
        result = update("UPDATE pet SET pet_state = 4 WHERE pet_id = %i" % (int(pet_id)))
        if result > 0:
            return format_json("", 200)
        return format_json("",400)
    return render_template('errors/403.html')

@pets.route('/pets/<int:pet_id>/questions/', methods = ['GET', 'POST'])
def get_pets_questions(pet_id):
    if request.method == 'GET':
        data = select('SELECT que_id, use_name, que_question, que_date FROM question, user WHERE que_pet = %i AND que_user = use_id ORDER BY que_date DESC' % (int(pet_id)))
        return format_json(data);
    else:
        if(validate(get_token())):
            question = request.form['question']
            if question:
                question_id = insert("INSERT INTO question(que_user, que_pet, que_question, que_date) VALUES(%i,%i,'%s', now())" % (get_user_id(get_token()), int(pet_id), question))
                if question_id > 0:
                    return format_json(select('SELECT que_id, use_name, que_question FROM question, user WHERE que_pet = %i AND que_user = use_id AND que_id = %i' % (int(pet_id), question_id)), 201)
        return format_json("", 400)
    return format_json("No has iniciado sesion", 403)

@pets.route('/pets/<int:pet_id>/questions/<int:question_id>/', methods = ['GET', 'PUT', 'DELETE'])
def get_pets_question(pet_id, question_id):
    if request.method == 'GET':
        data = select('SELECT que_id, use_name, que_question, que_answer, que_date FROM question, user WHERE que_pet = %i AND que_user = use_id AND que_id = %i ORDER_BY que_date DESC' % (int(pet_id), int(question_id)))
        return format_json(data);
    elif request.method == 'PUT':
        answer = request.form['answer']
        if validate(get_token()):
            if answer:
                pet = select("SELECT pet_id FROM pet WHERE pet_id = %i AND pet_user_id = %i" % (int(pet_id), get_user_id(get_token())))
                if len(pet) > 0:
                    result = update("UPDATE question SET que_answer = '%s' WHERE que_id = %i " % (answer, question_id))
                    if result > 0:
                        data = select('SELECT que_id, use_name, que_question, que_answer FROM question, user WHERE que_pet = %i AND que_user = use_id AND que_id = %i' % (int(pet_id), int(question_id)))
                        return format_json(data,200)
                    return format_json("",400)
                return format_joson("",403)
            return format_json("",400)
        return format_json("",403)
    elif validate(get_token()):
        user = select("SELECT use_id, use_name, use_user_type FROM user WHERE use_id = %s" % (get_user_id(get_token())))
        if user[0]['use_user_type'] < 3:
            result = delete("DELETE FROM question WHERE que_id = %i" % (int(question_id)))
            if result > 0:
                return format_json("");
        return format_json("",403)
        

    
@pets.route('/pets/<int:pet_id>/images/', methods = ['GET', 'POST'])
def get_pet_images(pet_id):
    if request.method == 'GET':
        data = select("SELECT pim_id, pim_url FROM pet_image WHERE pim_pet_id = %s" % (pet_id))
        return format_json(data)
    elif request.method == 'POST' and validate(get_token()):
        check = select("SELECT * FROM pet WHERE pet_id = %i AND pet_user_id = %i" % (int(pet_id), get_user_id(get_token())))
        if len(check) > 0:
            file = request.files['file']
            filename = str(pet_id)+"_"+file.filename
            file.save(os.path.join(current_app.config.get('UPLOAD_FOLDER'), filename))
            image_id = insert("INSERT INTO pet_image(pim_url, pim_pet_id) VALUES('%s', %i)" % (filename, int(pet_id)))
            data = select("SELECT * FROM pet_image WHERE pim_id = %i" % (image_id))
            return format_json(data, 201)
    return render_template('errors/403.html')
        

@pets.route('/pets/<int:pet_id>/images/<int:image_id>/', methods = ['GET', 'PUT', 'DELETE'])
def get_pet_image(pet_id,image_id):
    data = select("SELECT pim_id, pim_url FROM pet_image WHERE pim_id = %s and pim_pet_id = %s" % (image_id, pet_id))
    return format_json(data)


@pets.route('/pets/new/', methods = ['GET'])
def new_pet():
    if validate(get_token()):
        user = select("SELECT use_name, use_user_type FROM user WHERE use_id = %s" % (get_user_id(get_token())))
        return render_template('private/new_pet.html', user = user, script = ['js/private/new_pet.js'])
    else:
        return render_template('errors/403.html')
    
@pets.route('/pets/types/', methods = ['GET', 'POST'])
def get_pets_types():
    data = select("SELECT * FROM pet_type")
    if request.method == 'GET' and request_wants_json():
        return format_json(data)
    elif validate(get_token()):
        if request.method == 'GET':
            if get_perfil(get_token()) == 1:
                user = select("SELECT use_name, use_user_type FROM user WHERE use_id = %s" % (get_user_id(get_token())))
                return render_template('private/species.html', user = user, species = data, script = ['js/private/species.js'])
        if request.method == 'POST':
            name = request.form['specie']
            type_id = insert("INSERT INTO pet_type(pty_detail) VALUES ('%s')" % (name))
            if type_id > 0:
                data = select("SELECT * FROM pet_type WHERE pty_id = %i" % (type_id))
                return format_json(data,201)
        return format_json("", 400)
    return return_forbidden()
        

@pets.route('/pets/<int:pet_id>/edit/', methods = ['GET', 'PUT'])
def edit_pet(pet_id):
    if validate(get_token()):
        user = select("SELECT use_name, use_user_type FROM user WHERE use_id = %s" % (get_user_id(get_token())))
        pet = select("SELECT pet_id, pet_name, pet_user_id, pet_age, pet_state, pst_detail, pet_type, pty_detail, pet_race, pet_created, pet_updated, pet_description FROM pet, pet_state, pet_type WHERE pet_id = %i AND pet_state = pst_id AND pet_type = pty_id AND pet_user_id = %s AND (pet_state = 1 OR pet_state = 2 OR pet_state = 3)" % (pet_id, get_user_id(get_token())))
        if request.method == 'GET':
            user = select("SELECT use_name, use_user_type FROM user WHERE use_id = %s" % (get_user_id(get_token())))
            if len(pet) > 0:
                return render_template('private/edit_pet.html', user = user, script = ['js/private/edit_pet.js'], pet = pet)
        elif user[0]['use_user_type'] < 3 or user[0]['use_id'] == pet[0]['pet_user_id']:
            state = request.form['state']
            result = update("UPDATE pet SET pet_state = %i WHERE pet_id = %i" % (int(state), int(pet_id)))
            if result > 0:
                return format_json("", 200)
            return format_json("", 400)
    return render_template('errors/403.html')

@pets.route('/pets/<int:pet_id>/adopt/', methods = ['GET', 'POST', 'DELETE', 'PUT'])
def adopt_pet(pet_id):
    if validate(get_token()):
        pet = select("SELECT pet_id, pet_name, pet_age, pet_type, use_name, pet_user_id, pet_race, pty_detail, pet_created, pet_description, (SELECT pim_url FROM pet_image WHERE pim_pet_id = pet_id LIMIT 1) as pet_image FROM user, pet, pet_type WHERE pty_id = pet_type AND pet_user_id = use_id AND pet_id = %s" % (pet_id))
        user_own = select("SELECT use_name, use_user_type, use_id, use_phone_number, use_email FROM user WHERE use_id = %s" % (pet[0]['pet_user_id']))
        adoption = select("SELECT ado_user_request, ado_pet_id, ado_state, ado_created, ado_updated, ast_detail, ast_id FROM adoption, adoption_state WHERE ado_pet_id = %i AND ast_id = ado_state" % (int(pet_id)))
        user = select("SELECT use_name, use_user_type, use_id FROM user WHERE use_id = %s" % (get_user_id(get_token())))   
        if request.method == 'GET' and adoption:    
            user_req = select("SELECT use_name, use_user_type, use_id, use_phone_number, use_email FROM user WHERE use_id = %s" % (adoption[0]['ado_user_request']))
            if pet[0]['pet_user_id'] == get_user_id(get_token()) or adoption[0]['ado_user_request'] == get_user_id(get_token()):
                return render_template('private/adopt.html', pet = pet[0], script = ['js/private/adopt.js'], user = user, adoption = adoption[0], user2 = user_own[0], user3 = user_req[0])
        elif request.method == 'POST':
            if pet[0]['pet_user_id'] != get_user_id(get_token()):
                adopt_id = insert("INSERT INTO adoption(ado_user_request, ado_pet_id, ado_state, ado_created, ado_updated) VALUES(%i,%i,1,now(),now())" % (get_user_id(get_token()), int(pet_id)))
                upd = update("UPDATE pet SET pet_state = 6 WHERE pet_id = %i" % (int(pet_id)))
                if len(select("SELECT * FROM adoption WHERE ado_pet_id = %i" % (int(pet_id)))) > 0:
                    return format_json("",201)
            return format_json("",400)
        elif request.method == 'DELETE':
            if pet[0]['pet_user_id'] == get_user_id(get_token()) or adoption[0]['ado_user_request'] == get_user_id(get_token()):
                result = delete("DELETE FROM adoption WHERE ado_pet_id = %i" % (int(pet_id)))
                upd = update("UPDATE pet SET pet_state = 2 WHERE pet_id = %i" % (int(pet_id)))
                if result > 0:
                    return format_json("")
                return format_json("",400)
        else:
            if pet[0]['pet_user_id'] == get_user_id(get_token()) or adoption[0]['ado_user_request'] == get_user_id(get_token()):
                upd = update("UPDATE adoption SET ado_state = 3 WHERE ado_pet_id = %i" % (int(pet_id)))
                upd2 = update("UPDATE pet SET pet_state = 5 WHERE pet_id = %i" % (int(pet_id)))
                if upd > 0 and upd2 > 0:
                    return format_json("")
                return format_json("",400)
    return return_forbidden()

    
