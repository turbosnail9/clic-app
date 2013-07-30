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
import urllib2


def jsonparse():
    CHO = 0
    response = urllib2.urlopen("http://198.61.177.186:8080/virgil/data/glucoseapp/menu/1")
    data = json.load(response)  
    for key, value in data.iteritems():
        val = ast.literal_eval(value)
        carb = int(val.get("carb_p_serv"))
        CHO += carb
    return CHO
            
       
    
    
def test(x):
    #carbval = jsonparse()
    modelData = np.array([70,7,0,x,2000,13,0,70,3000,18,0,70,3000,30,1,0,0,0,1,0,0,0])
    
    f = runModel(modelData)
    print f
    #pyplot.plot(f[1])
    return f


test(jsonparse())