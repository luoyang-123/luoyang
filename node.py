
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
        Time = '开机时间'+str(json.dumps(Time))
        return Time


    def Network(self):
        IO={'IO':psutil.net_io_counters()}
        a='总的网络IO信息：'+'<br />'+str(IO)
        return a

    def Magnetic_disk(self):
        P = psutil.disk_partitions()  # 获取磁盘分区的信息；
        p = '磁盘分区信息:'+'<br />'
        for i in range(len(P)):
            disk = {'device=': P[i][0], 'mountpoint=': P[i][1], 'fstype=': P[i][2], 'opts=': P[i][3],
                    'maxfile=': P[i][4], 'maxpath=': P[i][5]}
            disk = json.dumps(disk)
            p += str(disk)+'<br />'
        return p

    def Process(self):
        s=''
        index = 0

        for i in psutil.pids():
            try:
                p = psutil.Process(i)
                exe={"exe":str(p.exe())}
                exe = json.dumps(exe)
                p={'name':str(p.name()),' pid':str(p.pid),' status':str(p.status())}
                p = json.dumps(p)
                print(p)
                s += '进程信息:'+str(p)+'<br />'+'进程文件位置:'+str(exe)+'<br />'+'<br />'
                index+=1
                if index == 10:
                    break
            except:
                pass

        return s