from keras.models import Sequential
from keras.layers import Dense, Activation
import keras
import numpy as np
import pandas as pd
import sys

classes={"motorway","trunk","primary","secondary","tertiary","unclassified","residential","service"}


for arg in sys.argv[1:]:
    df = pd.read_csv(arg)

    X = df.ix[:, :-1]
    y = df.ix[:, -1]
    n_instances, n_features = X.shape
    print(n_features)
    X = X.values
    y = y.values.reshape((n_instances, 1))
    print(np.shape(y))
    y_hot= keras.utils.to_categorical(y, num_classes=len(classes))

    model = Sequential()
    model.add(Dense(32, activation='relu', input_dim = n_features))
    model.add(Dense(len(classes), activation='softmax'))
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(X, y_hot, epochs=2, batch_size = 50)

    score = model.evaluate(X, y_hot, batch_size = 50)
