import click
import logging
from pathlib import Path
import sqlite3
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from sklearn.model_selection import train_test_split
import os
# from jinja2 import Template

load_dotenv(find_dotenv())

# move those to the env file
DEFAULT_TRAIN_SET_SIZE = 0.8
DEFAULT_RANDOM_STATE = 42
DEFAULT_TRAIN_SET_PATH = "datasets/interim/train_set.parquet"
DEFAULT_TEST_SET_PATH = "datasets/interim/test_set.parquet"

@click.command()
@click.option('--train_set_filepath', default=DEFAULT_TRAIN_SET_PATH, type=click.Path())
@click.option('--test_set_filepath', default=DEFAULT_TEST_SET_PATH, type=click.Path())
@click.option('--random_state', default=DEFAULT_RANDOM_STATE, type=click.INT)
@click.option('--train_set_size', default=DEFAULT_TRAIN_SET_SIZE, type=click.FLOAT)
def main(train_set_filepath, test_set_filepath, random_state, train_set_size):
    """ Runs data train, test split scripts to turn data into
        splitted train and test set data.
    """
    logger = logging.getLogger(__name__)
    logger.info("creating train and test set data from raw data")

    con = sqlite3.connect(os.environ.get("SQLITE_DATABASE_URL"))
    all_predictors_sql = open("src/data/pipeline/queries/predictors.sql").read()

    df = pd.read_sql_query(all_predictors_sql, con)
    train_df, test_df = train_test_split(df, train_size=train_set_size, random_state=random_state)

    train_df.to_parquet(train_set_filepath)
    test_df.to_parquet(test_set_filepath)

# execute the script
if __name__ == '__main__':
    main()
