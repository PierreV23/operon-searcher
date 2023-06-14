from pathlib import Path
from pprint import pprint, pformat
from typing import Annotated, Optional
import typer
from operon_searcher import searcher, visualizer
from operon_searcher.gene import genomic_parser
from operon_searcher.searcher import search_operons

from operon_searcher.tf import fimo_parser
from operon_searcher.visualizer import visualize_operons

import rich

app = typer.Typer()

@app.command()
def main(
    folder: Annotated[Optional[Path], typer.Argument(..., exists=True, file_okay=False, dir_okay=True)] = None,
    do_visualize: bool = typer.Option(
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
    fimo_file: Path = typer.Option(
        None,
        "-f",
        "--fimo",
        help="Specify the .gff file containing the fimo results.",
        file_okay=True
    ),
    genomic_file: Path = typer.Option(
        None,
        "-g",
        "--genes",
        help="Specify the .gff file containing the genes.",
        file_okay=True
    ),
    site_gap: int = typer.Option(
        300,
        "--site-gap",
        help="Biggest allowed gap first gene found behind binding site.",
    ),
    gene_gap: int = typer.Option(
        200,
        "--gene-gap",
        help="Biggest allowed gap between genes to count it was an operon.",
    ),
    batch_size: int = typer.Option(
        30,
        "--batch-size",
        help="Amount of fimo hits to be tried, sorted on p-value.",
    ),
    max_fails: int = typer.Option(
        5,
        "--max-fails",
        help="Maximum allowed consecutive failed hits."
    ),
    tfbs_color: str = typer.Option(
        "#ffd700",
        "--tfbs-color",
        help="Color of binding site when visualizing."
    ),
    gene_color: str = typer.Option(
        "#cffccc",
        "--gene-color",
        help="Color of gene when visualizing."
    ),

):
    searcher.GENE_OPERON_MAX_GAP          = gene_gap
    searcher.FIMO_BATCH_SIZE              = batch_size
    searcher.GENE_TO_BINDING_SITE_MAX_GAP = site_gap
    searcher.MAX_FAILED_HITS              = max_fails

    visualizer.TFBS_COLOUR = tfbs_color
    visualizer.GENE_COLOUR = gene_color

    if folder is None and (fimo_file is None or genomic_file is None):
        # Raise exception or something...
        ...
    if fimo_file is None:
        fimo_file = folder / 'fimo.gff'
    binding_sites = fimo_parser(fimo_file)
    if genomic_file is None:
        genomic_file = folder / 'genomic.gff'
    genes = genomic_parser(genomic_file)
    operons = search_operons(binding_sites, genes)
    if do_visualize:
        visualize_operons(operons)
    if do_print:
        rich.print(pformat(tuple(operons.items())))



# TODO:
# - --color-tfbs
# - --color-gene
# - --circular
# settings die in searcher.py staan

