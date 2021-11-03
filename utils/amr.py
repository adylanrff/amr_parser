from graphviz import Digraph
from stog.data.dataset_readers.amr_parsing.io import AMRIO

def dump_amr_features(amr, annotation, f):
    amr.tokens = annotation['tokens']
    amr.lemmas = annotation['lemmas']
    amr.pos_tags = annotation['pos_tags']
    amr.ner_tags = annotation['ner_tags']
    AMRIO.dump([amr], f)

def penman_to_dot(amr, path):
    dot = Digraph(format='png')
    
    instance_triples = filter(lambda x: x[1] == 'instance', amr._triples)
    edges = amr.edges()

    for triple in instance_triples:
        dot.node(triple[0], label=triple[2])
    for edge in edges:
        dot.edge(edge[0],edge[2], label=edge[1])

    dot.render(path)
    return dot.source