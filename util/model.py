import gensim
from constants.paths import SAVED_MODEL_DIR, WORD2VEC_PATH, ONE_HOT_ENCODER_PATH, LABEL_ENCODER_PATH
import pickle

def load_model(model_name):
    with open(SAVED_MODEL_DIR+model_name, 'rb') as f:
        model = pickle.load(f)

    return model

def save_model(model, model_name):
    with open(best_model_filename, 'wb') as f:
        pickle.dump(best_model.model, f)

def load_word_vec():
    word_vec_model = gensim.models.Word2Vec.load(WORD2VEC_PATH)
    word_vec = word_vec_model.wv
    return word_vec

def load_one_hot_encoder():
    with open(ONE_HOT_ENCODER_PATH, 'rb') as f:
        one_hot_encoder = pickle.load(f)
    return one_hot_encoder

def load_label_encoder():
    with open(LABEL_ENCODER_PATH, 'rb') as f:
        label_encoder = pickle.load(f)    
    return label_encoder
