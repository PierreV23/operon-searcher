from pathlib import Path
from operon_searcher.gene import Gene
from operon_searcher.lib import timer
from operon_searcher.tf import TFBS
from dna_features_viewer import GraphicFeature, GraphicRecord # deze import duurt kapot lang

TFBS_COLOUR = "#ffd700"
GENE_COLOUR = "#cffccc"

# @timer
def create_graphic_features(tf: TFBS, genes: list[Gene]) -> list[GraphicFeature]:
    features=[]
    features.append(
        GraphicFeature(start=tf.start, end=tf.end, strand=eval(tf.strand.value + str(tf.start % 3 or 3)), color=TFBS_COLOUR, label="TFBS")
    )
    for gene in genes:
        features.append(
        GraphicFeature(start=gene.start, end=gene.end, strand=eval(tf.strand.value + str(tf.start % 3 or 3)), color=GENE_COLOUR, label=gene.name)
    )
    return features


def visualize_operons(tf_genes: dict[TFBS, list[Gene]]):
    (Path() / 'output').mkdir(exist_ok=True)
    for tf, genes in tf_genes.items():
        features = create_graphic_features(tf, genes)
        features.sort(key=lambda gf: gf.start) # type: ignore
        first_index = min(features, key=lambda gf: gf.start).start - 100 # type: ignore
        record = GraphicRecord(sequence_length=max(features, key=lambda gf: gf.end).end-first_index+100, features=features, first_index=first_index) # type: ignore
        ax, _ = record.plot(figure_width=5)
        labels = [int(f) for f in ax.get_xticks()]
        ax.set_xticklabels(labels=labels, rotation=45, ha='right')
        ax.figure.tight_layout()
        # ax.figure.set_size_inches(1920/100, 1080/100)
        ax.figure.set_size_inches(1200/100, 800/100)
        ax.figure.savefig(str(Path() / 'output' / f'{tf.n:02} - {tf.score}.png'), dpi = 300)
