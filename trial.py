# import sys, os, time, threading, subprocess,datetime
#
# diskinfo_raw = subprocess.Popen("df -h", shell=True,stdout=subprocess.PIPE)
# output = diskinfo_raw.communicate()[0]
# print (output.decode())
#
#
# """p1 = subprocess.run("df -h", shell=True, stdout=subprocess.PIPE)
#
# #print(p1.stdout.decode())
#
# p2 = subprocess.run(stdin=subprocess.PIPE.p1.stdout)
#
# print(p2.stdout)
# """

# import sys,os,time,threading,subprocess,datetime
#
# diskinfo_raw = subprocess.Popen("df -h", shell=True, stdout=subprocess.PIPE)
# output = diskinfo_raw.communicate()[0]
# #print (output.decode())
# #print("test")
#
# splitted = output.splitlines()
#
# for x in splitted:
# 	splitbyspace = x.split()
#     #print(splitbyspace)
# 	filesystem = splitbyspace[0].decode("utf-8")
#     #print(filesystem)
#
# 	if filesystem[0] == '/' or filesystem[0] == 't' :
# 		percentage = (splitbyspace[4].decode("utf-8"))
# 		percentagevalue = int(percentage.rstrip("%"))
# 		if percentagevalue > 10:
# 			print(filesystem)

import sys
import os
import time
import threading
import subprocess
import datetime
import json
import requests

URL = "http://dcrc02.triumf.ca:8081/?mjsonrpc"
#GET variable from ODB
def requestODBget(httpODB, ODBpath, ODBvar):
    try:

        header = {"Content-Type":"application/json","Accept":"application/json"}

        #print("\n","http request to get variable from ", ODBvar)
        pload={'jsonrpc':'2.0','id':None,'method':'db_get_values','params':{'paths':[ODBpath+ODBvar]}}
        r=requests.post(httpODB, json=pload, headers=header, timeout=50)
        #print("Reply:")
        #print(r.text)
        ODBr=json.loads(r.text)

        return ODBr["result"]["data"][0]

    except requests.exceptions.ConnectionError:
        print("Midas http connection failed! Establish connetion to Midas ODB")

# print("ODB keys from the folder /Series info:")
# print()
print("\n" + "****************This is Disk Space Info*******************"  + "\n\n")

# ODB_test_variable=POSTrequestODBget("http://dcrc02.triumf.ca:8081/?mjsonrpc", "/Health monitoring/", 'Used Percentage Disk')
#print("Used Percentage Disk = ", ODB_test_variable)

#
#
# ODB_test_variable=requestODBget(URL, "/Health monitoring/", 'Used Percentage Disk')
# print("Threshold Percentage Value for Disk = "+ str(ODB_test_variable) +'%'+'\n')
#
# #To make a command initiate on shell for check disk
# #diskinfo_raw = subprocess.Popen("df -h", shell=True, stdout=subprocess.PIPE)
# diskinfo_raw = subprocess.Popen("df -hT", shell=True, stdout=subprocess.PIPE)
# output = diskinfo_raw.communicate()[0]
# # print (output)
#
# #split the output
# splitted = output.splitlines()
#
# for x in splitted:
# 	splitbyspace = x.split()
# 	# print(splitbyspace)
# 	#making splitted output(bite format) into a string format
# 	filesystem = splitbyspace[0].decode("utf-8")
# 	#selet the filesystem column with first character
# 	#if filesystem[0] == '/' or filesystem[0] == 't' :
# 	if filesystem[0] == '/':
# 		#select 4th column
# 		percentage = (splitbyspace[5].decode("utf-8"))
# 		#print(percentage)
# 		#getrid of "%" sign
# 		percentagevalue = int(percentage.rstrip("%"))
# 		#any filesystems of higher than given percentage will be printed
# 		if percentagevalue > ODB_test_variable:
# 			print(filesystem + "\nused space=" + percentage + "\n")
# 			# print(percentage)
#
#
#

