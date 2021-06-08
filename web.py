from  flask import Blueprint,current_app,request
import jsonify
import json
webapp = Blueprint('luoyang', __name__)
_webapp = Blueprint('luoyang', __name__)

@webapp.route("/")
def aa():
    return '大家好，我是罗洋'

@webapp.route("/register")
def register():
    nodes=request.remote_addr + ":" + request.args["port"]
    print(nodes)
    if nodes not in current_app.psdash._nodes:
        current_app.psdash.register_agent(nodes,request.args["name"])
    return ""

@webapp.route("/nodes")
def nodes():
    a=[]
    for node in  current_app.psdash._nodes:
        node=node.split(":")
        a.append({"nodename":node[0],"ip":node[1],"port":int(node[2])})
    return str(a)
@webapp.route("/<name>/memory")
def memory(name):
    memory=current_app.psdash._Node[name]['memory']
    memory={"name":name,"Total memory":memory[1],"Memory used":memory[0],"Remaining memory":memory[3]}
    memory = json.dumps(memory)
    return memory

@webapp.route("/<name>/time")
def _time(name):
    print(current_app.psdash._Node[name])
    __time= current_app.psdash._Node[name]['time']

    return str(__time)

@webapp.route("/<name>/Network")
def Network(name):
    _network = current_app.psdash._Node[name]['Network']

    return _network
@webapp.route("/<name>/Process")
def Process(name):
    _Process = current_app.psdash._Node[name]['Process']

    return _Process

@webapp.route("/<name>/disk")
def _disk(name):
    disk = current_app.psdash._Node[name]['disk']

    return disk



