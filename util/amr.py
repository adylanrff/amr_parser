from stog.data.dataset_readers.amr_parsing.io import AMRIO

def dump_amr_features(amr, annotation, f):
    amr.tokens = annotation['tokens']
    amr.lemmas = annotation['lemmas']
    amr.pos_tags = annotation['pos_tags']
    amr.ner_tags = annotation['ner_tags']
    AMRIO.dump([amr], f)