def diskUtillization():
    ODB_test_variable=requestODBget(URL, "/Health monitoring/", 'Used Percentage Disk')
    print("Threshold Percentage Value for Disk = "+ str(ODB_test_variable) +'%'+'\n')

    #To make a command initiate on shell for check disk
    #diskinfo_raw = subprocess.Popen("df -h", shell=True, stdout=subprocess.PIPE)
    diskinfo_raw = subprocess.Popen("df -hT", shell=True, stdout=subprocess.PIPE)
    output = diskinfo_raw.communicate()[0]
    # print (output)

    #split the output
    splitted = output.splitlines()

    for x in splitted:
        # print(x)
    	splitbyspace = x.split()
    	# print(len(splitbyspace))
    	#making splitted output(bite format) into a string format
    	filesystem = splitbyspace[0].decode("utf-8")
    	#selet the filesystem column with first character
    	#if filesystem[0] == '/' or filesystem[0] == 't' :
    	if filesystem[0] == '/':
    		#select 4th column
    		percentage = (splitbyspace[5].decode("utf-8"))
    		#print(percentage)
    		#getrid of "%" sign
    		percentagevalue = int(percentage.rstrip("%"))
    		#any filesystems of higher than given percentage will be printed

    		if percentagevalue > ODB_test_variable:
    			print(filesystem  + " used space=" + percentage )
                # print(x + "\n")
        # num_of_partitions = len(filesystem[0])
        # print(num_of_partitions)
    			# print(percentage)
diskUtillization()
# #to show disk space in kB blocks (K=1024)
# diskinfo_raw = subprocess.Popen("df -T", shell=True, stdout=subprocess.PIPE)
#
# #str_partitions_raw = diskinfo_raw.communicate()[0]
# str_partitions_raw=diskinfo_raw.communicate()[0].decode("utf-8")
#
# #print (str_partitions_raw)
#
# lst_part_split = str_partitions_raw.splitlines()
#
# lst_part_FS = []		#File system
# lst_part_FStype = []	#Type of partition
# lst_part_Size_kB = []	#Partition size in kB
# lst_part_Used_kB = []	#Partition used in kB
# lst_part_Used_percent = []	#Partition used in %
# lst_part_MountedOn = []	#Partition mounted
#
# #var_exclude_tmpfs = 1  #bool to exlude temporary file systems (tmpfs) 0-exclude from the list, 1-include to the list2
# var_exclude_none = 1    #bool to exlude none file systems (tmpfs) 0-exclude from the list, 1-include to the list2
#
# for i in range(1, len(lst_part_split)):
#     #print(lst_part_split[i])
#     lst_part_util = lst_part_split[i].split()
#     #if var_exclude_tmpfs==0:
#     if var_exclude_none==0:
#         lst_part_FS.append(str(lst_part_util[0]))
#         lst_part_FStype.append(str(lst_part_util[1]))
#         lst_part_Size_kB.append(int(lst_part_util[2]))
#         lst_part_Used_kB.append(int(lst_part_util[3]))
#         lst_part_Used_percent.append((lst_part_util[5]))
#         lst_part_MountedOn.append((lst_part_util[6]))
#     else:
#         #if lst_part_util[1]!="tmpfs":
#         if lst_part_util[0]!="none":
#             lst_part_FS.append(str(lst_part_util[0]))
#             lst_part_FStype.append(str(lst_part_util[1]))
#             lst_part_Size_kB.append(int(lst_part_util[2]))
#             lst_part_Used_kB.append(int(lst_part_util[3]))
#             lst_part_Used_percent.append((lst_part_util[5]))
#             lst_part_MountedOn.append((lst_part_util[6]))
#
# print()
# print("Disks partitions:")
# for j in range(len(lst_part_FS)):
#     print(lst_part_FS[j]," ",lst_part_FStype[j], " ", "Size=", str(round((lst_part_Size_kB[j]/1024)/1024))+"GB", "Used=", str(round((lst_part_Used_kB[j]/1024)/1024))+"GB" +"("+lst_part_Used_percent[j]+")", "Mounted on ", lst_part_MountedOn[j])


print("\n" + "****************This is Processors Info*******************"  + "\n\n")

