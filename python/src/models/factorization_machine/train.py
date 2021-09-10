import pandas as pd
import logging
import pickle
from fastFM import als, sgd, mcmc
import numpy as np
from scipy.sparse import csr_matrix, csc_matrix
from sklearn import svm
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
import click

# from dotenv import find_dotenv, load_dotenv

LOGGER = logging.getLogger(__name__)

# load_dotenv(find_dotenv())

PLAYED_HEROES_PREDICTORS = [f"hero_{i}" for i in range(1, 225)]

DEFAULT_TRAIN_SET_PATH = "datasets/interim/only_draft_train_set.parquet"
DEFAULT_OUTPUT_MODEL_PATH = "models/fm_only_draft.pkl"

@click.command()
@click.option('--input_train_set_path', default=DEFAULT_TRAIN_SET_PATH, type=click.Path())
@click.option('--output_model_path', default=DEFAULT_OUTPUT_MODEL_PATH, type=click.Path())
def main(input_train_set_path, output_model_path):
    """Train models.
    ...
    """
    train_df = pd.read_parquet(input_train_set_path)
    test_df = pd.read_parquet("datasets/interim/only_draft_test_set.parquet")

    logger = logging.getLogger(__name__)
    logger.info("Some testing with SVM and FM")

    y_train = train_df["radiant_win"]
    # X_train = pipeline.fit_transform(train_df.drop(["radiant_win", "match_id"], axis=1))
    X_train = train_df.drop(["radiant_win", "match_id", "start_time"], axis=1)

    y_test = test_df["radiant_win"]
    # X_test = pipeline.fit_transform(test_df.drop(["radiant_win", "match_id"], axis=1))
    X_test = test_df.drop(["radiant_win", "match_id", "start_time"], axis=1)

    # slice
    MATCHES_COUNT = 20000
    X_train = X_train[0:MATCHES_COUNT]
    y_train = y_train[0:MATCHES_COUNT]

    # fm = sgd.FMClassification(n_iter=200, rank=60)
    # fm.fit(X_train, y_train)
    # score = fm.score(csc_matrix(X_test), y_test)

    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    param = {'max_depth': 2, 'eta': 1, 'objective': 'binary:logistic'}
    param['nthread'] = 4
    param['eval_metric'] = 'auc'

    num_round = 10
    bst = xgb.train(param, dtrain, num_round)
    pr1 = bst.predict(dtest)

    model = XGBClassifier(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)
    # make predictions for test data
    y_pred = model.predict(X_test)

    predictions = [round(value) for value in y_pred]
    # evaluate predictions
    accuracy = accuracy_score(y_test, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))

    kfold = StratifiedKFold(n_splits=10)
    results = cross_val_score(model, X_train, y_train, cv=kfold)
    print("Accuracy: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

    print("bst")
    print("bst")
    bst.predict(dtest)


    # pickle.dump(classifier, open(output_model_path, 'wb'))

if __name__ == '__main__':
    main()
