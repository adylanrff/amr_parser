from constants.etc import RANDOM_STATE

def custom_dependency_parser_feature_k_fold(dataset, n_split, shuffle=False):
    min_sentence_id = dataset.min()['sentence_id']
    max_sentence_id = dataset.max()['sentence_id']
    sentence_num = max_sentence_id
    
    sentence_ids = np.arange(min_sentence_id, max_sentence_id+1)
    if (shuffle):
        np.random.seed(RANDOM_STATE)
        np.random.shuffle(sentence_ids)
    
    cur_sentence_id = min_sentence_id
    split_size = sentence_num // n_split
    
    indexes = []
    while (cur_sentence_id < max_sentence_id):
        stop_sentence_id = min(cur_sentence_id + split_size-1, sentence_num)
        test_sentence_ids = sentence_ids[cur_sentence_id:stop_sentence_id+1]
        
        test_condition = dataset.sentence_id.isin(test_sentence_ids)
        train_condition = ~test_condition 
        
        indexes.append((dataset[train_condition].index, dataset[test_condition].index))
        cur_sentence_id = stop_sentence_id
    
    return indexes