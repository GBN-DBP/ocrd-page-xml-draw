import click
from ocrd.decorators import ocrd_cli_options, ocrd_cli_wrap_processor

from ocrd_page_xml_draw.main import OcrdPageXmlDraw


@click.command()
@ocrd_cli_options
def ocrd_page_xml_draw(*args, **kwargs):
    return ocrd_cli_wrap_processor(OcrdPageXmlDraw, *args, **kwargs)