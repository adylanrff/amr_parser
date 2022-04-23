import string
from collections import defaultdict

import nltk
import stanza
from tqdm import tqdm
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from utils.argument_parser import parse_arguments

# from utils.amr import penman_to_dot
from utils.ner.entity_recognizer import get_entities, get_entities_tf
from utils.amr_parsing.io import AMRIO
from utils.amr_parsing.amr import AMR
import argparse

class FeatureAnnotator:
    word_dict = {}
    
    def __init__(self, params):
        self.nlp = stanza.Pipeline(lang="id",use_gpu=True,verbose=False, tokenize_pretokenized=True)
        self.annotation={}
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()
        self.params = params
        if self.params["ner_tagger"]=='tf' :
            self.ner = get_entities_tf
        else:
            self.ner = get_entities
        
        if self.params['pos_tagger'] == 'nltk':
            self.pos_tagger = nltk.tag.CRFTagger()
            self.pos_tagger.set_model_file('pretrained/pos_tagger/all_indo_man_tag_corpus_model.crf.tagger')
        elif self.params['pos_tagger'] == 'stanza':
            pass
        
    def annotate(self, sentence):
        self.annotation = defaultdict(list)
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        self.annotation["sentence"] = sentence
        doc = self.nlp(sentence)
        
        self.annotation['ner_tags'] = self.ner(sentence)
        
        word_dict = defaultdict(int)
        
        for sent in doc.sentences:
            for idx, word in enumerate(sent.words):
                self.annotation['tokens'].append(word.text)
                stemmed_word = self.stemmer.stem(word.text)                
                if (self.annotation['ner_tags'][idx] in ['PER', 'ORG']):
                    stemmed_word = word.text.lower()
                word_dict[stemmed_word] += 1
                self.annotation['lemmas'].append(stemmed_word)
                self.annotation['pos_tags'].append(word.upos)
    
        if self.params['pos_tagger'] == 'nltk':
            self.annotation['pos_tags'] = [tag[1] for tag in self.pos_tagger.tag(self.annotation['tokens'])]
            
        
        return self.annotation

ner_labels_map = {
    "PER" : "PERSON",
    "LOC" : "LOCATION",
    "FAC" : "LOCATION",
    "GPE" : "LOCATION",
    "NOR" : "ORGANIZATION",
    "ORG" : "ORGANIZATION",
    "MON" : "MONEY",
    "CRD" : "NUMBER",
    "ORD" : "ORDINAL",
    "PRC" : "PERCENT",
    "DAT" : "DATE",
    "TIM" : "TIME",
}

def transform_ner_tags(annotation):
    ner_tags = annotation["ner_tags"]
    for i, ner in enumerate(ner_tags):
        annotation["ner_tags"][i] = ner_labels_map.get(ner.split("-")[-1],"O")

def dump_amr_features(amr_graph, annotation, f, index=None):
    amr = AMR()
    if amr_graph != "":
        amr.graph = amr_graph
    if index:
        amr.id = index
    amr.sentence = annotation["sentence"].strip()
    amr.tokens = annotation['tokens']
    amr.lemmas = annotation['lemmas']
    amr.pos_tags = annotation['pos_tags']
    amr.ner_tags = annotation['ner_tags']
    AMRIO.dump([amr], f)

def preprocess_amr(filepath, params):
    annotator = FeatureAnnotator(params)
    
    with open(filepath + '.features', 'w', encoding='utf-8') as f:
        i = 1
        for amr in AMRIO.read(filepath):
            if i % 100 == 0:
                print('{} processed.'.format(i))
            i+=1
            annotation = annotator.annotate(amr.sentence)
            transform_ner_tags(annotation)
            dump_amr_features(amr.graph, annotation, f, index=amr.id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AMR Parser for Bahasa Indonesia")
    parser.add_argument('file', help="AMR file input path for training or prediction")
    parser.add_argument('--pos_tagger', help="kind of pos tagger used either `nltk` or `stanza`", nargs='?', const="nltk", type=str)
    parser.add_argument('--ner_tagger', help="kind of ner tagger used either `tf` or `anago`",nargs='?', const="anago", type=str)
    args = parser.parse_args()
    filepath = args.file
    pos_tagger = args.pos_tagger #nltk/stanza
    ner_tagger = args.ner_tagger #anago/tf

    preprocess_amr(filepath, {'pos_tagger': pos_tagger, 'ner_tagger':ner_tagger})