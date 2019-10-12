#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import random
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app) 
from pprint import pprint
Graph_Container = dict()
from fuzzywuzzy import process,fuzz
from Graph import *
from Intent import extract_and_get_intent
from DB import saveRating


# In[10]:


def msg(code, mess=None):
    if code == 200 and mess is None:
        return jsonify({"code":200, "value": True})
    else:
        return jsonify({"code": code, "message": mess}), code


# In[11]:


def get_new_id():
    while (True):
        _id = str(random.randint(100000, 999999))
        if _id not in Graph_Container.keys():
            return _id


# In[12]:


def process_save_POST(data):
    data["timestamp"] = int(round(time.time() * 1000))
    rating_collection.insert_one(data)
    return "saved"


# In[13]:


def process_conversation_POST(graph_id, message):
    graph = None
    if graph_id in Graph_Container.keys():
        graph = Graph_Container[graph_id]
    else:
        graph = HuongNghiep_Graph()
        Graph_Container[graph_id] = graph
    
    extracted, extracted_dict, candidate_intent_dict = extract_and_get_intent(message)
    graph.fill(extracted_dict, candidate_intent_dict)


# In[14]:


def process_conversation_GET(graph_id):
    returnMesg = None
    graph = Graph_Container[graph_id]
    isDone, returnMesg = graph.getResponse()
            
    returnDict = dict()
    if isDone:
        returnDict["answer"] = returnMesg
    else:
        returnDict["question"] = returnMesg
    returnDict["isDone"] = isDone   
    returnDict["graph"] = list(graph.intents.keys())
    return returnDict


# In[ ]:





# In[ ]:


@app.route('/')
def index():
    return """<h1>Tư vấn hướng nghiệp - Hồ Lê Phương Thọ</h1>"""

@app.errorhandler(404)
def url_error(e):
    return msg(404, "NOT FOUND")

@app.errorhandler(500)
def server_error(e):
    return msg(500, "SERVER ERROR")

#input_data: { message: <text>, graph_id: <something>}

@app.route('/api/conversation-manager', methods=['POST'])
def post_api():
    input_data = request.json
    print(input_data)
    if "message" not in input_data.keys(): 
        return msg(400, "Message cannot be None")
    else:
        message = input_data["message"]
    if "graph_id" not in input_data.keys(): 
        graph_id = get_new_id()
    else:
        graph_id = input_data["graph_id"]
    pprint('\n   API POST: graph: ' + graph_id + " message: " + message)
    process_conversation_POST(graph_id, message)
    return msg(200, "Graph_id: " + str(graph_id))

@app.route('/api/conversation-manager', methods=['GET'])
def get_api():
    graph_id = request.args.get('graph_id')
 
    if graph_id is None: 
        return msg(400, "Graph ID cannot be None")    
    if graph_id not in Graph_Container.keys():
        return msg(404, "Graph not found")
    
    output_data = process_conversation_GET(graph_id)
    return jsonify(output_data)

@app.route('/api/conversation-manager', methods=['DELETE'])
def delete_api():
    graph_id = request.args.get('graph_id')
    new_node_name = request.args.get('new_node')
    if graph_id is None: 
        return msg(400, "Graph ID cannot be None")   
    if graph_id not in Graph_Container.keys():
        return msg(404, "Graph not found")
    else:
        Graph_Container.pop(graph_id)
        return msg(200, "Pop graph " + str(graph_id))
        
@app.route('/api/save-rating-conversation', methods=['POST'])
def post_save_rating_conversation():
    input_data = request.json
    saved = saveRating(input_data)
    return msg(200, saved)

if __name__ == '__main__':
    app.run()


# In[ ]:





# In[ ]:





# In[ ]:




