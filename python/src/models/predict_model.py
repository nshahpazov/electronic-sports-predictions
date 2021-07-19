from datetime import date, timedelta
# import mlflow
# import numpy as np
import pandas as pd
import logging
import pickle
import pickle
import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from dotenv import find_dotenv, load_dotenv
from sklearn.metrics import roc_auc_score
import click
from sklearn.compose import ColumnTransformer

from sklearn.preprocessing import MinMaxScaler, StandardScaler, FunctionTransformer, OneHotEncoder
from sklearn.pipeline import Pipeline, FeatureUnion

LOGGER = logging.getLogger(__name__)

load_dotenv(find_dotenv())

DEFAULT_INPUT_PATH = "datasets/interim/train_set.pkl"
DEFAULT_OUTPUT_PATH = "datasets/processed/train_set.parquet"

NUMERIC_PREDICTORS = [
    "base_armor_diff", "base_attack_min_diff", "base_attack_max_diff", "base_str_diff",
    "base_agi_diff", "base_int_diff", "str_gain_diff", "agi_gain_diff", "int_gain_diff",
    "attack_range_diff", "projectile_speed_diff", "attack_rate_diff", "move_speed_diff",
    "turn_rate_diff"
]

CATEGORIC_PREDICTORS = [
    "has_carry_1", "has_escape_1", "has_nuker_1", "has_initiator_1", "has_durable_1",
    "has_disabler_1", "has_support_1", "has_pusher_1", "has_jungler_1", "has_carry_2",
    "has_escape_2", "has_nuker_2", "has_initiator_2", "has_durable_2", "has_disabler_2",
    "has_jungler_2", "has_support_2", "has_pusher_2", "has_primary_agi_1", "has_primary_int_1",
    "has_primary_str_1", "has_primary_agi_2", "has_primary_int_2", "has_primary_str_2",
    "has_melee_1", "has_ranged_1", "has_melee_2", "has_ranged_2"
]

PLAYED_HEROES_PREDICTORS = [f"hero_{i}" for i in range(1, 225)]

LOGGER = logging.getLogger(__name__)

DEFAULT_TEST_SET_PATH = "datasets/interim/only_draft_test_set.parquet"
DEFAULT_MODEL_PATH = "models/lr_only_draft.pkl"

@click.command()
@click.option('--test_set_path', default=DEFAULT_TEST_SET_PATH, type=click.Path())
@click.option('--model_path', default=DEFAULT_MODEL_PATH, type=click.Path())
def main(model_path, test_set_path):
    """Predict on test data
    """
    test_df = pd.read_parquet(test_set_path)

    pipeline = FeatureUnion([
        ('numerical', Pipeline([
            ('select_num', FunctionTransformer(func=lambda X: X.loc[:, NUMERIC_PREDICTORS])),
            ('scaler', StandardScaler())
        ])),
        ('categorical', Pipeline([
            ('select_cat', FunctionTransformer(func=lambda X: X.loc[:, CATEGORIC_PREDICTORS])),
            ('onehot', OneHotEncoder(sparse=False, handle_unknown='ignore'))
        ])),
        ('rest', Pipeline([
            ('identity', FunctionTransformer(func=lambda X: X.loc[:, PLAYED_HEROES_PREDICTORS]))
        ]))
    ])

    # for now train only on the draft features

    train_df = pd.read_parquet("datasets/interim/train_set_all.parquet")
    pipeline.fit(train_df.drop(["radiant_win", "match_id"], axis=1))

    # X_test = pipeline.transform(test_df.drop(["radiant_win", "match_id"], axis=1))
    X_test = test_df.drop(["radiant_win", "match_id"], axis=1)

    y_test = test_df["radiant_win"]

    # create model instance and train
    clf1 = pickle.load(open(model_path, 'rb'))

    result1 = clf1.score(X_test, y_test)
    print(result1)

    # testing xgboost model
    # bst = pickle.load(open("./models/xgboost_only_draft.pkl", 'rb'))
    # dtest = xgb.DMatrix(X_test)

    # preds = bst.predict(dtest)
    # print((preds > 0.5) == y_test)
    # ('ROC AUC Score', roc_auc_score(y_test, preds))

if __name__ == '__main__':
    main()
