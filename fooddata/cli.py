import json as jsonp
import shutil

import click

from .db import create_views, load_categories, load_food, load_nutrients, run_query
from .download import download_data

DEFAULT_SOURCE_URL = 'https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_csv_2020-04-29.zip'


@click.group()
def cli():
    """
    Download and build USDA food database
    """
    pass


@cli.command()
@click.option('--db-path', default="data.db")
@click.option('--source', default=DEFAULT_SOURCE_URL)
def build(db_path: str, source: str):
    """
    Download food data from USDA website and build database
    """

    destination_dir = download_data(source)
    click.echo(click.style('Successfully downloaded data', fg='green', bold=True))

    click.echo('Loading categories into DB')
    load_categories(db_path, destination_dir)
    click.echo('Loading food into DB')
    load_food(db_path, destination_dir)
    click.echo('Loading nutrients into DB')
    load_nutrients(db_path, destination_dir)
    click.echo('Creating views in DB')
    create_views(db_path)
    click.echo(click.style('Database successfully built', fg='green', bold=True))

    shutil.rmtree(destination_dir)


@cli.command()
@click.argument('query')
@click.option('--db-path', default="data.db")
@click.option('--json/--no-json', default=False)
def query(query: str, db_path: str, json: bool):
    """
    Query database
    Args:
        query:
        json:

    Returns:

    """
    rows = run_query(db_path, query)

    formatted_rows = [dict(row) for row in rows]
    if json:
        click.echo(jsonp.dumps(formatted_rows))
    else:
        click.echo(formatted_rows)


if __name__ == '__main__':
    cli()
