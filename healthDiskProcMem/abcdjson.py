import psutil
import numpy as np
import os
import pytz
from datetime import datetime
from pytz import timezone
# import midas.client
import socket
import json

# client = midas.client.MidasClient("pytest")
#for getting time 
tz_Pac = pytz.timezone('US/Pacific')
datetime = datetime.now(tz_Pac)
datetime= datetime.strftime('%a %b %d %H:%M:%S %Z %Y')
#print(datetime)
#get hostname
hostoutput= socket.gethostname()
hostoutput=hostoutput.split('.')[0]
ODB_test_variable = 90

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


def Processor_Utilization():

    num_CPUs = psutil.cpu_count()
    CPUsUtilization_percent = psutil.cpu_percent(interval=1, percpu=True)
    MeanValue=sum(CPUsUtilization_percent)/len(CPUsUtilization_percent)
    #print(CPUsUtilization_percent)
    # print('number of processor =',num_CPUs)
    # print('maximum % of processor utilized', max(CPUsUtilization_percent))
    # print('minimum % of processor utilized', min(CPUsUtilization_percent))
    # print('average % of Processor utilized', MeanValue)
    # for i in range(num_CPUs):
    #     print("CPU", str(i), "utilization%  =",(CPUsUtilization_percent[i]))
   
    return[num_CPUs,CPUsUtilization_percent,MeanValue]



def MemoryUtilization():
    
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

    

print('\n\n********DISK PARTITION*********\n\n')
print('Threshold Percentage Value for Disk =  {} % '.format(str(ODB_test_variable)))
print('Number of partitions checked: {}'.format(str(disk_partition()[0])))
print('number of partitions higher than threshold value: {}'.format(disk_partition()[3]))
print('Maximum Utilized partition percentage: {} %'.format(str(disk_partition()[1])))
print('Minimum Utilized partition percentage: {} %'.format(str(disk_partition()[2])))

print('\n\n******processor utilization **************\n\n')
#return [num_CPUs,max(CPUsUtilization_percent),min(CPUsUtilization_percent),MeanValue]
#print(Processor_Utilization()[1])
# for i in range(Processor_Utilization()[0]):
# print("CPU", str(i),"utilization%  =") #,(Processor_Utilization()[1][i])
print('number of processor =',Processor_Utilization()[0])
print('maximum % of processor utilized', max(Processor_Utilization()[1]))
print('minimum % of processor utilized', min(Processor_Utilization()[1]))
print('average % of Processor utilized', Processor_Utilization()[2])
# return [MemTot, SwapMemTot, MemPercent, SwapMemPercent]
#print(MemoryUtilization())
print('\n\n********Memory Utilization*********\n\n')
print('Memory Total {} GB'.format(MemoryUtilization()[0]))
print('Memory Utilization in {}%'.format(MemoryUtilization()[2]))
print('Memory  SWAP Total {} GB'.format(MemoryUtilization()[1]))
print('Memory Swap Utilization in {}%'.format(MemoryUtilization()[3]))

json12={"hostname":hostoutput,"DiskSpaceUtilization":{'lastRead':datetime ,'nmDiskSpaceChk':disk_partition()[0],'MaxDiskSpceChk%':disk_partition()[1],'MinDiskSpaceChk%':disk_partition()[2],'nmGtrThreshold': disk_partition()[3]},"ProcessorUtilization":{'lastRead':datetime ,'nmCPUs': Processor_Utilization()[0],'MaxCPUutilized%':max(Processor_Utilization()[1]),'MinCPUutilized%':min(Processor_Utilization()[1]) ,'MeanCPUutilized%':Processor_Utilization()[2]},"MemoryUtilization":{'lastRead':datetime,'Memoryused%':MemoryUtilization()[2],'MemTotinGB':MemoryUtilization()[0],'SwapMemoryused%':MemoryUtilization()[3] ,'SwapMemTotinGB':MemoryUtilization()[2]}}


out_file = open("/home/cdms/health_monitoring/lekhraj/SystemHealthMonitor/healthDiskProcMem/"+ str(hostoutput) +".json", "w")
json.dump(json12, out_file)

out_file.close()

