from pathlib import Path
from pprint import pprint, pformat
from operon_searcher.gene import genomic_parser
from operon_searcher.searcher import search_operons
from operon_searcher.tf import fimo_parser
from operon_searcher.visualize import visualize_operons

REFSEQ = Path() / 'RefSeq_GCA_000017005.1'
GENBANK = Path() / 'Genbank_GCF_000017005.1'

# folder = REFSEQ
folder = GENBANK

binding_sites = fimo_parser(folder)
genes = genomic_parser(folder)
operons = search_operons(binding_sites, genes)

pprint(operons.items(), indent=4)

visualize_operons(operons)


# umm note: de import in operon_searcher.visualize duurt kapot lang

