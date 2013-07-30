# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 16:32:25 2013

@author: Ari Ramdial
"""
import numpy as np
from GIM import SimulateCobelliDay as runModel
from matplotlib import pyplot
import json
import ast


from flask import Flask, request, Response, jsonify
import requests
app = Flask(__name__)

def jsonparse(x):
    CHO = 0
    #response = urllib2.urlopen("http://198.61.177.186:8080/virgil/data/glucoseapp/menu/1")
    #data = json.load(response)  
    for key, value in x.iteritems():
        val = ast.literal_eval(value)
        carb = int(val.get("carb_p_serv"))
        CHO += carb
    return CHO
    
    
def test(y):
    modelData = np.array([70,7,0,y,2000,13,0,70,3000,18,0,70,3000,30,1,0,0,0,1,0,0,0])
    
    f = runModel(modelData)
    #pyplot.plot(f[1])
    return f
@app.route("/")
def hello():
    return "blah World!"
    
@app.route("/puppies")
def puppies():
    return "PUPPIES!!"
    
"""
THIS IS a test on the local machine

"""      
#@app.route('/user/<user_id>')
#def ping(user_id):
#    # pull from cassandra 
#    r = requests.get("http://198.61.177.186:8080/virgil/data/glucoseapp/menu/%s" % user_id)
#    data = r.text 
#    data1 = ast.literal_eval(data)
#    y = jsonparse(data1)
#    z = test(y)
#    glucose = jsonify(G=z[1])
#    
#    s = requests.put("http://198.61.177.186:8080/virgil/data/glucoseapp/results/%s" % timestamp)
#    #carbinput = jsonparse(data.read())
#    #out = test(carbinput)
#    return jsonify(G=z[1])   
    
@app.route('/menu/<timestamp>')
def ping_cassandra(timestamp):
    # pull from cassandra 
    r = requests.get("http://198.61.177.186:8080/virgil/data/glucoseapp/menu/%s" % timestamp)
    data = r.text 
    data1 = ast.literal_eval(data)
    y = jsonparse(data1)
    z = test(y)
    glucose = jsonify(G=z[1])
    s = requests.put("http://198.61.177.186:8080/virgil/data/glucoseapp/results/%s" % timestamp, data = glucose)
    return s
    
if __name__ == "__main__":
    app.run(debug = True)
    

