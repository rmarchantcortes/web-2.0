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

countries = Blueprint('countries', __name__)

@countries.route('/countries/', methods = ['GET'])
def get_countries():
    data = select("SELECT * FROM country")
    return format_json(data)

@countries.route('/countries/<int:country_id>/', methods = ['GET'])
def get_country(country_id):
    data = select("SELECT * FROM country WHERE cou_id = %i" % (country_id))
    return format_json(data)

@countries.route('/countries/<int:country_id>/states/', methods = ['GET'])
def get_states(country_id):
    data = select("SELECT sta_id, sta_name FROM state WHERE sta_country_id = %i" % (country_id))
    return format_json(data)