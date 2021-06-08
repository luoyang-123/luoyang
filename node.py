
import psutil, datetime
import json
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


class RemoteNode(Node):
    def __init__(self,host,port):
        self.host = host
        self.port = int(port)

    def create_service(self):
        client = zerorpc.Client()
        client.connect('tcp://%s:%s' % (self.host, self.port))
        return client



class LocalService(object):
    def get_memory(self):
        return psutil.virtual_memory()

class LocalNode(Node):
    def create_service(self):
        return  LocalService()
    def _time(self):
        # 转换成自然时间格式
        Time={'time':datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H: %M: %S")}
        Time=json.dumps(Time)
        return Time


    def Network(self):
        Io = psutil.net_io_counters()  # 获取网络IO的信息；
        IO= {'bytes_sent': str(Io[0]), 'bytes_recv': str(Io[1]), 'packets_sent': str(Io[2]), 'packets_recv': str(Io[3]),
                'errin': str(Io[4]), 'errout': str(Io[5]), 'dropin': str(Io[6]), 'dropout': str(Io[6])}
        print(IO)
        IO = json.dumps(IO)
        return IO

    def Magnetic_disk(self):
        P = psutil.disk_partitions()  # 获取磁盘分区的信息；
        p ={}
        for i in range(len(P)):
            disk = {'device': str(P[i][0]), 'mountpoint': str(P[i][1]), 'fstype': str(P[i][2]), 'opts': str(P[i][3]),
                    'maxfile': str(P[i][4]), 'maxpath': str(P[i][5])}
            p[str(i)]=disk
        p = json.dumps(p)
        return p

    def Process(self):
        s={}
        index = 0

        for i in psutil.pids():
            try:
                p = psutil.Process(i)
                exe=str(p.exe())
                p={'name':str(p.name()),' pid':str(p.pid),' status':str(p.status())}
                s[str(index)] = {'pids':p}
                s[str(index)]['exe'] = exe
                index+=1
                if index == 10:
                    break
            except:
                pass
        s = json.dumps(s)
        return s