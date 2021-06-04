import zerorpc

class Node(object):
    def __init__(self):
        self.service = None

    def create_service(self):
        return NotImplementedError

    def get_service(self):
        if not self.service:
            self.service = self.create_service()
        return self.service





class LocalService(object):
    def __init__(self):
        self._service = None

    def _create_service(self):
        raise NotImplementedError

    def get_service(self):
        if not self._service:
            self._service = self._create_service()
        return self._service

class LocalNode(Node):
    def create_service(self):
        return  LocalService()
