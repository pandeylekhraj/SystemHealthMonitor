#@Writter Lekhraj  email: pandeylekhraj4447@gmail.com
# It helps to collect all the json files compile all the information and writes to ODB about processor Utilization, Memory Utilization & Diskspace

#importing some library
import json
import os
import midas.client
from collections import OrderedDict

#connecting client to odb
client = midas.client.MidasClient("pytest", host_name="cdms-back-10g.cdmsdaq.snolab.ca")

#client = midas.client.MidasClient("pytest")
#os.system('pwd')
#os.system ('rm /home/cdms/health_monitoring/lekhraj/all/cdms-dqsurf.json')
#os.system('scp cdms@192.168.28.12:/home/cdms/healthmonitoring/lekhraj/cdms-dqsurf.json /home/cdms/health_monitoring/lekhraj/all')
# helps to copy json from cdms-surf to cdms-back @@like using terminal command
os.system('scp /home/cdms/healthmonitoring/lekhraj/cdms-dqsurf.json /home/cdms/health_monitoring/lekhraj/SystemHealthMonitor/healthDiskProcMem/' )
# print("==",path)
#list out all files inside that directory
dir_list = os.listdir("/home/cdms/health_monitoring/lekhraj/SystemHealthMonitor/healthDiskProcMem/")
#print(dir_list)
json_dirs = []
for dir in dir_list:
    # select those files in the diretory that has .json and append those files in json_list
    if '.json' in dir:
        json_dirs.append(dir)
#print(json_dirs)
load_inf=[]
for dir in json_dirs:
    #print(dir)
    #read all the files and append information on load_inf    
    with open(dir, "r") as f:
        data = json.loads(f.read())
        load_inf.append(data)
        #print("==",data)
        f.close()

#getting all the keysname from json using set dont count keys double 
list_keys=list(set((load.inf[0].keys())))
# removing hostname from list_keys
list_keys.remove('hostname')
for i in range(len(load_inf)):
    for element in list_keys:
        #print(element)
        # keep all the information expect hostname
        content1=OrderedDict(load_inf[i][str(element)])
        #print(content1)
        # help to keep the complete information for a particular hostname
        client.odb_set("/HealthMonitoring/"+str([i]['hostname'])+"/"+str(element),content1)
                                                                         
