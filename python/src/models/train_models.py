from datetime import date, timedelta

import mlflow
import numpy as np
import pandas as pd
import logging
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

LOGGER = logging.getLogger(__name__)

def main():
    """Generate training sets and traing models.
    ...
    """
    scaler = StandardScaler()

    # mlflow.set_experiment("my-first-model-training")

    # with mlflow.start_run():

        # mlflow.log_params({"delta": delta, "batch_id": batch_id})

    train_data = pd.read_pickle("datasets/interim/train_set.pkl")
    # TODO: find a better way to remove those two cols
    X = train_data.loc[:, train_data.columns != "radiant_win"]
    X = X.loc[:, X.columns != "match_id"]
    y = train_data["radiant_win"]

    # create model instance and train
    clf = LogisticRegression(random_state=0).fit(X, y)

    # dump the model
    pickle.dump(clf, open("models/logistic_regression.pkl", 'wb'))

if __name__ == '__main__':
    main()
