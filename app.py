from flask import Flask
from logging import getLogger
from gevent.pywsgi import WSGIServer
import click
import requests
import zerorpc
from tset import webapp
from node import LocalNode

logger = getLogger('psdash.run_web')

class PsDashRunner():


    def __init__(self, *args, **kwargs):
        self.post = kwargs['post']
        self.host = kwargs['host']
        self.name = kwargs['name']
        self.rpc = kwargs['rpc']
        self.local = LocalNode()
        self._nodes = {}

    def create_app(self):

        app = Flask(__name__)
        app.psdash = self
        app.register_blueprint(webapp)
        self.app=app


    def get_local_node(self):
        return self._nodes.get(self.host)

    def _run_web(self):
        self.create_app()
        print(self.name)
        print('PSDASH_BIND_HOST:', self.host),
        print('PSDASH_PORT:', self.post)
        self._nodes[f"{self.name}:localnode:{self.post}"]= self.local
        self.server = WSGIServer(
            (self.host,self.post),
            application=self.app,
        )
        self.server.serve_forever()


    def run_as_rpc(self):
        print('启动{}:{}rpc server'.format(self.host,self.post))

        service = self.get_local_node().get_service()
#        requests.get(self.rpc + f"/register?port={self.post}&name={self.name}")
        self.server = zerorpc.Server(service)
        self.server.bind('tcp://%s:%s' %({self.host},{self.post}))
        self.server.run()



@click.command()
@click.option('-a', '--rpc', default='None', help='启动代理注册')
@click.option('-h', '--host', default='0.0.0.0', help='host')
@click.option('-p', '--post',type=int, default=5000, help='post')
@click.option('-n', '--name', default='localhost', help='节点名字')
def aa(name,host,post,rpc):
    run = PsDashRunner(**locals())
    run._run_web()

    if rpc :
        run.run_as_rpc()
    else:
        run._run_web()

if __name__ == '__main__':
    aa()