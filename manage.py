#!/usr/bin/env python3
import os

import click

import finances


@click.group()
def cli():
    pass


@cli.command()
def run():
    click.secho('Running server for Finances', fg='green')
    finances.app.run(debug=True, reloader=True)


@cli.command()
def test():
    os.system(
        'nosetests --cover-package=finances '
        '--cover-erase --with-coverage --with-doctest'
    )


@cli.command()
@click.option('--silently', '-s', is_flag=True)
def init(silently):
    click.secho("Init database done", fg='green')
    init_db(silently)


def init_db(silently=False):
    models = finances.models
    for model in [
        models.User,
        models.Account,
    ]:
        model.create_table(silently)


if __name__ == '__main__':
    cli()