def get_processors_utilization():

    #To make a command initiate on shell
    procinfo_raw = subprocess.Popen("mpstat -P ALL", shell=True, stdout=subprocess.PIPE)

    str_processors_raw=procinfo_raw.communicate()[0].decode("utf-8")
    #print(str_processors_raw)

    lst_proc_split = str_processors_raw.splitlines()

    #print()
    #print(len(lst_proc_split))

    lst_CPU = []        #CPU number
    lst_CPU_util = []   #CPU utilization in %
    lst_CPU_idle = []   #CPU idle in %
    for i in range(3, len(lst_proc_split)):
        #print(lst_proc_split[i])
        lst_proc_util = lst_proc_split[i].split()
        lst_CPU.append(lst_proc_util[2])
        lst_CPU_util.append(round(100-float(lst_proc_util[12]),2))
        lst_CPU_idle.append(float(lst_proc_util[12]))

    # print()
    print("Number of CPU = "+str(len(lst_CPU)-1))
    print("CPU "+lst_CPU[0]+"  average utilization = "+str(lst_CPU_util[0])+"%"+" (idle "+str(lst_CPU_idle[0])+"%)")
    for i in range(1, len(lst_CPU)):
        print("CPU "+lst_CPU[i]+" utilization = "+str(lst_CPU_util[i])+"%"+" (idle "+str(lst_CPU_idle[i])+"%)")

    #returned tuple: CPU number, CPU utilization in %, CPU idle in %
    return(lst_CPU, lst_CPU_util, lst_CPU_idle)
    #return(lst_CPU)

cpuUtilization = get_processors_utilization()

print("\n" + "****************This is Memory Info*******************"  + "\n\n")

# To make a command initiate on shell
meminfo_raw = subprocess.Popen("free -t", shell=True, stdout=subprocess.PIPE)

str_meminfo_raw=meminfo_raw.communicate()[0].decode("utf-8")
# print()
# print("Memory:")
# print(str_meminfo_raw)
# print()

lst_mem_split = str_meminfo_raw.split()
lst_mem = lst_mem_split[7:13]

mem_utilization_raw=(float(lst_mem[1])/float(lst_mem[0]))*100
mem_utilization=round((float(lst_mem[1])/float(lst_mem[0]))*100, 2)

print("Memory utilization = "+str(mem_utilization,)+"%")

def POSTrequestODBpaste(httpODB, ODBpath, ODBvar, ODBval):
    try:
        # httpODB='http://131.225.179.174:8089?mjsonrpc'

        header = {"Content-Type":"application/json","Accept":"application/json"}
        pload={"jsonrpc":"2.0","id":None,"method":"db_paste","params":{"paths":[ODBpath+ODBvar], "values":[ODBval]}}
        r=requests.post(httpODB, json=pload, headers=header, timeout=50)
        # print(r.text)
        ODBr=json.loads(r.text)
        # print(ODBr)
        return ODBr["result"]["status"]


    except requests.exceptions.ConnectionError:
        print("Midas http connection failed! Establish connetion to Midas ODB")

timeinfo_raw = subprocess.Popen("date", shell=True, stdout=subprocess.PIPE)
timeoutput = timeinfo_raw.communicate()[0].decode("utf-8")
# strtimeoutput = timeoutput
print(timeoutput)
# cpuUtilization = get_processors_utilization()
# print(len(cpuUtilization[1])-1)
chkVar=POSTrequestODBpaste(URL, "/Health monitoring/", 'date time', timeoutput)
if chkVar[0]==1:
    print("date time OBD key set successfully")
else:
    print("Error! Check if average CPU utilization ODB key exists in ODB")

#-----set value of average CPU utilization ODB key to ODB on dcrc02----------

chkVar=POSTrequestODBpaste("http://dcrc02.triumf.ca:8081/?mjsonrpc", "/Health monitoring/", 'test Number of CPUs', len(cpuUtilization[1])-1)
if chkVar[0]==1:
    print("average CPU utilization OBD key set successfully")
else:
    print("Error! Check if average CPU utilization ODB key exists in ODB")

chkVar=POSTrequestODBpaste(URL, "/Health monitoring/", 'test CPU average utilization', cpuUtilization[1][0])
if chkVar[0]==1:
    print("average CPU utilization OBD key set successfully")
else:
    print("Error! Check if average CPU utilization ODB key exists in ODB")

chkVar=POSTrequestODBpaste(URL, "/Health monitoring/", 'test CPU max utilization', max(cpuUtilization[1]))
if chkVar[0]==1:
    print("CPU max utilization OBD key set successfully")
else:
    print("Error! Check if CPU max utilization ODB key exists in ODB")

chkVar=POSTrequestODBpaste(URL, "/Health monitoring/", 'test CPU min utilization', min(cpuUtilization[1]))
if chkVar[0]==1:
    print("CPU min utilization OBD key set successfully")
else:
    print("Error! Check if CPU min utilization ODB key exists in ODB")
