from flask import Flask,jsonify,request,abort
from collections import OrderedDict
import json
import os
app=Flask("__main__")
#loading  tasks data from the file 
data_file="tasks.json"
try:
    # Try to open and load existing tasks
    with open(data_file, "r") as f:
        tasks = json.load(f, object_pairs_hook=OrderedDict)
        f.close()
except (FileNotFoundError, json.JSONDecodeError):
    # If file is missing or empty, initialize tasks as an empty list
    tasks = []
    
#saving tasks to file 
def saveinfo():
    with open(data_file,'w') as f:
        json.dump(tasks,f,indent=4)
    f.close()
    

#route for homepage 
@app.route("/")
def home():
    return("Welcome to task management application !")
    
#creating a task that contains title,status,taskid in json form .

#CREATE 

@app.route("/tasks",methods=["POST"])
def addtask():
    task_details=request.get_json()
    if not task_details or not task_details['title']:
        abort(400,"Task title is required")
    #add a task
    task=OrderedDict()
    task["taskid"] = len(tasks)+1
    task["title"] =task_details['title']
    task["status"] = task_details.get('status', 'pending') 
    task["description"] = task_details.get('description', '')
    tasks.append(task)
    saveinfo()
    return jsonify(task)

#get the list of the tasks 

#READ
@app.route('/tasks',methods=["GET"])
def display():
    return(jsonify(tasks))

#get task details by task id 
@app.route('/tasks/<int:task_id>',methods=["GET"])
def taskbyid(task_id):
    task=next((task for task in tasks if task['taskid']==task_id),None)
    if(task == None):
        abort(400,"Task not found ")
    return(jsonify(task))
    

#update 
@app.route('/tasks/<int:task_id>',methods=["PUT"])
def update(task_id):
    task=next((task for task in tasks if task['taskid']==task_id),None)
    if(task == None):
        abort(400,"Task not found ")
    else:
        task_data=request.get_json()
        task['description']=task_data.get('description',task['description'])
        task['title']=task_data.get('title',task['title'])
        task["status"] = task_data.get('status',task['status'])  
    saveinfo()
    return(jsonify(task))

#DELETE TASK

@app.route('/tasks/<int:task_id>',methods=["DELETE"])
def delete(task_id):
    task=next((task for task in tasks if task['taskid']==task_id),None)
    if(task==None):
        abort(400,"Task not foound")
    else:
        tasks.remove(task)
    saveinfo()
    return jsonify({"message":"Task deleted"}),200
        
    
if __name__=="__main__":
    app.run(debug=True) 