import click

from mkite_core.cli.runner import run


class MkiteGroup(click.Group):
    pass


@click.command(cls=MkiteGroup)
def kite():
    """Command line interface for mkite_core"""


kite.add_command(run)

if __name__ == "__main__":
    kite()
