
from operon_searcher.gene import Gene
from operon_searcher.lib import Strand
from operon_searcher.tf import TFBS


GENE_OPERON_MAX_GAP = 200
FIMO_BATCH_SIZE = 30
GENE_TO_BINDING_SITE_MAX_GAP = 300
MAX_FAILED_HITS = 5

def search_operons(binding_sites: list[TFBS], genes: list[Gene]):
    binding_sites = sorted(binding_sites, key=lambda tfbs: tfbs.pvalue)[:FIMO_BATCH_SIZE]
    failed_hits = 0
    tf_genes: dict[TFBS, list[Gene]] = {}
    for n, tf in enumerate(binding_sites):
        tf.n = n # TODO: properly implement this
        if failed_hits > MAX_FAILED_HITS and n >= 20:
            break
        gene_tail = -1
        for gene in genes:
            if tf.strand != gene.strand:
                continue
            condition = False
            # Check if possible TF overlaps with a gene, if yes, this is a failed hit
            if any(gene.start <= pos <= gene.end for pos in (tf.start, tf.end)):
                if tf in tf_genes:
                    tf_genes.pop(tf)
                failed_hits += 1
                break

            if tf.strand == Strand.Positive:
                if gene_tail == -1:
                    condition = (0 <= gene.start - tf.end <= GENE_TO_BINDING_SITE_MAX_GAP)
                else:
                    condition = ((tf.end < gene.start) and (gene.start - gene_tail <= GENE_OPERON_MAX_GAP))
                if condition:
                    gene_tail = gene.end
            elif tf.strand == Strand.Negative:
                if gene_tail == -1:
                    condition = (0 <= tf.start - gene.end <= GENE_TO_BINDING_SITE_MAX_GAP)
                else:
                    condition = (tf.start > gene.end and (gene_tail - gene.end <= GENE_OPERON_MAX_GAP))
                if condition:
                    gene_tail = gene.start
            else:
                raise Exception("HUH???")
            if condition:
                if tf not in tf_genes:
                    tf_genes[tf] = []
                tf_genes[tf].append(gene)
                failed_hits = 0
            else:
                failed_hits += 1
    return tf_genes