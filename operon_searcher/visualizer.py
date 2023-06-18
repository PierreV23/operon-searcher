from pathlib import Path

import matplotlib
from operon_searcher.gene import Gene
from operon_searcher.tf import TFBS
from dna_features_viewer import GraphicFeature, GraphicRecord # deze import duurt kapot lang

TFBS_COLOUR = "#ffd700"
GENE_COLOUR = "#cffccc"
USE_OLD_LOCUS_TAG = False

def create_graphic_features(tf: TFBS, genes: list[Gene]) -> list[GraphicFeature]:
    features=[]
    features.append(
        GraphicFeature(start=tf.start, end=tf.end, strand=eval(tf.strand.value + str(tf.start % 3 or 3)), color=TFBS_COLOUR, label="TFBS")
    )
    for gene in genes:
        if gene.name == gene.locus_tag:
            if USE_OLD_LOCUS_TAG:
                label = gene.old_locus_tag if gene.old_locus_tag not in (None, "None") else gene.locus_tag
            else:
                label = gene.locus_tag or gene.old_locus_tag
        else:
            label = gene.name
        features.append(
        GraphicFeature(start=gene.start, end=gene.end, strand=eval(tf.strand.value + str(tf.start % 3 or 3)), color=GENE_COLOUR, label=label)
    )
    return features


def visualize_operons(tf_genes: dict[TFBS, list[Gene]], output_folder: Path):
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
        ax.figure.savefig(output_folder / f'{tf.n:02} - {tf.score} {tf.start}-{tf.end}.png', dpi = 300)
        matplotlib.pyplot.close(ax.figure)
