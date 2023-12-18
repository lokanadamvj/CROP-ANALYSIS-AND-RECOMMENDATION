import pickle
from flask import *
import numpy as np
import pandas as pd
import os
def predict(inputs):        
    # load the model from disk
    unique_values = pickle.load(open('unique_values_pickle_file', 'rb'))    
    # load the model from disk
    scaler = pickle.load(open('scalerpickle_file', 'rb'))
    # load the model from disk
    knn = pickle.load(open('knnpickle_file', 'rb'))

    #X_test = [[90,42,43,20.879744,82.002744,6.502985,202.935536]]
    X_test = [inputs]

    X_test_scaled = scaler.transform(X_test)

    result = knn.predict(X_test_scaled)

    result = unique_values[result]    