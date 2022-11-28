import pandas as pd
import numpy as np
from tensorflow import keras

MODEL_PATHS = ["MLP_model.h5", "CNN_model.h5", "GRU_model.h5"]

MODEL_NAMES = [["MLP"], ["CNN"], ["GRU"]]
COLUMN_NAMES = ["Model Type",
     "Readily Biodegradable Substrate",
     "Slowly Biodegradable OM",
     "Soluble NH4-N Concentration",
     "Soluble Biodegradable O-N Concentration",
     "Particulate Biodegradable O-N"]


class Model():
    def __init__(self, path):
        self.model = keras.models.load_model(path)
        self.sample_maxes = [5.47953264264528, 0.009540294233475, 0.0058713081660306, 2.46425683526441e-08]
        self.sample_mins = [0.0068592823106617, 0.0, 0.0, 0.0]
        self.label_maxes = [159.9858, 408.9682, 64.995, 12.9996, 33.998]
        self.label_mins = [2.5614e-02, 9.0985, 1.0017, 1.8174e-05, 9.5180e-03]

    def reshape(self, X):
        return np.reshape(X, newshape=(1, 4, 96))

    # ensures samples are scaled using the training data Min-Max-Scaling parameters
    def scale(self, X):
        scaled_X = np.zeros(X.shape)
        for i in range(4):
            scaled_X[i, :] = (X[i, :] - self.sample_mins[i]) / (self.sample_maxes[i] - self.sample_mins[i])
        return scaled_X

    # un-scales the labels from [0,1] to the original range
    def un_scale(self, Y):
        un_scaled_Y = np.zeros(Y.shape)
        for i in range(5):
            un_scaled_Y[:, i] = (Y[:, i] * (self.label_maxes[i] - self.label_mins[i])) + self.label_mins[i]
        return un_scaled_Y

    def predict_(self, X):
        scaled = self.scale(X)
        input = self.reshape(scaled)
        prediction = self.model.predict(input)
        return self.un_scale(prediction)


class CNN_Model(Model):
    def __init__(self, path):
        super().__init__(path)


class RNN_Model(Model):
    def __init__(self, path):
        super().__init__(path)

    def reshape(self, X):
        return np.reshape(X.T, newshape=(1, 96, 4))


class MLP_Model(Model):
    def __init__(self, path):
        super().__init__(path)

    def reshape(self, X):
        return np.reshape(X[:, :].flatten(), newshape=(1, 384))


class ModelList:
    def __init__(self):
        self.mlp = MLP_Model(MODEL_PATHS[0])
        self.cnn = CNN_Model(MODEL_PATHS[1])
        self.rnn = RNN_Model(MODEL_PATHS[2])
        self.list = [self.mlp, self.cnn, self.rnn]

    def predict_all(self, input_X):
        results = pd.DataFrame(np.zeros((len(self.list), 5)), columns=COLUMN_NAMES[1:])
        results.iloc[0, :] = self.mlp.predict_(input_X)
        results.iloc[1, :] = self.cnn.predict_(input_X)
        results.iloc[2, :] = self.rnn.predict_(input_X)
        models = pd.Series(MODEL_NAMES, name=COLUMN_NAMES[0])
        return pd.concat([models, results], axis=1)


class Example:
    def __init__(self, input_df, DO_col=1, NO3_col=2, NH4_col=3, MH_col=4):
        cols_to_keep = [DO_col, NO3_col, NH4_col, MH_col]

        self.example_data = input_df.T.to_numpy()[cols_to_keep, :96]
        self.models = ModelList()

    def predict_(self):
        return self.models.predict_all(self.example_data)
