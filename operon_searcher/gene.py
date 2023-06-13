import dataclasses
from operon_searcher.lib import SubSequence, automatic_field_converter, from_dict, parse_rest

from pathlib import Path


@dataclasses.dataclass
class Gene(SubSequence):
    id: str
    name: str
    __post_init__ = automatic_field_converter
    from_dict = from_dict
    def __hash__(self) -> int:
        return hash(str(super().__hash__()) + self.id)

def genomic_parser(path: Path) -> list[Gene]:
    with open(path / 'genomic.gff', 'r') as file:
        l = []
        for line in file.readlines():
            line.strip("\n")
            if line.startswith('#'):
                continue
            organism_id, source, soort_seq, start, end, stip, strand, idk, rest = line.split("\t")
            # rest = eval(f"dict({rest.replace(';', ',')})")
            # id, dbxref, iscircular, 
            # if int(start)-int(end) > 0:
            #     print("interesting")
            if soort_seq != 'gene':
                continue
            data = {
                'organism_id': organism_id,
                'start': start,
                'end': end,
                'strand': strand
            }
            data |= parse_rest(rest)
            l.append(Gene.from_dict(data))
        return l