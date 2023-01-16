#@Writter Lekhraj  email: pandeylekhraj4447@gmail.com
#It helps to provide the information about processor Utilization, Memory Utilization & DiskspaceUtilization

#Calling different libraries like psutil link is here https://psutil.readthedocs.io/en/latest/ 
#used datetime modules to get the time when the code is running. using subprocess modules is not used because this wont in some computer like Centos, etc
# socket help to get the hostname of the computer terminal

import psutil
import numpy as np
import os
import pytz
from datetime import datetime
from pytz import timezone
import midas.client
import socket
from collections import OrderedDict


# midas client helps to connect code with odb page
client = midas.client.MidasClient("pytest")


#for getting time from python modules
tz_Pac = pytz.timezone('US/Pacific')
datetime = datetime.now(tz_Pac)
datetime= datetime.strftime('%a %b %d %H:%M:%S %Z %Y')
#print(datetime)

#get hostname of terminal split will only print its name not full address of computer
hostoutput= socket.gethostname()
hostoutput=hostoutput.split('.')[0]

#connecting code with ODB so that thresholdControl directory can be created by the user. If this code is run for the first time line 38, 39 should be uncommented before running 
# after that user can set values from odb page hence 35 and 36 can be commented after first run 
# DiskPartition testvalue, how many number of diskspace above diskpartition testvalve, how much MeanCPUutilThreshold & MemUtilThreshold are set in this line.


# content=OrderedDict([("ODB_Test_Value", 80),("NumDiskaboveTest_Value", 0),("MeanCPUutilThreshold", 0.5),('MemUtilThreshold', 5)])
# client.odb_set("/HealthMonitoring/ThresholdControl",content)
DiskSpaceThreshold=client.odb_get('/HealthMonitoring/ThresholdControl/NumDiskaboveTest_Value')
MeanProcessorThreshold=client.odb_get('/HealthMonitoring/ThresholdControl/MeanCPUutilThreshold')
MemThreshold=client.odb_get('/HealthMonitoring/ThresholdControl/MemUtilThreshold')
ODB_test = client.odb_get('/HealthMonitoring/ThresholdControl/ODB_Test_Value', recurse_dir=True, include_key_metadata=False)


# Provides information above diskpartion above the threshold value, the test value should be given by User from the THresholdControl directory in HealthMointoring from ODB
# These source code can be found on google

def disk_partition():
    print('\n\n********DISK PARTITION*********\n\n')
    ''' We are using library psutil and trying to get detail of disk partions. We are finding
 total number of partitions, maximum usgae and minimum usage. Also, we keep ODB_test_variable and try
 to get disk partion higher then ODB_test_variable

    '''
    ODB_test_variable =ODB_test
    num_of_partitions = 0
    higher_than_threshold = 0
    max_usage = 0
    min_usage =100
    print('Threshold Percentage Value for Disk =  {} % '.format(str(ODB_test_variable)))
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

    for values in usedpercent:
        #print(df3_df['filesystem'],values)
        values = float(values)
        #print(values)
        #converting string into float
        #check number of disk partition
        num_of_partitions += 1
        
        #helps to find the maximum valve of the available disk partition
        if values > max_usage:
            max_usage =values
            # print(max_usage)
        # helps to find the min values of available disk partition
        if values < min_usage:
            min_usage =values
        
        # important part helps to find how many partions are above the thrshold valves 
        if values > ODB_test_variable:
            higher_than_threshold += 1
    # setting number of threshold value to 0 if it is less than 1
    if higher_than_threshold < 1:
        higher_than_threshold = 0

    print('Number of partitions checked: {}'.format(str(num_of_partitions)))
    print('number of partitions higher than threshold value: {}'.format(str(higher_than_threshold)))
    print('Maximum Utilized partition percentage: {} %'.format(str(max_usage)))
    print('Minimum Utilized partition percentage: {} %'.format(str(min_usage)))

    #setting individual odb keys and its corresponding values using midas client
    content=OrderedDict([("lastRead", datetime),('nmDiskSpaceChk',num_of_partitions), ("MaxDiskSpceChk%", max_usage),
      ("MinDiskSpaceChk%", min_usage),('nmGtrThreshold',higher_than_threshold)])
    client.odb_set("/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization",content)


disk_partition()


# In Processor_utilization, we are using psutil python library: and get all processor utilized array and find max, min amd mean of processor utilization value. 


