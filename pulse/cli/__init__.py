"""CLI interface module"""

import click

from pulse.notification import send_notification


@click.group(commands=[])
@click.version_option(None, "--version", package_name="pulse")
@click.pass_context
def cli(context=None) -> None:
    """CLI Runner group"""
    click.echo("Hola maquinola")
    send_notification("HOLA LOCOOO")


if __name__ == "__main__":
    cli()
