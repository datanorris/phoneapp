from jsonschema import validate
from flask import (Blueprint, request, jsonify)
bp = Blueprint('Customer', __name__, url_prefix='/customer')

from db import get_db

create_schema = {
    'type': 'object',
    'properties': {
        'customerName': { 'type': 'string', 'minLength': 1, 'maxLength': 200 },
        'customerPhoneNumber': { 'type': 'string', 'pattern': '^[0-9]{11}$' }
    },
    'required': ['customerName', 'customerPhoneNumber']
}

@bp.route('/create', methods=['POST'])
def create():
    db = get_db()

    new_cust = request.get_json()
    validate(new_cust, create_schema)

    db.execute('INSERT INTO customer (customerName, customerPhoneNumber) VALUES (?, ?)',
               (new_cust['customerName'],
                new_cust['customerPhoneNumber']))
    db.commit()

    return ""

# input (query string)
#   phonePrefix = <string>
#   <optional> maxResults = <+ve int>
#
# implement maximum 100 results here
@bp.route('/search-by-phone-prefix')
def search_by_phone_prefix():
    db = get_db()

    phonePrefix = request.args['phonePrefix']
    maxResults = int(request.args.get('maxResults',100))

    if maxResults <= 0 or maxResults > 100:
        maxResults = 100

    rs = db.execute(
        """
        SELECT customerId, customerName, customerPhoneNumber
        FROM customer \
        WHERE customerPhoneNumber LIKE ? || '%'
        ORDER BY customerPhoneNumber
        LIMIT ?
        """, (phonePrefix, maxResults))

    # unacceptable solution for larger result sets, but this service will be limited to small ones
    return jsonify(
      [{"customerId": r[0],
        "customerName": r[1],
        "customerPhoneNumber": r[2]}
       for r in rs.fetchall()])