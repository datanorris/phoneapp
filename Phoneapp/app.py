import os
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

import db
db.init_app(app)

import smash_db
smash_db.init_app(app)

from services import (customer, phoneAPI)
app.register_blueprint(customer.bp)
app.register_blueprint(phoneAPI.bp)

# Visual Studio project code for debugging
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    #try:
    #    PORT = int(os.environ.get('SERVER_PORT', '5555'))
    #except ValueError:
    #    PORT = 5555
    PORT = 5000
    app.run(HOST, PORT)
