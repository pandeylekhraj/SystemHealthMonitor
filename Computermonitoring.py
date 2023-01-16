import ast
import os
import json
import midas.client
from collections import OrderedDict
#using shell command to get jsonfrom cdms_dqsurf
path='/home/cdms/health_monitoring/Computermonitoring/SystemHealthMonitor/' 
pathsurf='ssh cdms-dqsurf python3 /home/cdms/health_monitoring/HMdqsurf.py $(python3 '+str(path)+'dqsurfthreshold.py) > ./txtfile/dqsurf.txt'
os.system(str(pathsurf))
#Using shell command to get json for gateway computer
pathmidasinstall=str(path)+"FinalComputermonitoringcode.py"
pathgw=str(pathmidasinstall)
os.system('python3 '+str(pathgw)+ ' > ./txtfile/gw.txt')
#Using for loop to create json for other

#print('python3 FormidasInstallServer.py > ./Json/gw.json')
#Using for loop for all other 7 computer
serverlist=["cdms-back","cdms-fe1","cdms-fe2","cdms-fe3","cdms-dq1","cdms-dq2","cdms-dqweb"]
for i in serverlist:
    y="ssh "+i+  " python3  " +str(pathmidasinstall) + " > ./txtfile/" +i.split('-')[-1]+".txt"
    #print(y) 
    os.system(str(y))
client= midas.client.MidasClient("pytest")
path1=str(path)+"txtfile/"
#print(path1)
dirlist=os.listdir(str(path1))
#print(dirlist)
dirs=[i.split('-')[-1]+".txt" for i in serverlist]
#print(dirs)
load_all_data=[]
for dir in dirlist:
    if dir in dirs:
        with open(str(path1)+str(dir),"r") as f:
            data=f.read()
            data=data.split("\n")[1:-1][0]
            data=(str(data))
            data1=ast.literal_eval(data)
            #print(type(data1))
            load_all_data.append(data1)
            f.close()
    else:
        with open(str(path1)+str(dir),"r") as f:
            data=f.read()
            data=data.split("\n")[0]
            data=ast.literal_eval(str(data))
            #print(type(data))
            load_all_data.append(data)
            f.close()
#print(load_all_data[0])
#print(len(load_all_data))
list_keys=list(set(load_all_data[0].keys()))
#print(list_keys)
list_keys.remove('hostname')
#print(list_keys)
for i in range(len(load_all_data)):
    for element in list_keys:
        #print(element)
        content1=OrderedDict(load_all_data[i][str(element)])
        client.odb_set("/HealthMonitoring/ComputerMonitoring/"+str(load_all_data[i]['hostname'])+"/"+str(element),content1)
        #print(content1)
        #print(load_all_data[i]['hostname'])
     
