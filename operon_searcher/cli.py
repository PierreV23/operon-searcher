from dataclasses import asdict
import json
from pathlib import Path
from pprint import pformat
import threading
from typing import Annotated, Optional
import typer
from operon_searcher import searcher
from operon_searcher.gene import genomic_parser
from operon_searcher.searcher import search_operons

from operon_searcher.tf import fimo_parser

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
        None,
        "--tfbs-color",
        help="Color of binding site when visualizing."
    ),
    gene_color: str = typer.Option(
        None,
        "--gene-color",
        help="Color of gene when visualizing."
    ),
    export: Path = typer.Option(
        None,
        "-e",
        "--export",
        help="Exporteer operons naar een json bestand.",
        file_okay=True
    ),
    do_ignore_hypothetical_proteins: bool = typer.Option(
        False,
        "--ignore-hypothetical-proteins",
        help="Het bestaan van een gen negeren tijdens het zoeken naar operons, als het gen een hypothetical protein is.",
        file_okay=True
    ),
):    
    searcher.GENE_OPERON_MAX_GAP          = gene_gap
    searcher.FIMO_BATCH_SIZE              = batch_size
    searcher.GENE_TO_BINDING_SITE_MAX_GAP = site_gap
    searcher.MAX_FAILED_HITS              = max_fails
    searcher.IGNORE_HYPOTHETICAL_PROTEINS = do_ignore_hypothetical_proteins

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
        from operon_searcher import visualizer
        if tfbs_color is not None or gene_color is not None:
            visualizer.TFBS_COLOUR = tfbs_color
            visualizer.GENE_COLOUR = gene_color
        visualizer.visualize_operons(operons)
    if do_print:
        rich.print(pformat(tuple(operons.items()), sort_dicts=False))
    if export is not None:
        with open(export, 'w') as file:
            json.dump(
                [
                    {
                        'tfbs': asdict(tfbs),
                        'genes': [asdict(gene) for gene in genes]
                    }
                    for tfbs, genes in operons.items()
                ],
                file,
                indent=4,
                sort_keys=False
            )



# TODO:
# - --color-tfbs
# - --color-gene
# - --circular
# settings die in searcher.py staan

