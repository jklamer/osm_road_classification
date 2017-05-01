from keras.models import Sequential
from keras.layers import Dense, Activation
import numpy as np
import pandas as pd
import sys


model = Sequential()

for arg in sys.argv:
    df = pd.read_csv(arg)
    X = df.ix[:, :-1]
    y = df.ix[:, -1]

    n_instances, n_features = X.shape

    X = X.values
    y = y.values
    print(X[2])
    for k in y:
        if isinstance(y, float):
            print(y)
    #classes = np.unique(y)
    #print(classes)
    exit()

    model.add(Dense(32, activation='relu', input_dim = n_features))
    model.add(Dense(10, activation='softmax'))
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
