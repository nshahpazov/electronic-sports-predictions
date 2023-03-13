from datetime import date, timedelta

# import mlflow
import numpy as np
import pandas as pd
import logging
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

import click
from dotenv import find_dotenv, load_dotenv
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit

from sklearn.preprocessing import MinMaxScaler, StandardScaler, FunctionTransformer, OneHotEncoder
from sklearn.pipeline import Pipeline, FeatureUnion

LOGGER = logging.getLogger(__name__)

load_dotenv(find_dotenv())

PLAYED_HEROES_PREDICTORS = [f"hero_{i}" for i in range(1, 225)]

DEFAULT_TRAIN_SET_PATH = "datasets/interim/only_draft_train_set.parquet"
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

    y_train = train_df["radiant_win"]
    # X_train = pipeline.fit_transform(train_df.drop(["radiant_win", "match_id"], axis=1))
    X_train = train_df.drop(["radiant_win", "match_id", "start_time"], axis=1)

    # create model instance and train (Logistic Regression)
    logistic_regression = LogisticRegression(max_iter=10000)
    classifier = logistic_regression.fit(X_train, y_train)

    pickle.dump(classifier, open(output_model_path, 'wb'))

if __name__ == '__main__':
    main()