def Processor_Utilization():
    print('\n\n******processor utilization **************\n\n')
    ''' We are using library psutil and trying to get detail of num of CPU used and their respective
cpu utilization percentage. We are keeping maximum,minumium cpu utilization and number of cpu in webpage
    '''
    
    # gives number of CPU Processor
    num_CPUs = psutil.cpu_count()
    CPUsUtilization_percent1 = psutil.cpu_percent(interval=0.7,percpu=True)
    #CPUsUtilization_percent1 = psutil.cpu_percent(interval= 1, percpu=True)

    #gives array of cpu utilized
    CPUsUtilization_percent=[round(num,5) for num in CPUsUtilization_percent1]
    #print(CPUsUtilization_percent)
     
    #give max, min & Average valves 
    maxValue=max(CPUsUtilization_percent)
    minValue=min(CPUsUtilization_percent)
    MeanValue=round(sum(CPUsUtilization_percent)/len(CPUsUtilization_percent),2)

    print('number of processor =',num_CPUs)
    print('maximum % of processor utilized', maxValue)
    print('minimum % of processor utilized', minValue)
    print('average % of Processor utilized', MeanValue)
    
    # write to see the result on the screen
    for i in range(num_CPUs):
        print("CPU", str(i), "utilization%  =",(CPUsUtilization_percent[i]))
    
    # connect output to the odb page 
    content=OrderedDict([("lastRead", datetime),("nmCPUs", num_CPUs), ('MaxCPUutilized%',maxValue), ("MinCPUutilized%", minValue), ("MeanCPUutilized%", MeanValue)])
    client.odb_set("/HealthMonitoring/"+hostoutput+"/ProcessorUtilization",content)
   

Processor_Utilization()

# THis function helps to retrive information about memory, memoryused%, Swapmemoryused%
def MemoryUtilization():
    print('\n\n********Memory Utilization*********\n\n')
    ''' We are using library psutil and trying to get detail of virtual and swap
 memory using psutil.virtual_memory() and psutil.swap_memory(). We are finding
 ntotal memory in GB by converting bytes into GB and we are finding Memory Utilization
 (total -avialable)*100/total in term of percentage in case both of RAM and Swap
    '''

    # RAM memory
    Memory= psutil.virtual_memory()
    # SWAP memory
    SwapMemory= psutil.swap_memory()
    # total RAM Memory in GB
    MemTot= round(Memory.total/(1024**3),2)
    # total Swap memory in GB
    SwapMemTot= round(SwapMemory.total/(1024**3),2)
    # RAM memory used %
    MemPercent= Memory.percent
    # Swap memory used %
    SwapMemPercent= SwapMemory.percent

    print('Memory Total {} GB'.format(MemTot))
    print('Memory Utilization is {} %'.format(MemPercent))
    print('SwapMemory Total {} GB'.format(SwapMemTot))
    print('SwapMemory Utilization is {} %'.format(SwapMemPercent))
    #print(MemoryUtilization.__doc__)

    # connecting memory information to the odb page
    content=OrderedDict([("lastRead", datetime),('Memoryused%',MemPercent), ("MemTotinGB", MemTot), ("SwapMemoryused%", SwapMemPercent),("SwapMemTotinGB", SwapMemTot)])
    client.odb_set("/HealthMonitoring/"+hostoutput+"/MemoryUtilization",content)


MemoryUtilization()

# Alarming is one of the important aspect of MIDAS. If the threshold value go beyond then it helps to inform to the user in ODB
# Also, it helps to provide information about which threshold value is corssing the limits

def Alarm():
    #Alarm for DiskSpace
    client.create_evaluated_alarm('HMDiskSpacePartition',"/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/nmGtrThreshold > " + str(DiskSpaceThreshold),message='disk partition is filled more than'+str(ODB_test)+'percentage',alarm_class="Alarm", activate_immediately=True)
    #Alarm for ProcessorUtilization taking MeanCPU
    client.create_evaluated_alarm('HMProcessorsUtilization',"/HealthMonitoring/"+hostoutput+"/ProcessorUtilization/MeanCPUutilized% > " + str(MeanProcessorThreshold), message=' average CPU processor is filled more than '+ str(MeanProcessorThreshold)+'percentage',alarm_class="Alarm", activate_immediately=True)
    #client.create_evaluated_alarm('GDProcessorsUtilization',"/HealthMonitoring/"+hostoutput+"/ProcessorUtilization/MeanCPUutilized% > 0.5",message=' average CPU processor is filled more than '+ str(MeanProcessorThreshold)+'percentage',alarm_class="Alarm", activate_immediately=True)
    #Alarm for memomryUtilization
    client.create_evaluated_alarm('HMMemoryUtilization',"/HealthMonitoring/"+hostoutput+"/MemoryUtilization/Memoryused% > "+ str(MemThreshold),message='memory utilization is more than  '+ str(MemThreshold)+'percentage',alarm_class="Alarm", activate_immediately=True)
    
Alarm()
