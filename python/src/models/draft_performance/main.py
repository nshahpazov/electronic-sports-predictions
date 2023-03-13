# %% import libraries
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix, csc_matrix

# models used
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
# from fastFM import als, sgd, mcmc

from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_validate
from sklearn.neural_network import MLPClassifier

# %% some constants
PLAYED_HEROES_PREDICTORS = [f"hero_{i}" for i in range(1, 225)]

# %% train and test dataframes
train_df = pd.read_parquet("../../../datasets/interim/only_draft_train_set.parquet")
test_df = pd.read_parquet("../../../datasets/interim/only_draft_test_set.parquet")

# extract design matrix and outcome variable
y_train = train_df["radiant_win"]
# X_train = pipeline.fit_transform(train_df.drop(["radiant_win", "match_id"], axis=1))
X_train = train_df.drop(["radiant_win", "match_id", "start_time"], axis=1)

y_test = test_df["radiant_win"]
X_test = test_df.drop(["radiant_win", "match_id", "start_time"], axis=1)

# %% slice the dataframe for the sake of quick exploration
MATCHES_COUNT = 10000
X_train = X_train[0:MATCHES_COUNT]
y_train = y_train[0:MATCHES_COUNT]

# %% load logistic regression and xgboost and do a cross validation with them
lr = LogisticRegression(max_iter=1000, penalty='none')

# cross validation with all the models

scores_hash = cross_validate(lr, X_train, y_train, scoring=['accuracy', 'roc_auc', 'neg_log_loss'], cv=10)
scores_df = pd.DataFrame(scores_hash)
scores_df

# kfold = StratifiedKFold(n_splits=10)
# results = cross_val_score(lr, X_train, y_train, cv=kfold, scoring=['accuracy', 'precision'])
# print("Accuracy: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))


# %%
dtrain = xgb.DMatrix(X_train, label = y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

param = {'bst:max_depth':30, 'bst:eta':0.3, 'silent':1, 'objective':'binary:logistic', gamma}
param['nthread'] = 10
param['eval_metric'] = 'logloss'
num_round = 400
bst = xgb.train(param, dtrain)
preds = bst.predict(dtest).round()
accuracy_score(y_test, preds)


# %%
lr.fit(X_train, y_train)
lr.score(X_test, y_test)

# %% train a neural network on the yan dataset

clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(10,), random_state=1, activation='logistic')
clf.fit(X_train, y_train)

score = clf.score(X_test, y_test)


# %% train neural network on the kaggle dataset
kgl_df = pd.read_csv("../../../datasets/interim/train_draft_kgl.csv")
kgl_df_test = pd.read_csv("../../../datasets/interim/test_draft_kgl.csv")

y_train = kgl_df["radiant_win"].to_numpy()
y_test = kgl_df_test["radiant_win"].to_numpy()

# drop unnecessary cols
X_train = kgl_df.drop(['Unnamed: 0', "match_id", "radiant_win"], axis=1).to_numpy()
X_test = kgl_df_test.drop(['Unnamed: 0', "match_id", "radiant_win"], axis=1).to_numpy()

clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(10,), random_state=1, activation='relu')
clf.fit(X_train, y_train)

score = clf.score(X_test, y_test)

# %%
