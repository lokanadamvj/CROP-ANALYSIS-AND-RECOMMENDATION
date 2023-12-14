import pickle
from flask import *
import numpy as np
import pandas as pd
import os
#import sklearn
#from sklearn.neighbors import KNeighborsClassifier
app = Flask(__name__)

f=open('args.txt')
args=f.readlines()
f.close()

@app.route('/')
def index():
    return render_template('index.html', args=args)

@app.route('/about')
def about():
    return render_template('about.html', args=args)

@app.route('/train')
def train():
    os.system("jupyter notebook crop-analysis-and-prediction.ipynb")
    return render_template('train.html', args=args)

@app.route('/parameters', methods=['GET'])
def parameters():
    return render_template('parameters.html', args=args)

@app.route('/team')
def team():
    return render_template('team.html', args=args) 

@app.route('/predict', methods=['GET'])
def predict():        
    # load the model from disk
    unique_values = pickle.load(open('unique_values_pickle_file', 'rb'))    
    # load the model from disk
    scaler = pickle.load(open('scalerpickle_file', 'rb'))
    # load the model from disk
    knn = pickle.load(open('knnpickle_file', 'rb'))

    District=request.args.get("District")
    N=request.args.get("N")
    P=request.args.get("P")
    K=request.args.get("K")
    temperature=request.args.get("temperature")
    humidity=request.args.get("humidity")
    ph=request.args.get("ph")
    rainfall=request.args.get("rainfall")
    #label=request.args.get("label")

    #X_test = [[90,42,43,20.879744,82.002744,6.502985,202.935536]]
    X_test = [[N,P,K,temperature,humidity,ph,rainfall]]

    X_test_scaled = scaler.transform(X_test)

    result = knn.predict(X_test_scaled)

    result = unique_values[result]


    return render_template('predict.html', args=args, result=result)

if __name__ == "__main__":
    ## Uncomment for flask only (no docker container)
    #app.run(debug=True)
    ## Comment out for flask only (no docker container)
    app.run(host="0.0.0.0", port=8080)