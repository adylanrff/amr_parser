from constants.etc import RANDOM_STATE
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from preprocessing.model_feature import preprocess_feature_and_label, feature_selection

class TrainingModel:
    def __init__(self, name, model, performance, labels):
        self.name = name
        self.model = model
        self.performance = performance
        self.labels = labels
    
    def __gt__(self, model2):
        return self.performance['f1_macro'] > model2.performance['f1_macro']
    
    def print_metrics(self):
        performance = self.performance
        accuracy = performance['accuracy']
        f1_macro = performance['f1_macro']
        f1_micro = performance['f1_micro']
        smatch = performance.get('smatch', 0)
                
        print("----{}----".format(self.name))
        print()
        print("Accuracy: {:.3f}\nF1 Micro : {:.3f}\nF1 Macro: {:.3f}\nSMATCH: {:.3f}".format(accuracy,f1_micro, f1_macro, smatch))
        
    def save(self):
        best_model_filename = "saved_model/{}_best.pickle.dat".format(self.name)
        with open(best_model_filename, 'wb') as f:
            pickle.dump(best_model.model,f)
            
class ExperimentParams:
    def __init__(self, model_name, model_params):
        self.model_name = model_name
        self.model_params = model_params

def fit_predict_model(model_name, X_train, y_train, X_val, y_val, params):
    supported_model_name = ['dtc', 'xgb']
    if model_name not in supported_model_name:
        raise Exception("Model not supported")

    if model_name == 'dtc':
        model = DecisionTreeClassifier(random_state=RANDOM_STATE, **params)
    elif model_name == 'xgb':
        if not params:
            params = {}
        model = XGBClassifier(**params)
    # Do training
    model = model.fit(np.array(X_train), np.array(y_train))
    # Do predict with val data
    y_val_pred = model.predict(np.array(X_val))
    
    return model, y_val_pred


def run_k_fold_validation(dataset, n_split, word_vec, label_encoder, one_hot_encoder, shuffle=False, feature_filter='all', model_name='dtc', params=None):
    folds = custom_dependency_parser_feature_k_fold(dataset, n_split, shuffle=shuffle)
    label = ['label']
    
    performances = defaultdict(list)
    
    for train_idx, val_idx in folds:
        train_dataset, val_dataset = dataset.iloc[train_idx], dataset.iloc[val_idx]
        X_train, y_train = train_dataset.drop(label, axis=1), train_dataset[label]
        X_val, y_val = val_dataset.drop(label, axis=1), val_dataset[label]
        
        filtered_X_train = feature_selection(X_train, feature_filter)
        filtered_X_val = feature_selection(X_val, feature_filter)
        
        # save AMR Data
        amr_val_df = amr_dataset[amr_dataset.sentence_id.isin(X_val.sentence_id.unique())]
        save_amr_data(amr_val_df, amr_val_prediction_path)
        
        # preprocess features
        X_train_processed, y_train_processed = preprocess_feature_and_label(filtered_X_train, y_train, one_hot_encoder, label_encoder)
        X_val_processed, y_val_processed = preprocess_feature_and_label(filtered_X_val, y_val, one_hot_encoder, label_encoder)
        
        model, y_val_pred = fit_predict_model(model_name, X_train_processed, y_train_processed, X_val_processed, y_val_processed, params)
        performance = get_metrics(y_val_processed, y_val_pred, label_encoder)

        # build prediction
        amr_graphs = build_amr_from_prediction(X_val, y_val_pred)
        save_amr_graphs(amr_graphs, amr_val_prediction_path)
        
        for key in performance:
            performances[key].append(performance[key])
    
    for key in performances:
        performances[key] = np.mean(performances[key])
    
    return model, performances