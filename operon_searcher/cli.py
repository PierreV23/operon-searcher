from pathlib import Path
from pprint import pprint, pformat
import typer
from operon_searcher.gene import genomic_parser
from operon_searcher.searcher import search_operons

from operon_searcher.tf import fimo_parser
from operon_searcher.visualize import visualize_operons

app = typer.Typer()

@app.command()
def main(
    folder: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True),
    visualize: bool = typer.Option(
        False,
        "-v",
        "--visualize",
        help="Visualizes found operons."
    ),
    do_print: bool = typer.Option(
        False,
        "-p",
        "--print",
        help="Print out found operons."
    ),
):
    binding_sites = fimo_parser(folder)
    genes = genomic_parser(folder)
    operons = search_operons(binding_sites, genes)
    if visualize:
        visualize_operons(operons)
    if do_print:
        typer.echo(pformat(tuple(operons.items())))



# TODO:
# - --color-tfbs
# - --color-gene
# - --circular
# settings die in searcher.py staan

