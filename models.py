import pandas as pd
import numpy as np
from numpy.core.defchararray import strip
from tensorflow import keras

MODEL_PATHS = ["MLP_model.h5", "CNN_model.h5", "GRU_model.h5"]
EXAMPLE_FILES = ["Example1.csv", "Example2.csv", "Example3.csv"]

# This needs to be changed to a dataframe or dictionary so it displays the input parameters nicely
EXAMPLE_LABELS = [[1,1,1,1,1], [2,2,2,2,2], [3,3,3,3,3]]

MODEL_NAMES = ["MLP", "CNN", "GRU"]
COLUMN_NAMES = \
    ["Model Type",
 "Readily Biodegradable Substrate",
 "Slowly Biodegradable OM",
 "Soluble NH4-N Concentration",
 "Soluble Biodegradable O-N Concentration",
 "Particulate Biodegradable O-N"]

class Model():
    def __init__(self, path):
        self.model = keras.models.load_model(path)
        self.sample_maxes = [5.77305055620045, 0.009540294233475, 0.0058713081660306, 1.26923574748256e-08]
        self.sample_mins = [0.0281795730197485, 0.0, 0.0, 0.0]
        self.label_maxes = [159.9858, 408.9682, 64.995, 12.9996, 33.998]
        self.label_mins = []

    def reshape(X):
        return X

    # ensures samples are scaled using the training data Min-Max-Scaling parameters
    def scale(self, X):
        scaled_X = np.zeros(X.shape)
        for i in range(4):
            scaled_X[:,i,:] = (X[:,i,:] - self.sample_mins[i]) / (self.sample_maxes[i]-self.sample_mins[i])
        return scaled_X

    # un-scales the labels from [0,1] to the original range
    def un_scale(Y):
        un_scaled_X = np.zeros(Y.shape)
        for i in range(5):
            un_scaled_X[:, i, :] = X[:, i, :] * (self.sample_maxes[i] - self.sample_mins[i]) + self.sample_mins[i]
        return scaled_X

    def predict_(self, X):
        return un_scale(self.model.predict_(transform(scale(X.to_numpy())).numpy()))

class CNN_Model(Model):
    def __init__(self, path):
        super().__init__(path)

class RNN_Model(Model):
    def __init__(self, path):
        super().__init__(path)

    def reshape(X):
        reshaped_X = np.zeros((len(X), 96, 4))
        for i in range(len(X)):
            reshaped_X[i] = X[i].T
        return reshaped_X

class MLP_Model(Model):
    def __init__(self, path):
        super().__init__(path)

    def reshape(X):
        return np.array([X[i, :, :].flatten() for i in range(len(X))])

class ModelList():
    def __init__(self):
        self.mlp = MLP_Model(MODEL_PATHS[0])
        self.cnn = CNN_Model(MODEL_PATHS[1])
        self.rnn = RNN_Model(MODEL_PATHS[2])
        self.list = [self.mlp, self.cnn, self.rnn]

    def predict_all(self, input_X):
        predictions = np.zeros((len(self.list), 7))
        for i in range(len(self.list)):
            predictions[i] = list[i].predict(input_X)
        return pd.DataFrame((MODEL_NAMES, predictions), columns=COLUMN_NAMES)

class Example():
    def __init__(self, file=None, DO_col=1, NO3_col=2, NH4_col=3, MH_col=4):
        cols_to_keep = [DO_col, NO3_col, NH4_col, MH_col]

        if file == None:
            self.example_data = []
            self.display_data = []
            num=0
            for file_name in EXAMPLE_FILES:
                self.display_data.append(pd.DataFrame(pd.read_csv(file_name)))
                self.example_data.append(self.display_data[num].iloc[:, cols_to_keep])
                num+=1
        else:
            self.display_data = pd.DataFrame(pd.read_csv(file))
            self.example_data = self.display_data.iloc[:, cols_to_keep]

        self.models = ModelList()

    def run_example(self, example_number):
        return self.models.predict_all(self.example_data[example_number-1])

    def run_custom(self):
        return self.models.predict_all(self.example_data)

    def disp_example(self, example):
       try:
        return EXAMPLE_LABELS[example-1]
       except:
        return "No example selected"