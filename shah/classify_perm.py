# Load scikit's random forest classifier library
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
# Load pandas
import pandas as pd

# Load numpy
import numpy as np

# Create a dataframe with the four feature variables
train = pd.read_csv('/home/shahrear/SHAH_PROJECTS/google-play-scraper/shah/training_data.csv')

test = pd.read_csv('/home/shahrear/SHAH_PROJECTS/google-play-scraper/shah/test_data.csv')

features = train.columns[:192]

clf = RandomForestClassifier(n_jobs=-1)



clf.fit(train[features], train['class'])

preds = clf.predict(test[features])

print list(zip(train[features], clf.feature_importances_))

print pd.crosstab(test['class'], preds, rownames=['Actual'], colnames=['Predicted'])

print precision_score(test['class'], preds, average='macro')

print accuracy_score(test['class'], preds)

print f1_score(test['class'], preds, average='macro')

print recall_score(test['class'], preds, average='macro')

print confusion_matrix(test['class'], preds)

print classification_report(test['class'], preds)

# clf = GaussianNB()
#
# clf.fit(train[features], train['class'])
#
# preds = clf.predict(test[features])
#
# print pd.crosstab(test['class'], preds, rownames=['Actual'], colnames=['Predicted'])
#
# print precision_score(test['class'], preds, average='macro')
#
# print accuracy_score(test['class'], preds)
#
# print f1_score(test['class'], preds, average='macro')
#
# print recall_score(test['class'], preds, average='macro')
#
# print confusion_matrix(test['class'], preds)
#
# print classification_report(test['class'], preds)
#
# clf = svm.SVC()
#
# clf.fit(train[features], train['class'])
#
# preds = clf.predict(test[features])
#
# print pd.crosstab(test['class'], preds, rownames=['Actual'], colnames=['Predicted'])
#
# print precision_score(test['class'], preds, average='macro')
#
# print accuracy_score(test['class'], preds)
#
# print f1_score(test['class'], preds, average='macro')
#
# print recall_score(test['class'], preds, average='macro')
#
# print confusion_matrix(test['class'], preds)
#
# print classification_report(test['class'], preds)