from flask import(
    Blueprint,
    current_app,
    redirect,
    url_for
)
from Model import(
    select,
    insert,
    update
)
from Response import (
    format_json,
    request_wants_json
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
        data = select("SELECT pet_id, pet_name, pet_age, pet_type, use_name, pet_description, (SELECT pim_url FROM pet_image WHERE pim_pet_id = pet_id LIMIT 1) as pet_image FROM user, pet WHERE pet_state = 2 and pet_user_id = use_id ORDER BY pet_id DESC LIMIT %i,%i" % (page*ITEMS_PER_PAGE, ITEMS_PER_PAGE))
        total = int(ceil(select("SELECT count(pet_id) as total FROM pet")[0]['total']/ITEMS_PER_PAGE))
        if page > total:
            return redirect(url_for('pets.get_pets'))
        if request_wants_json():
            return format_json(data)
        else:
            if validate(get_token()):
                user = select("SELECT use_name, use_user_type FROM user WHERE use_id = %s" % (get_user_id(get_token())))
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

def set_select():#por mientras
    count = get_countries();
    return render_template('index.html', count=count)

@pets.route('/pets/<int:pet_id>/', methods = ['GET', 'PUT', 'DELETE'])
def get_pet(pet_id):
    if request.method == 'GET':
        data = select("SELECT pet_id, pet_name, pet_age, pet_type, use_name FROM user, pet WHERE pet_state = 2 and pet_user_id = use_id and pet_id = %s" % (pet_id))
        if request_wants_json():
            return format_json(data)
        else:
            user = select("SELECT use_name, use_user_type FROM user WHERE use_id = %s" % (get_user_id(get_token())))
            return render_template('private/pet.html', user = user, pet = data)
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
        return 'PET DELETED'
    return render_template('errors/403.html')

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
    
@pets.route('/pets/types/', methods = ['GET'])
def get_pets_types():
    data = select("SELECT * FROM pet_type")
    return format_json(data)

@pets.route('/pets/<int:pet_id>/edit/', methods = ['GET'])
def edit_pet(pet_id):
    if validate(get_token()):
        user = select("SELECT use_name, use_user_type FROM user WHERE use_id = %s" % (get_user_id(get_token())))
        pet = select("SELECT pet_id, pet_name, pet_user_id, pet_age, pet_state, pst_detail, pet_type, pty_detail, pet_race, pet_created, pet_updated, pet_description FROM pet, pet_state, pet_type WHERE pet_id = %i AND pet_state = pst_id AND pet_type = pty_id AND pet_user_id = %s AND (pet_state = 1 OR pet_state = 2 OR pet_state = 3)" % (pet_id, get_user_id(get_token())))
        if len(pet) > 0:
            return render_template('private/edit_pet.html', user = user, script = ['js/private/edit_pet.js'], pet = pet)
    return render_template('errors/403.html')