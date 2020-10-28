import json
import multiprocessing
import os
from typing import List

import click
from click.core import Option, Context
from prettytable import PrettyTable

from ..config.meta import __TITLE__, __VERSION__, __AUTHOR__, __AUTHOR_EMAIL__
from ..information import entrance_finder_version, entrance_finder_git_commit_id, entrance_finder_build_time
from ..method import find_multiple_entrances


# noinspection PyUnusedLocal
def print_version(ctx: Context, param: Option, value: bool):
    if not value or ctx.resilient_parsing:
        return
    click.echo('{title}, version {version}.'.format(title=__TITLE__.capitalize(), version=__VERSION__))
    click.echo('With entrance-finder, version {version}.'.format(version=entrance_finder_version))
    click.echo('Built at {time}, {commit}.'.format(
        time=entrance_finder_build_time, commit=entrance_finder_git_commit_id[:8]))
    click.echo('Developed by {author}, {email}.'.format(author=__AUTHOR__, email=__AUTHOR_EMAIL__))
    ctx.exit()


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)

_LINE_SEPARATOR_FOR_PRETTY_TABLE = "\n"


# noinspection PyUnusedLocal
def validate_concurrency(ctx: Context, param: Option, value: int):
    if value > 0:
        return value
    else:
        raise ValueError("Concurrency should be no less than 1.")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--version', is_flag=True,
              callback=print_version, expose_value=False, is_eager=True,
              help="Show package's version information.")
@click.option('-H', '--headless', is_flag=True, default=False,
              help='Do not show as a table, used when you need to use pipes.')
@click.option('-j', '--use_json', is_flag=True, default=False,
              help='Use json format to print the result.')
@click.option('-s', '--sorted_by',
              type=click.types.Choice(['entrance', 'package', 'class', 'file']), default='file',
              help='The order to sorted by.')
@click.option('-r', '--reverse', is_flag=True, default=False,
              help='Reverse the sorted result, only applied when -s is used.')
@click.option('-A', '--absolute', is_flag=True, default=False,
              help='Use absolute path to display file.')
@click.option('-n', '--concurrency', type=int, default=multiprocessing.cpu_count(), callback=validate_concurrency,
              help='Concurrency to do this calculation.')
@click.argument('sources', nargs=-1, type=click.types.Path(exists=True, readable=True))
def cli(sources: List[str],
        headless: bool, use_json: bool, absolute: bool,
        sorted_by: str, reverse: bool, concurrency: int):
    table = PrettyTable(['Entrance', 'Package', 'Class', 'File'])

    entrances = set(find_multiple_entrances(*sources, concurrency=concurrency))
    for entrance in entrances:
        filename = os.path.normpath(entrance.filename)
        table.add_row([
            entrance.entrance,
            entrance.package,
            entrance.class_name,
            filename if absolute else os.path.relpath(filename),
        ])

    if headless:
        table.header = False
        table.junction_char = ' '
        table.vertical_char = ' '
        table.horizontal_char = ' '
    else:
        table.title = "Result of entrance finder"

    table.sortby = sorted_by.capitalize()
    table.reversesort = reverse

    if use_json:
        json_result = json.loads(table.get_json_string())
        json_result = [{
            str(k).lower(): v for k, v in item.items()
        } for item in json_result if isinstance(item, dict)]
        click.echo(
            json.dumps(json_result, indent=4, separators=(",", ": "), sort_keys=True))
    else:
        str_result = table.get_string()
        lines = str_result.split(_LINE_SEPARATOR_FOR_PRETTY_TABLE)
        lines = [line for line in lines if line.strip()]
        str_result = os.linesep.join(lines)
        click.echo(str_result)
