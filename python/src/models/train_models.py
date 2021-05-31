from datetime import date, timedelta

import mlflow
import numpy as np
import pandas as pd
import logging
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from dotenv import find_dotenv, load_dotenv
import os
import xgboost as xgb
import click
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import MinMaxScaler, StandardScaler, FunctionTransformer, OneHotEncoder
from sklearn.pipeline import Pipeline, FeatureUnion

LOGGER = logging.getLogger(__name__)

load_dotenv(find_dotenv())

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

DEFAULT_TRAIN_SET_PATH = "datasets/interim/train_set.parquet"
DEFAULT_OUTPUT_MODEL_PATH = "models/lr_only_draft.pkl"


@click.command()
@click.option('--input_train_set_path', default=DEFAULT_TRAIN_SET_PATH, type=click.Path())
@click.option('--output_model_path', default=DEFAULT_OUTPUT_MODEL_PATH, type=click.Path())
def main(input_train_set_path, output_model_path):
    """Train models.
    ...
    """
    train_df = pd.read_parquet(input_train_set_path)

    logger = logging.getLogger(__name__)
    logger.info("Processing data by standardizing and imputing it")

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

    # mlflow.set_experiment("my-first-model-training")

    # with mlflow.start_run():

        # mlflow.log_params({"delta": delta, "batch_id": batch_id})

    y_train = train_df["radiant_win"]
    X_train = pipeline.fit_transform(train_df.drop(["radiant_win", "match_id"], axis=1))
    # X_train = train_df.drop(["radiant_win", "match_id"], axis=1)

    # create model instance and train (Logistic Regression)
    clf = LogisticRegression(max_iter=10000).fit(X_train, y_train)
    pickle.dump(clf, open(output_model_path, 'wb'))

    # XGBoost training
    train_set, validation_set = train_test_split(train_df)

    # TODO: try with different levels
    dtrain = xgb.DMatrix(X_train, label=y_train)
    # dtest = xgb.DMatrix(X_high[test_ind, :], label = y_high[test_ind])

    param = {'bst:max_depth': 6, 'bst:eta': 0.4, 'silent': 1, 'objective': 'binary:logistic'}
    param = {'max_depth': 2, 'eta': 1, 'objective': 'binary:logistic'}
    param['eval_metric'] = 'accuracy'
    param['nthread'] = 4
    param['eval_metric'] = ['accuracy']
    num_round = 200
    bst = xgb.train( param, dtrain, num_round, evallist, verbose_eval = 10)


if __name__ == '__main__':
    main()
