from flask import Blueprint
from Model import select
from Response import (
    format_json,
    request_wants_json
)
from flask import(
    request,
    render_template
)
from Auth import *

pets = Blueprint('pets', __name__)

@pets.route('/')
@pets.route('/pets/', methods = ['GET', 'POST'])
def get_pets():
    if request.method == 'GET':
        data = select("SELECT pet_id, pet_name, pet_age, pet_type, use_name FROM user, pet WHERE pet_state = 2 and pet_user_id = use_id")
        if validate(get_token()):
            user = select("SELECT use_name FROM user WHERE use_id = %s" % (get_user_id(get_token())))
        if request_wants_json():
            return format_json(data)
        return render_template('index.html', user = user)
    else:
        return "POST"

@pets.route('/pets/<int:pet_id>', methods = ['GET', 'PUT', 'DELETE'])
def get_pet(pet_id):
    if request.method == 'GET':
        data = select("SELECT pet_id, pet_name, pet_age, pet_type, use_name FROM user, pet WHERE pet_state = 2 and pet_user_id = use_id and pet_id = %s" % (pet_id))
        return format_json(data)
    elif request.method == 'PUT':
        return 'PET UPDATED'
    else:
        return 'PET DELETED'

@pets.route('/pets/<int:pet_id>/image/', methods = ['GET'])
def get_pet_images(pet_id):
    data = select("SELECT pim_id, pim_url FROM pet_image WHERE pim_pet_id = %s" % (pet_id))
    return format_json(data)

@pets.route('/pets/<int:pet_id>/image/<int:image_id>/', methods = ['GET'])
def get_pet_image(pet_id,image_id):
    data = select("SELECT pim_id, pim_url FROM pet_image WHERE pim_id = %s and pim_pet_id = %s" % (image_id, pet_id))
    return format_json(data)


@pets.route('/pages/pets/', methods = ['GET'])
def pets_page():
    return get_pets()