import  json,psutil
P = psutil.net_io_counters() # 获取磁盘分区的信息；

disk = {'bytes_sent': P[0], 'bytes_recv': P[1], 'packets_sent': str(P[2]), 'packets_recv': str(P[3]),
        'errin': P[4], 'errout':P[5],'dropin':P[6],'dropout':P[6]}
disk = json.dumps(disk)

print(disk)




str = "this is string example....wow!!! this is really string"
print (str.replace("is", "was"))
print(str.replace("is", "was", 3))