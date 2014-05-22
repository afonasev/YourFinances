#!/usr/bin/env python3
import os
import logging

import click
import peewee

from finances import app
from finances import models


logger = logging.getLogger('peewee')
logger.setLevel(logging.FATAL)
logger.addHandler(logging.StreamHandler())


@click.group()
def cli():
    pass


@cli.command(help='Init database')
@click.option('--db', default=app.config['database'])
@click.option('--silently', is_flag=True, help='Fail silently mod, default=OFF')
@click.option('--clean', is_flag=True, help='Clean database if it exist, default=OFF')
def init(db, silently, clean):
    if clean:
        os.remove(db)
        print('Database was removed: %s' % db)

    app_base_init(db)

    print('Init database: %s' % db)
    for model in [models.User, models.Category, models.CategoryType]:
        model.create_table(silently)


@cli.command(help='Running server for Finances web application')
@click.option('--db', default=app.config['database'])
@click.option('--host', default='localhost', help='Default=localhost')
@click.option('--port', default=8080, help='Default=8080')
@click.option('--reloader', is_flag=True, help='Reloader mod, default=OFF')
@click.option('--debug', is_flag=True, help='Debug mod, default=OFF')
def run(db, debug, reloader, host, port):
    print('Running server for Finances web application')
    app_base_init(db)
    app.run(host=host, port=port, debug=debug, reloader=reloader, interval=0.5)


@cli.command(help='Do something')
@click.option('--db', default=app.config['database'])
def do(db):
    app_base_init(db)
    m = models.Category.get(name='sdfgdg')
    # m.save()
    print(m.type)


@cli.command(help='Run auto tests')
def test():
    os.system(r'../scripts/run_tests.sh finances')


def app_base_init(db):
    database = peewee.SqliteDatabase(db)
    models.database.initialize(database)


if __name__ == '__main__':
    try:
        cli()
    except Exception as exc:
        print('ERROR: %s!' % exc)
