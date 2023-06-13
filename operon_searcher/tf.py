import dataclasses
from pathlib import Path
from .lib import SubSequence, automatic_field_converter, from_dict, parse_rest

@dataclasses.dataclass
class TFBS(SubSequence):
    score: float
    name: str
    pvalue: float
    qvalue: float
    sequence: str
    __post_init__ = automatic_field_converter

    from_dict = from_dict
    
    def __hash__(self) -> int: # Just to be sure ;)
        return hash(str(super().__hash__()) + self.sequence)


def fimo_parser(path: Path) -> list[TFBS]:
    with open(path / 'fimo.gff', 'r') as file:
        l = []
        for line in file.readlines():
            line.strip("\n")
            if line.startswith('#'):
                continue
            organism_id, _, _, start, end, score, strand, _, rest = line.split("\t")
            # if int(start)-int(end) > 0:
            #     print("interesting")
            data: dict[str, str] = {
                'start': start,
                'end': end,
                'score': score,
                'strand': strand,
                'organism_id': organism_id
            }
            data |= parse_rest(rest)
            # l.append({'start': start, 'end': end, 'score': score, 'pvalue': data['pvalue'], 'qvalue': data['qvalue']})
            l.append(TFBS.from_dict(data))
        return l