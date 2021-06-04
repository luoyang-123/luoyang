from node import LocalNode,RemoteNode
from  flask import Blueprint,current_app,request
webapp = Blueprint('luoyang', __name__)



@webapp.route("/register")
def register():
    nodes=request.remote_addr + ":" + request.args["port"]
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



