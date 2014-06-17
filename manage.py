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

db_path = app.config['database']


@click.group()
def cli():
    pass


@cli.command()
@click.option('--silently', is_flag=True)
@click.option('--remove', is_flag=True)
def init(silently, remove):
    if remove:
        os.remove(db_path)
        msg = click.style("Database was removed: %s" % db_path, fg='red')
        click.echo(msg)

    app_base_init()

    msg = click.style("Init database: %s" % db_path, fg='green')
    click.echo(msg)

    for model in [
        models.User,
        models.Category,
        models.SubCategory,
        models.Transaction,
    ]:
        model.create_table(silently)


@cli.command()
def run():
    msg = click.style("Running server for Finances web application", fg='green')
    click.echo(msg)

    app_base_init()
    app.run(debug=True, reloader=True, interval=0.5)


@cli.command()
def test():
    os.system(
        r'nosetests --cover-package=finances'
        r'--cover-erase --with-coverage --with-doctest'
    )


def app_base_init():
    database = peewee.SqliteDatabase(db_path)
    models.database.initialize(database)


if __name__ == '__main__':
    try:
        cli()
    except Exception as exc:
        click.echo(click.style("ERROR: %s!" % exc, fg='red'))
