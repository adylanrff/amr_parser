import gensim
from constants.paths import WORD2VEC_PATH

def load_word_vec():
    word_vec_model = gensim.models.Word2Vec.load(WORD2VEC_PATH)
    word_vec = word_vec_model.wv
    return word_vec