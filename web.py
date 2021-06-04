
from  flask import Blueprint,current_app,request
webapp = Blueprint('luoyang', __name__)


@webapp.route("/register")
def register():
    nodes=request.remote_addr + ":" + request.args["port"]
    if nodes not in current_app.psdash.nodes:
        current_app.psdash.register_agent(nodes,request.args["name"])
    return ""

@webapp.route("/nodes")
def nodes():
    a=[]
    for node in  current_app.psdash.nodes:
        node=node.split(":")
        a.append({"hostname":node[0],"host":node[1],"port":int(node[2])})
    return str(a)



