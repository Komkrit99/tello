from sklearn.datasets import load_iris 
from sklearn.model_selection import train_test_split 
from sklearn.neighbors import KNeighborsClassifier
import pickle
import pandas as pd

hand = pd.read_csv('hand_df.csv')
# print(hand)
y = hand['label']
X = hand.drop(columns=['label','Unnamed: 0'])

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=4)
# build KNN model and choose n_neighbors = 5
knn = KNeighborsClassifier(n_neighbors = 9)
# train the model
knn.fit(X_train.values, y_train)
# get the predict value from X_test
y_pred = knn.predict(X_test)
# print the score
print('accuracy: ', knn.score(X_test, y_test))

filename = 'finalized_model.sav'
pickle.dump(knn, open(filename, 'wb'))

loaded_model = pickle.load(open(filename, 'rb'))
print(loaded_model.predict(X_test))
print(X_test)