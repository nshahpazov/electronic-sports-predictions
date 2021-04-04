from datetime import date, timedelta

import mlflow
import numpy as np
import pandas as pd
import logging
import pickle
from sklearn.linear_model import LogisticRegression

LOGGER = logging.getLogger(__name__)

def main():
    """Predict on test data
    ...
    """
    test_data = pd.read_pickle("datasets/interim/test_set.pkl")
    X_test = test_data.loc[:, test_data.columns != "radiant_win"]
    Y_test = test_data["radiant_win"]

    # create model instance and train
    clf = pickle.load(open("models/logistic_regression.pkl", 'rb'))

    result = clf.score(X_test, Y_test)
    print(result)

if __name__ == '__main__':
    main()
