from  flask import Blueprint,current_app,request,jsonify
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
    a={}
    for node in  current_app.psdash._nodes:
        node=node.split(":")
        a[str(node[0])]={"nodename":node[0],"ip":node[1],"port":int(node[2])}
    return str(a)

@webapp.route("/<name>/<test>")
def memory(name,test):
    current_service=current_app.psdash.Node[name].get_service()
    if test=="memory":
        return current_service.memory()
    elif test=="disk":
        return  current_service.Magnetic_disk()
    elif test == "time":
        return current_service.htime()
    elif test == "Process":
        return  current_service.Process()
    elif test == "Network":
        return  current_service.Network()





