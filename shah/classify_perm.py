# Load scikit's random forest classifier library
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn import tree
from sklearn import neighbors
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
# Load pandas
import pandas as pd

# Load numpy
import numpy as np

# Create a dataframe with the four feature variables
train = pd.read_csv('/home/shahrear/SHAH_PROJECTS/google-play-scraper/shah/training_data.csv')

test = pd.read_csv('/home/shahrear/SHAH_PROJECTS/google-play-scraper/shah/test_data.csv')

features = train.columns[:192]
#
# #gaussian
# clf = GaussianNB()
#
# clf.fit(train[features], train['class'])
#
# preds = clf.predict(test[features])
#
# print confusion_matrix(test['class'], preds)
#
# print classification_report(test['class'], preds)
#
# #svm
# clf = svm.SVC()
#
# clf.fit(train[features], train['class'])
#
# preds = clf.predict(test[features])
#
# print confusion_matrix(test['class'], preds)
#
# print classification_report(test['class'], preds)
#
# #DecisionTree
# clf = tree.DecisionTreeClassifier()
#
# clf.fit(train[features], train['class'])
#
# preds = clf.predict(test[features])
#
# print confusion_matrix(test['class'], preds)
#
# print classification_report(test['class'], preds)
#
# #kNN
# clf = neighbors.KNeighborsClassifier(15, 'uniform')
#
# clf.fit(train[features], train['class'])
#
# preds = clf.predict(test[features])
#
# print confusion_matrix(test['class'], preds)
#
# print classification_report(test['class'], preds)

#RandomForest
clf = RandomForestClassifier(n_jobs=-1)

clf.fit(train[features], train['class'])

preds = clf.predict(test[features])

print confusion_matrix(test['class'], preds)

print classification_report(test['class'], preds)


