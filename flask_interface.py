# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 16:32:25 2013

@author: Ari Ramdial
"""
import ast
import numpy as np
from GIM import SimulateCobelliDay as predict

from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

"""
PARSE JSON REQUEST
"""
def jsonparse(x):
    CHO = 0
    for key, value in x.iteritems():
        val = ast.literal_eval(value)
        carb = int(val.get("carb_p_serv"))
        CHO += carb
    return CHO
    
"""
RUN PREDICTION ALGORITHM
"""    
def test(y):
    # Input array for model
    BW = 70
    eatingTime = 30
    bHour = 7
    bMin = 0
    bCHO = y
    bInsulin = 0
    lHour = 0
    lMin = 0
    lCHO = 0
    lInsulin = 0
    dHour = 0
    dMin = 0
    dCHO = 0
    dInsulin = 0
    modelData = np.array([BW,
                          bHour,bMin,bCHO,bInsulin,
                          lHour,lMin,lCHO,lInsulin,
                          dHour,dMin,dCHO,dInsulin,
                          eatingTime,1,0,0,0,1,0,0,0])
    
    # Call GIM model
    f = predict(modelData)
    return f

    
@app.route("/")
def webprint(): 
    return render_template('webcode.html') 
    
    
"""
THIS IS a test on the local machine

"""      
@app.route('/user/<user_id>')
def ping(user_id):
    # pull from cassandra 
    r = requests.get("http://198.61.177.186:8080/virgil/data/glucoseapp/menu/%s" % user_id)
    
    # Encode response as UTF-8 formatted string
    data = r.text
    
    # Convert string to list
    data1 = ast.literal_eval(data)
    
    # Parse list and return carb input
    y = jsonparse(data1)
    
    # Call prediction algorithm
    z = test(y)
    
    # Convert glucose levels (2nd index) to json
    glucose = jsonify(G=z[1])
    
    #s = requests.put("http://198.61.177.186:8080/virgil/data/glucoseapp/results/%s" % timestamp)
    #carbinput = jsonparse(data.read())
    #out = test(carbinput)
    return glucose   
    
    
if __name__ == "__main__":
    app.run(host='198.61.177.186')
    

