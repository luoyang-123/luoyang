from flask import Flask
from gevent.pywsgi import WSGIServer
import click
import requests
import zerorpc
from web import webapp ,_webapp
from node import LocalNode,RemoteNode
import psutil

class PsDashRunner():

    def __init__(self, *args, **kwargs):
        self.port = int(kwargs['port'])
        self.host = kwargs['host']
        self.name = kwargs['name']
        self.rpc = kwargs['rpc']
        self.local = LocalNode()
        self._nodes = {}
        self._Node={}
    def create_app(self):

        app = Flask(__name__)
        app.psdash = self
        app.register_blueprint(webapp)
        self.app=app

    def register_agent(self,node,name):   #作为rpc server 启动时，向http server 注册
        print(f"已注册 {node}")
        print(name)
        host,port= node.split(":")
        self._nodes[f'{name}:{node}']=RemoteNode(host,port)   #远端数据存储
        self.agent(name)

    def agent(self,name):
        self._Node[name]={'time':LocalNode()._time()}
        self._Node[name]['memory'] = psutil.virtual_memory()
        self._Node[name]['Network']=LocalNode().Network()
        self._Node[name]['Process'] = LocalNode().Process()
        self._Node[name]['disk'] = LocalNode().Magnetic_disk()

    def _run_web(self):
        self.create_app()
        print('name:',self.name)
        print('PSDASH_BIND_HOST:', self.host),
        print('PSDASH_PORT:', self.port)
        self.agent(self.name)
        self._nodes[f"{self.name}:localnode:{self.port}"]= self.local
        self.server = WSGIServer((self.host,self.port),application=self.app,)
        self.server.serve_forever()


    def run_as_rpc(self):
        print('启动{}:{}rpc server'.format(self.host,self.port))

        service = self.local.get_service()
        requests.get(self.rpc + f"/register?port={self.port}&name={self.name}")

        self.server = zerorpc.Server(service)

        self.server.bind('tcp://%s:%s' %(self.host,self.port))
        self.server.run()


@click.command()
@click.option('-a', '--rpc', default=None, help='启动代理注册')
@click.option('-h', '--host', default='0.0.0.0', help='host')
@click.option('-p', '--port',type=int, default=5000, help='port')
@click.option('-n', '--name', default='localhost', help='节点名字')
def aa(name,host,port,rpc):
    run = PsDashRunner(**locals())
    if rpc :
        run.run_as_rpc()
    else:
        run._run_web()

if __name__ == '__main__':
    aa()