import pandas as pd
import logging
import pickle
import pickle
from dotenv import find_dotenv, load_dotenv
import click

LOGGER = logging.getLogger(__name__)

load_dotenv(find_dotenv())

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
    X_test = test_df.drop(["radiant_win", "match_id", "start_time"], axis=1)

    y_test = test_df["radiant_win"]

    clf1 = pickle.load(open(model_path, 'rb'))

    result1 = clf1.score(X_test, y_test)
    print(result1)

if __name__ == '__main__':
    main()
