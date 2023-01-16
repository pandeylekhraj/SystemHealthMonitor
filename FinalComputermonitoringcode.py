# written by Lekhraj(USD) 
#importing libraries 
import psutil
import numpy as np
import os
import pytz
from datetime import datetime
from pytz import timezone
import midas.client
import socket

#connecting 
client = midas.client.MidasClient("pytest")
#for getting time 
tz_Pac = pytz.timezone('US/Pacific')
datetime = datetime.now(tz_Pac)
datetime= datetime.strftime('%a %b %d %H:%M:%S %Z %Y')
#print(datetime)
#get hostname
hostoutput= socket.gethostname()
hostoutput=hostoutput.split('.')[0]
ODBTest=client.odb_get("/HealthMonitoring/ComputerMonitoring/ThresholdControl/"+hostoutput+"/ODB_Test_Value")
ODB_test_variable=int(ODBTest)

def disk_partition():
    
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
   # print('Number of partitions checked: {}'.format(str(num_of_partitions)))
   # print('number of partitions higher than threshold value: {}'.format(str(higher_than_threshold)))
   # print('Maximum Utilized partition percentage: {} %'.format(str(max_usage)))
   # print('Minimum Utilized partition percentage: {} %'.format(str(min_usage)))

    #setting individual odb keys and its corresponding values using midas client

    # client.odb_set("/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/lastRead",datetime)
    # client.odb_set("/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/MaxDiskSpceChk%",max_usage)
    # client.odb_set("/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/MinDiskSpaceChk%",min_usage)
    # client.odb_set("/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/nmDiskSpaceChk",num_of_partitions)
    # client.odb_set("/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/nmGtrThreshold",higher_than_threshold)



def Processor_Utilization():

    num_CPUs = psutil.cpu_count()
    CPUsUtilization_percent = psutil.cpu_percent(interval=1,percpu=True)
    MeanValue=sum(CPUsUtilization_percent)/len(CPUsUtilization_percent)
    
    return[num_CPUs,CPUsUtilization_percent,MeanValue]
    #print(CPUsUtilization_percent)
    #print('number of processor =',num_CPUs)
    #print('maximum % of processor utilized', max(CPUsUtilization_percent))
    #print('minimum % of processor utilized', min(CPUsUtilization_percent))
    #print('average % of Processor utilized', MeanValue)
   # for i in range(num_CPUs):
       # print("CPU", str(i), "utilization%  =",(CPUsUtilization_percent[i]))
        
    # client.odb_set("/HealthMonitoring/"+hostoutput+"/ProcessorUtilization/lastRead",datetime)
    # client.odb_set("/HealthMonitoring/"+hostoutput+"/ProcessorUtilization/MaxCPUutilized%",max(CPUsUtilization_percent))
    # client.odb_set("/HealthMonitoring/"+hostoutput+"/ProcessorUtilization/MinCPUutilized%",min(CPUsUtilization_percent))
    # client.odb_set("/HealthMonitoring/"+hostoutput+"/ProcessorUtilization/nmCPUs",num_CPUs)
   


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
    #print('Memory Total {} GB'.format(MemTot))
    #print('Memory Utilization in {}%'.format(MemPercent))
    #print('Memory Total {} GB'.format(SwapMemTot))
    #print('Memory Utilization in {}%'.format(SwapMemPercent))
    #print(MemoryUtilization.__doc__)

    # client.odb_set("/HealthMonitoring/"+hostoutput+"/MemoryUtilization/lastRead",datetime)
    # client.odb_set("/HealthMonitoring/"+hostoutput+"/MemoryUtilization/Memoryused%",MemPercent)
    # client.odb_set("/HealthMonitoring/"+hostoutput+"/MemoryUtilization/SwapMemoryused%",SwapMemTot)
    # client.odb_set("/HealthMonitoring/"+hostoutput+"/MemoryUtilization/MemTotinGB",MemTot)
    # client.odb_set("/HealthMonitoring/"+hostoutput+"/MemoryUtilization/SwapMemTotinGB",SwapMemTot)
json1={'hostname':hostoutput,'DiskSpaceUtilization':{'LastRead':datetime,'nmDiskSpaceChk':disk_partition()[0],'MaxDiskSpaceChk%':disk_partition()[1],'MinDiskSpaceChk%':disk_partition()[2],'nmGtrThreshold':disk_partition()[3]},'ProcessorUtilization':{'LastRead':datetime,'nmCPUs':Processor_Utilization()[0],'MaxCPUutilized%':max(Processor_Utilization()[1]),'MinCPUutilized%':min(Processor_Utilization()[1]),'MeanCPUutilized%':Processor_Utilization()[2]},'MemoryUtilization':{'LastRead':datetime,'MemoryUsed%':MemoryUtilization()[1],'MemTotinGB':MemoryUtilization()[0],'SwapMemoryused%':MemoryUtilization()[3],'SwapMemTotinGB':MemoryUtilization()[2]}}
print(json1)
