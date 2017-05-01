from keras.models import Sequential
from keras.layers import Dense, Activation
import keras
import numpy as np
import pandas as pd
import sys

classes={"motorway","trunk","primary","secondary","tertiary","unclassified","residential","service"}



def label_binarize(y):
    """Binarize labels in a one-vs-all fashion using one-hot encoding.

    The output will be a matrix where each column corresponds to one possible
    value of the input array, with the number of columns equal to the number
    of unique values in the input array.

    Parameters
    ----------
    y : array, shape = [n_instances,]
        Sequence of integer labels to encode.

    Returns
    -------
    y_bin : array, shape = [n_instances, n_classes]
        Binarized array.
    """
    n_instances = len(y)
    classes_ = np.unique(y)

    y_bin = np.zeros((n_instances, len(classes_)))
    for y_i in classes_:
        i = classes_.searchsorted(y_i)
        idx = np.where(y == y_i)
        y_bin[idx, i] = 1

    return y_bin


for arg in sys.argv[1:]:
    df = pd.read_csv(arg)

    X = df.ix[:, :-1]
    y = df.ix[:, -1]
    n_instances, n_features = X.shape
    X = X.values
    y = y.values.reshape((n_instances, 1))
    y_hot= label_binarize(y)

    model = Sequential()
    model.add(Dense(10, activation='relu', input_dim = n_features))
    model.add(Dense(len(classes), activation='softmax'))
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(X, y_hot, epochs=5, batch_size = 50)

    score = model.evaluate(X, y_hot, batch_size = 50)
    print("\nScore:{}".format(score))
