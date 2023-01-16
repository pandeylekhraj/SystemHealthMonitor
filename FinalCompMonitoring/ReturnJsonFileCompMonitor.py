# written by Lekhraj(USD) pandeylekhraj4447@gmail.com
#importing libraries main library is psutil midas.client communicates with odb page 

import psutil
import numpy as np
import os
import pytz
from datetime import datetime
from pytz import timezone
import midas.client
import socket
import json
import os.path

#connecting my script to odb
client = midas.client.MidasClient("pytest")

#for getting time 
tz_Pac = pytz.timezone('US/Pacific')
datetime = datetime.now(tz_Pac)
datetime= datetime.strftime('%a %b %d %H:%M:%S %Z %Y')
#print(datetime)
#get hostname
hostoutput= socket.gethostname()
hostoutput=hostoutput.split('.')[0]
#path inside midas client is path in the odb where the threshold comparable values comes from odb page
ODBTest=client.odb_get("/HealthMonitoring/ComputerMonitoring/ThresholdControl/"+hostoutput+"/ODB_Test_Value")
ODB_test_variable=int(ODBTest)
DiskSpaceThreshold=client.odb_get('/HealthMonitoring/ComputerMonitoring/ThresholdControl/'+hostoutput+'/NumDiskaboveTest_Value')
MeanProcessorThreshold=client.odb_get('/HealthMonitoring/ComputerMonitoring/ThresholdControl/'+hostoutput+'/MeanCPUutilThreshold')
MemThreshold=client.odb_get('/HealthMonitoring/ComputerMonitoring/ThresholdControl/'+hostoutput+'/MemUtilThreshold')



def disk_partition():

    ''' We are using library psutil and trying to get detail of disk partions. We are finding
 total number of partitions, maximum usgae and minimum usage. Also, we keep ODB_test_variable and try
 to get disk partion higher then ODB_test_variable

    '''
    
    num_of_partitions = 0
    higher_than_threshold = 0
    max_usage = 0
    min_usage =100
    #print('Threshold Percentage Value for Disk =  {} % '.format(str(ODB_test_variable)))
    #templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
    #print(templ % ("Device", "Total", "Used", "Free", "Use ", "Type",
    #              "Mount"))
    templ="%-17s %5s%%"
    filesystem=[]
    usedpercent=[]
    for part in psutil.disk_partitions(all=False):
        #print(os.name)
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                # skip cd-rom drives with no disk in it; they may raise
                # ENOENT, pop-up a Windows GUI error for a non-ready
                # partition or just hang.
                continue
        usage = psutil.disk_usage(part.mountpoint)
        templ % (
            filesystem.append(part.device),
            usedpercent.append(usage.percent))

    # FreeListPer= list(map(lambda x: round(100 - x,2), usedpercent))
    # print(filesystem)
    # print(usedpercent)
    # print(FreeListPer)
    for values in usedpercent:
        #print(df3_df['filesystem'],values)
        values = float(values)
        #print(values)
        #converting string into float
        num_of_partitions += 1
        if values > max_usage:
            max_usage =values
            # print(max_usage)
        if values < min_usage:
            min_usage =values
            # print(min_usage)
        if values > ODB_test_variable:
            higher_than_threshold += 1
    if higher_than_threshold < 1:
        higher_than_threshold = 0
    return [num_of_partitions, max_usage, min_usage, higher_than_threshold]

 
def Processor_Utilization():

    ''' We are using library psutil and trying to get detail of num of CPU used and their respective
cpu utilization percentage. We are keeping maximum,minumium cpu utilization and number of cpu in webpage
    '''

    num_CPUs = psutil.cpu_count()
    CPUsUtilization_percent = psutil.cpu_percent(interval=1,percpu=True)
    MeanValue=sum(CPUsUtilization_percent)/len(CPUsUtilization_percent)
    MeanValue=round(MeanValue,3)
    return[num_CPUs,CPUsUtilization_percent,MeanValue]   


def MemoryUtilization():
   # print('\n\n********Memory Utilization*********\n\n')
    ''' We are using library psutil and trying to get detail of virtual and swap
 memory using psutil.virtual_memory() and psutil.swap_memory(). We are finding
 ntotal memory in GB by converting bytes into GB and we are finding Memory Utilization
 (total -avialable)*100/total in term of percentage in case both of RAM and Swap 
    '''

    Memory= psutil.virtual_memory()
    SwapMemory= psutil.swap_memory()
    MemTot= round(Memory.total/(1024**3),2)
    SwapMemTot= round(SwapMemory.total/(1024**3),2)
    MemPercent= Memory.percent
    SwapMemPercent= SwapMemory.percent
    return [MemTot, SwapMemTot, MemPercent, SwapMemPercent]

# values from processor utilization, disk Space Utilization & memoryutilization 

Processor_=Processor_Utilization()
disk_=disk_partition()
Memory_=MemoryUtilization()

json1={'hostname':hostoutput,'DiskSpaceUtilization':{'LastRead':datetime,'nmDiskSpaceChk':disk_[0],'MaxDiskSpaceChk%':disk_[1],'MinDiskSpaceChk%':disk_[2],'nmGtrThreshold':disk_[3]},'ProcessorUtilization':{'LastRead':datetime,'nmCPUs':Processor_[0],'MaxCPUutilized%':max(Processor_[1]),'MinCPUutilized%':min(Processor_[1]),'MeanCPUutilized%':Processor_[2]},'MemoryUtilization':{'LastRead':datetime,'MemoryUsed%':Memory_[1],'MemTotinGB':Memory_[0],'SwapMemoryused%':Memory_[3],'SwapMemTotinGB':Memory_[2]},'Alarm':[hostoutput,ODB_test_variable,DiskSpaceThreshold,MeanProcessorThreshold,MemThreshold,disk_[3],Processor_[2],Memory_[1]]}
#print(json1)
#Pathwhere the code is running
#PathJson= os.path.join(os.getcwd())
#print(PathJson)
PathJson="/home/cdms/health_monitoring/Computermonitoring/SystemHealthMonitor/FinalCompMonitoring"
out_file = open(str(PathJson)+"/Json/"+ str(hostoutput) +".json", "w")
json.dump(json1, out_file)

out_file.close()

