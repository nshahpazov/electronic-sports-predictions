import click
import logging
import sqlite3
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from sklearn.model_selection import train_test_split
import os
from jinja2 import Template

load_dotenv(find_dotenv())

# move those to the env file
DEFAULT_TRAIN_SET_SIZE = 0.9

DEFAULT_TRAIN_SET_PATH = "datasets/interim/only_draft_train_set.parquet"
DEFAULT_TEST_SET_PATH = "datasets/interim/only_draft_test_set.parquet"

@click.command()
@click.option('--train_set_filepath', default=DEFAULT_TRAIN_SET_PATH, type=click.Path())
@click.option('--test_set_filepath', default=DEFAULT_TEST_SET_PATH, type=click.Path())
@click.option('--train_set_size', default=DEFAULT_TRAIN_SET_SIZE, type=click.FLOAT)
@click.option('--has_played_heroes', default=True)
@click.option('--has_hero_characteristics', default=False)
@click.option('--has_roles', default=False)
@click.option('--has_mmr_ratings', default=False)
@click.option('--limit')
def main(
    train_set_filepath,
    test_set_filepath,
    train_set_size,
    has_played_heroes,
    has_hero_characteristics,
    has_roles,
    has_mmr_ratings,
    limit
):
    """ Runs data train, test split scripts to turn data into
        splitted train and test set data.
    """
    logger = logging.getLogger(__name__)
    logger.info("creating train and test set data from raw data")

    con = sqlite3.connect(os.environ.get("SQLITE_DATABASE_URL"))
    all_predictors_template = open("src/data/pipeline/queries/predictors.sql").read()

    all_predictors_sql = Template(all_predictors_template).render(
    # rendered_sql = Template(played_heroes_sql).render(
        has_played_heroes=has_played_heroes,
        has_hero_characteristics=has_hero_characteristics,
        has_roles=has_roles,
        limit=limit,
        has_mmr_ratings=has_mmr_ratings
    )

    df = pd.read_sql_query(all_predictors_sql, con)

    train_df, test_df = train_test_split(
        df,
        train_size=train_set_size,
        shuffle=True,
        stratify=df['radiant_win']
    )

    train_df.to_parquet(train_set_filepath)
    test_df.to_parquet(test_set_filepath)

# execute the script
if __name__ == '__main__':
    main()
