from stog.data.dataset_readers.amr_parsing.io import AMRIO

def dump_amr_features(amr, annotation, f):
    amr.tokens = annotation['tokens']
    amr.lemmas = annotation['lemmas']
    amr.pos_tags = annotation['pos_tags']
    amr.ner_tags = annotation['ner_tags']
    AMRIO.dump([amr], f)

def penman_to_dot(amr):
    instance_triples = filter(lambda x: x[1] == 'instance', amr._triples)
    edges = amr.edges()


    instances = {}
    for triple in instance_triples:
        instances[triple[0]] = triple[2]


    dot_content = ''
    for edge in edges:
        dot_content += '{} -> {} [label="{}"];'.format(instances[edge[0]], instances[edge[2]], edge[1])
    dot = 'digraph {' + dot_content + "}"

    return dot