# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 16:32:25 2013

@author: Ari Ramdial
"""
import requests
from flask import json, jsonify

def reqtest():
    url = "http://localhost:5000/reqtest"
    data = {'carb_p_serv':'3','erg':'42'}
    #headers = {'content-type': 'application/json','Accept': 'text/plain'}
    requests.put(url, data=json.dumps(data)) 
    
reqtest()
