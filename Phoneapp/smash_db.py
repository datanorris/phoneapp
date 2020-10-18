import os
import sqlite3
import random

import click
from flask import current_app
from flask.cli import with_appcontext
import requests

from db import get_db

TARGET = 5000
INCR = 100
TARGET2 = 40 * 1000 * 1000

@click.command('smash-db')
@with_appcontext
def smash_db_command():
    db = get_db()
    svc_phoneapi = current_app.config['SVC_PHONEAPI']

    #click.echo('Deleting rows...')
    #db.execute('DELETE FROM customer')
    #db.commit()
    
    current_rows = db.execute('SELECT count(*) FROM customer').fetchone()[0]
    click.echo(f'Current number of rows: {current_rows}')

    click.echo('Inserting rows...')

    while current_rows < TARGET - INCR:
        for i in range(INCR):
            ph = f'{random.randint(1,100000000000):011}'

            #requests.post(svc_phoneapi + '/create-customer',
            #              json={'customerName': f'name {ph}',
            #                    'customerPhoneNumber': ph})

            db.execute('INSERT INTO customer (customerName, customerPhoneNumber) VALUES (?, ?)',
                       (f'name {ph}', ph))
            db.commit()

        current_rows = current_rows + INCR
        click.echo(current_rows)

    while current_rows < TARGET2 / 2:
        db.execute('''
                   INSERT INTO customer (customerName, customerPhoneNumber)
                   SELECT customerName, customerPhoneNumber
                   FROM customer
                   ''')
        db.commit()
        current_rows = current_rows * 2
        click.echo(current_rows)

    click.echo('Inserting rows done')

    updated_rows = db.execute('SELECT count(*) FROM customer').fetchone()[0]
    click.echo(f'Updated number of rows: {updated_rows}')

    click.echo(f'Querying for 012*...')
    
    import time
    startTime = time.time()
    resp = requests.get(svc_phoneapi + '/customer-search-by-phone-prefix',
                        params = { 'phonePrefix': "012", 'maxResults': 10 })
    executionTime = (time.time() - startTime)

    click.echo(resp.text)
    click.echo(f'Query completed in {executionTime} seconds')

def init_app(app):
    app.cli.add_command(smash_db_command)