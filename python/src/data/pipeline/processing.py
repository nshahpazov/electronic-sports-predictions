import click
import logging
from pathlib import Path
import pandas as pd
import numpy as np
from dotenv import find_dotenv, load_dotenv
import os

from sklearn.preprocessing import MinMaxScaler, StandardScaler, FunctionTransformer, OneHotEncoder
from sklearn.pipeline import Pipeline, FeatureUnion


load_dotenv(find_dotenv())

DEFAULT_INPUT_PATH = "datasets/interim/train_set.pkl"
DEFAULT_OUTPUT_PATH = "datasets/processed/train_set.parquet"

# TODO: Check why there are duplicate columns

NUMERIC_PREDICTORS = [
    "base_armor_diff",
    "base_attack_min_diff",
    "base_attack_max_diff",
    "base_str_diff",
    "base_agi_diff",
    "base_int_diff",
    "str_gain_diff",
    "agi_gain_diff",
    "int_gain_diff",
    "attack_range_diff",
    "projectile_speed_diff",
    "attack_rate_diff",
    "move_speed_diff",
    "turn_rate_diff"
]

CATEGORIC_PREDICTORS = [
    "has_carry_1",
    "has_escape_1",
    "has_nuker_1",
    "has_initiator_1",
    "has_durable_1",
    "has_disabler_1",
    "has_support_1",
    "has_pusher_1",
    "has_jungler_1",
    "has_carry_2",
    "has_escape_2",
    "has_nuker_2",
    "has_initiator_2",
    "has_durable_2",
    "has_disabler_2",
    "has_jungler_2",
    "has_support_2",
    "has_pusher_2",
    "has_primary_agi_1",
    "has_primary_int_1",
    "has_primary_str_1",
    "has_primary_agi_2",
    "has_primary_int_2",
    "has_primary_str_2",
    "has_melee_1",
    "has_ranged_1",
    "has_melee_2",
    "has_ranged_2"
]

@click.command()
@click.option('--input_path', default=DEFAULT_INPUT_PATH, type=click.Path())
@click.option('--output_filepath', default=DEFAULT_OUTPUT_PATH, type=click.Path())
def main(input_path, output_filepath):
    """
    Process the input data by standardizing the predictors and imputing returing a
    ready to model with data.
    """

    input_df = pd.read_pickle(input_path)

    not_transformed_cols = np.setdiff1d(input_df.columns, NUMERIC_PREDICTORS + CATEGORIC_PREDICTORS)

    # this excludes the columns not in the list
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
            ('identity', FunctionTransformer(func=lambda X: X.loc[:, not_transformed_cols]))
        ]))
    ])

    X = pipeline.fit_transform(input_df)

    transformed_df = pd.DataFrame(X, columns = input_df.columns)
    # transformed_df = transformed_df.loc[:, transformed_df.columns != "match_id"]

    logger = logging.getLogger(__name__)
    logger.info("Processing data by standardizing and imputing it")

    input_data = pd.read_pickle(input_path)
    print(input_data)


# execute the script
if __name__ == '__main__':
    main()
