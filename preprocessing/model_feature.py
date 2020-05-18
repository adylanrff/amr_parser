import numpy as np

def filter_pair(data, mode='all'):
    if ('preposition' in mode):
        data = data[data['child_pos'] != 'IN']
    
    if ('determiner' in mode):
        data = data[data['dependency_role'] != 'det']
        
    if ('case' in mode):
        data = data[data['dependency_role'] != 'case']
    
    if ('sc' in mode):
        data = data[data['child_pos'] != 'SC']

    return data

def feature_selection(dataset, filter_type='all'):
    lexical_features = ['parent', 'child']
    positional_features = ['parent_position', 'child_position']
    structural_features = ['parent_pos', 'child_pos']
    syntactic_features = ['dependency_role']
    ner_features = ['parent_ner', 'child_ner']
    
    selected_dataset = dataset
    
    if filter_type != 'all':
        if 'lexical' in filter_type:
            selected_dataset = selected_dataset.drop(lexical_features, axis=1)
        if 'positional' in filter_type:
            selected_dataset = selected_dataset.drop(positional_features, axis=1)
        if 'syntactic' in filter_type:
            selected_dataset = selected_dataset.drop(syntactic_features+structural_features, axis=1)
        if 'ner' in filter_type:
            selected_dataset = selected_dataset.drop(ner_features, axis=1)
        
    return selected_dataset

def preprocess(X_train, word_vec, one_hot_encoder):
    word_feature_names = ['parent', 'child']
    one_hot_feature_names = ['parent_ner', 'child_ner', 'parent_pos', 'dependency_role', 'child_pos']
    
    word_features = list(X_train.columns[X_train.columns.isin(word_feature_names)])
    one_hot_features = list(X_train.columns[X_train.columns.isin(one_hot_feature_names)])
    
    def check_word_features(X):
        columns = [column in word_features for column in X.columns]
        return any(columns)

    contains_word_features = check_word_features(X_train)
    
    X_train_dropped = X_train
    if (contains_word_features):
        X_train_dropped = X_train.drop(word_features+one_hot_features, axis=1)
    else:
        X_train_dropped = X_train.drop(one_hot_features, axis=1)
    
    if contains_word_features:
        X_train_word_data = X_train[word_features]
        # load word embedding
        embeddings = []
        for data in X_train_word_data.values:
            current_embedding = []
            for word in data:
                splitted_word = word.split('_')[0]
                if splitted_word in word_vec:
                    current_embedding.append(word_vec[splitted_word])
                else:
                    none = [0] * 300
                    current_embedding.append(none)
            embeddings.append(current_embedding)
    
    # load one hot encoder
    X_train_one_hot_data = X_train[one_hot_features]
    X_train_one_hot_encoded = one_hot_encoder.transform(X_train_one_hot_data).toarray()
    
    X_train = []
    for idx, row in enumerate(X_train_dropped.values):
        concatenated = None
        if (contains_word_features):
            concatenated = np.concatenate([row, X_train_one_hot_encoded[idx], embeddings[idx][0],embeddings[idx][1]])
        else:
            concatenated = np.concatenate([row, X_train_one_hot_encoded[idx]])
            
        X_train.append(concatenated)
    
    return np.array(X_train)