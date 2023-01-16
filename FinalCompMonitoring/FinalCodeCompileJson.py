# @ Lekhraj  Combined all the JSON files and read and writes the Value to the ODB

# importing all the libraries for doing ssh and running their respectives python scripts to get the data
import ast
import os
import json
import midas.client
#import time
from collections import OrderedDict
import threading
#import os.path
#using shell command to get jsonfrom cdms_dqsurf
#path= os.getcwd()
#print(path)

# absolute path
path='/home/cdms/health_monitoring/Computermonitoring/SystemHealthMonitor/FinalCompMonitoring/'
# ssh for midas-not installed 
pathsurf='ssh cdms-dqsurf python3 /home/cdms/health_monitoring/HMdqsurf.py $(python3 '+str(path)+'/dqsurfthreshold.py) > ' +str(path)+'/Json/cdms-dqsurf.json'
#pathmidas=os.path.join(path,"ReturnJsonFileCompMointor.py")
pathmidas=str(path)+"ReturnJsonFileCompMonitor.py"

#using function call for threading
def dqsurf(pathsurf):
     os.system(str(pathsurf))
    #print("dqsurf",time.time()-t)

def gw(pathmidas):

    pathgw=str(pathmidas)
    os.system('python3 '+str(pathgw))
    #print("gw",time.time()-t)

def fe1(pathmidas):
    os.system('ssh cdms-fe1 python3 '+pathmidas)
    #print("done in fe1 : ",time.time()-t)

def back(pathmidas):
    os.system('ssh cdms-back python3 '+pathmidas)
    #print("done in : fe2 ",time.time()-t)

def fe2(pathmidas):
    os.system('ssh cdms-fe2 python3 '+pathmidas)
    #print("done in : fe2 ",time.time()-t)

def fe3(pathmidas):
    os.system('ssh cdms-fe3 python3 '+pathmidas)
    #print("done in : fe3 ",time.time()-t)

def dq1(pathmidas):
    os.system('ssh cdms-dq1 python3 '+pathmidas)
    #print("done in :dq1 ",time.time()-t)

def dq2(pathmidas):
    os.system('ssh cdms-dq2 python3 '+pathmidas)
    #print("done in :dq2 ",time.time()-t)

def dqweb(pathmidas):
    os.system('ssh cdms-dqweb python3 '+pathmidas)
    #print("done in : dqweb ",time.time()-t)

#t=time.time()
t9=threading.Thread(target=back,args=(pathmidas,))
t1=threading.Thread(target=dqsurf,args=(pathsurf,))
t2=threading.Thread(target=gw,args=(pathmidas,))
t3=threading.Thread(target=fe1,args=(pathmidas,))
t4=threading.Thread(target=fe2,args=(pathmidas,))
t5=threading.Thread(target=fe3,args=(pathmidas,))
t6=threading.Thread(target=dq1,args=(pathmidas,))
t7=threading.Thread(target=dq2,args=(pathmidas,))
t8=threading.Thread(target=dqweb,args=(pathmidas,))
#t9=threading.Thread(target=gw,args=(pathmidas,))

#starting all the threats
t9.start()
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()

#joing all the threads
t9.join()
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
t8.join()

#print("done in : ",time.time()-t)

#communicating python and odb
client= midas.client.MidasClient("pytest")

path1=str(path)+"Json/"
#print(path1)
dirlist=os.listdir(str(path1))
#print(dirlist)
load_all_data=[]
json_dirs = []
#print(json_dirs)
#cheking for Json files
for dir in dirlist:
    #print(dir)
    if '.json' in dir:
        #print('mango',dir)
        json_dirs.append(dir)


#print('JSON listing',json_dirs)
#reading all the json files

for dir in json_dirs:
    with open(str(path1)+str(dir),"r") as f:
      data=f.read()
      if(data):
        data=data.split("\n")[0]
        #print(type(data))
        data=ast.literal_eval(str(data))
        #print(type(data))
        #print(data)
        load_all_data.append(data)
    f.close()

#print(load_all_data[0])
#print(load_all_data)
list_keys=list(set(load_all_data[0].keys()))
#print(list_keys)
list_keys.remove('hostname')
list_keys.remove('Alarm')
#print(list_keys)

for i in range(len(load_all_data)):
    for element in list_keys:
        #print("apple",element)
        content1=OrderedDict(load_all_data[i][str(element)])
        #retain values to ODB
        client.odb_set("/HealthMonitoring/ComputerMonitoring/"+str(load_all_data[i]['hostname'])+"/"+str(element),content1)
        #print(content1)

for i in range(len(load_all_data)):
    alarm=load_all_data[i]['Alarm']
    #print(alarm)

    #client.create_evaluated_alarm('HMDiskSpace'+str(alarm[0]),"/HealthMonitoring/ComputerMonitoring/"+str(alarm[0])+"/DiskSpaceUtilization/nmGtrThreshold > " + str(alarm[2]),message='disk partition is filled more than'+str(alarm[1])+'percentage',alarm_class="Alarm", activate_immediately=True)

    #client.create_evaluated_alarm('HMProceUtil'+str(alarm[0]),"/HealthMonitoring/ComputerMonitoring/"+str(alarm[0])+"/ProcessorUtilization/MeanCPUutilized% > " + str(alarm[3]), message=' average CPU processor is filled more than '+ str(alarm[3])+'percentage',alarm_class="Alarm", activate_immediately=True)
   
    #client.create_evaluated_alarm('HMMemoryUtilization',"/HealthMonitoring/ComputerMonitoring/"+hostoutput+"/MemoryUtilization/Memoryused% > "+ str(MemThreshold),message='memory utilization is more than  '+ str(alarm[4])+'percentage',alarm_class="Alarm", activate_immediately=True)
