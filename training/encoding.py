from sklearn.preprocessing import LabelEncoder, OneHotEncoder

from constants.paths import ONE_HOT_ENCODER_PATH, LABEL_ENCODER_PATH
from preprocessing.model_feature import feature_selection

def one_hot_encode(dependency_features_df, feature_filter_type=None):
    one_hot_encoder = OneHotEncoder(handle_unknown='ignore')

    filtered_df = feature_selection(dependency_features_df, feature_filter_type)
    one_hot_feature_names = ['parent_ner', 'child_ner', 'parent_pos', 'dependency_role','child_pos']
    one_hot_features = list(filtered_df.columns[filtered_df.columns.isin(one_hot_feature_names)])
    one_hot_encoder.fit(dependency_features_df[one_hot_features])

    # Save one hot encoder
    with open(ONE_HOT_ENCODER_PATH, 'wb') as f:
        pickle.dump(one_hot_encoder,f)

    return one_hot_encoder


def label_encode(dependency_features_df):
    label_encoder = LabelEncoder()
    label_encoder.fit(dependency_features_df['label'])
    labels = label_encoder.classes_

    with open(LABEL_ENCODER_PATH, 'wb') as f:
        pickle.dump(label_encoder,f)

    return label_encoder