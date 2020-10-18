from jsonschema import (validate, ValidationError)
import requests
from flask import (Blueprint, current_app, request)
bp = Blueprint('PhoneAPI', __name__, url_prefix='/phoneAPI')

create_customer_schema = {
    'type': 'object',
    'properties': {
        'customerName': { 'type': 'string', 'minLength': 1, 'maxLength': 200 },
        'customerPhoneNumber': { 'type': 'string', 'pattern': '^[0-9]{11}$' }
    },
    'required': ['customerName', 'customerPhoneNumber']
}

@bp.route('/create-customer', methods=['POST'])
def create_customer():
    svc_customer = current_app.config['SVC_CUSTOMER']

    new_cust = request.get_json()
    validate(new_cust, create_customer_schema)

    resp = requests.post(svc_customer + '/create', json=new_cust)
    return resp.text, resp.status_code, resp.headers.items()

# input (query string)
#   phonePrefix = <string>
#   <optional> maxResults = <+ve int>
#
# implement maximum 10 results here
@bp.route('/customer-search-by-phone-prefix')
def customer_search_by_phone_prefix():
    svc_customer = current_app.config['SVC_CUSTOMER']

    phonePrefix = request.args['phonePrefix']
    maxResults = int(request.args.get('maxResults',10))

    if maxResults <= 0 or maxResults > 10:
        maxResults = 10

    resp = requests.get(svc_customer + '/search-by-phone-prefix',
                        params = { 'phonePrefix': phonePrefix, 'maxResults': maxResults })
    return resp.text, resp.status_code, resp.headers.items()

@bp.app_errorhandler(ValidationError)
def handle_validation_error(error):
    return str(error), 500