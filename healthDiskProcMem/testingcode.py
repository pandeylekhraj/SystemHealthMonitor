#testing without client
import json
import os
#import midas.client
from collections import OrderedDict
#client = midas.client.MidasClient("pytest")
#os.system('pwd')
#os.system ('rm /home/cdms/health_monitoring/lekhraj/all/cdms-dqsurf.json')
#os.system('scp cdms@192.168.28.12:/home/cdms/healthmonitoring/lekhraj/cdms-dqsurf.json /home/cdms/health_monitoring/lekhraj/all')
#os.system('scp /home/cdms/healthmonitoring/lekhraj/cdms-dqsurf.json /home/cdms/health_monitoring/lekhraj/SystemHealthMonitor/healthDiskProcMem/' )
# print("==",path)
dir_list = os.listdir("/home/cdms/health_monitoring/lekhraj/SystemHealthMonitor/healthDiskProcMem/")
#print(dir_list)
json_dirs = []
for dir in dir_list:
    if '.json' in dir:
        json_dirs.append(dir)
#print(json_dirs)
x=[]
for dir in json_dirs:
    #print(dir)    
    with open(dir, "r") as f:
        data = json.loads(f.read())
        x.append(data)
        #print("==",data)
        f.close()
#print(x)
y=list(set((x[0].keys())))
y.remove('hostname')
for i in range(len(x)):
    for element in y:
        #print(element)
        content1=OrderedDict(x[i][str(element)])
        #print(content1)
        print( "/HealthMonitoring/"+str(x[i]['hostname'])+"/"+str(element),content1)
