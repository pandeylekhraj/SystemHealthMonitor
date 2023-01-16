# import sys
# import os
# import time
# import threading
# import subprocess
# import datetime
# import json
# import requests
# import array
#
# URL = "http://dcrc02.triumf.ca:8081/?mjsonrpc"
#
# # def POSTrequestODBcreate(httpODB, ODBpath, ODBvar)
# # def POSTrequestODBcreate(httpODB, ODBpath, ODBvar):
# def POSTrequestODBcreateString(httpODB, ODBpath, ODBvar):
#     try:
#         # httpODB='http://131.225.179.174:8089?mjsonrpc'
#
#         header = {"Content-Type":"application/json","Accept":"application/json"}
#         # pload={"jsonrpc":"2.0","id":None,"method":"db_create_key","params":{"paths":[ODBpath],"type":8,"values":[ODBvar]}}
#         # pload={"jsonrpc":"2.0","id":None,"method":"db_create","params":{"paths":[ODBpath],"type":8}}
#         # pload={"jsonrpc":"2.0","id":None,"method":"db_create","params":{"paths":"/Health monitoring/amila"}}
#         # pload={'jsonrpc':'2.0','id':None,'method':'db_create','params':[{'path':ODBpath+ODBvar, 'type':7 }]}
#         # pload={'jsonrpc':'2.0','id':None,'method':'db_create','params':[{'path':ODBpath+ODBvar, 'type':7, "values":ODBvar}]}
#         pload={'jsonrpc':'2.0','id':None,'method':'db_create','params':[{'path':ODBpath+ODBvar, 'type':12, 'string_length':32}]}
#
#         r=requests.post(httpODB, json=pload, headers=header, timeout=50)
#         # print(r.text)
#         ODBr=json.loads(r.text)
#         print(ODBr)
#         # return ODBr["result"]["status"]
#         return(ODBr)
#
#
#     except requests.exceptions.ConnectionError:
#         print("Midas http connection failed! Establish connetion to Midas ODB")

import sys
import os
import time
import threading
import subprocess
import datetime
import json
import requests
import re

# URL for ODB on dcrc02.triumf.ca
URL = "http://dcrc02.triumf.ca:8081/?mjsonrpc"

# ------------ dublicate the ODB key value from ODB on dcrc02.triumf.ca via HTTP REQUEST -------------
def dublicateODBkeyvalue(httpODB, ODBpath, ODBvar):
    try:

        header = {"Content-Type":"application/json","Accept":"application/json"}

        pload={'jsonrpc':'2.0','id':None,'method':'db_get_values','params':{'paths':[ODBpath+ODBvar]}}
        r=requests.post(httpODB, json=pload, headers=header, timeout=50)
        ODBr=json.loads(r.text)

        return ODBr["result"]["data"][0]

    except requests.exceptions.ConnectionError:
        print("Midas http connection failed! Establish connetion to Midas ODB")

# ------------set the ODB key value to ODB on dcrc02.triumf.ca via HTTP REQUEST -------------
def setODBkeyvalue(httpODB, ODBpath, ODBvar, ODBval):
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

# ------------Creat a the string ODB key and value to ODB on dcrc02.triumf.ca via HTTP REQUEST -------------
def CreateODBkeyString(httpODB, ODBpath, ODBvar):
    try:
        # httpODB='http://131.225.179.174:8089?mjsonrpc'

        header = {"Content-Type":"application/json","Accept":"application/json"}
        pload={'jsonrpc':'2.0','id':None,'method':'db_create','params':[{'path':ODBpath+ODBvar, 'type':12, 'string_length':64}]}

        r=requests.post(httpODB, json=pload, headers=header, timeout=50)
        # print(r.text)
        ODBr=json.loads(r.text)
        # print(ODBr)

        return ODBr["result"]["status"]


    except requests.exceptions.ConnectionError:
        print("Midas http connection failed! Establish connetion to Midas ODB")

def DeleteODBkey(httpODB, ODBpath):
    try:
        # httpODB='http://131.225.179.174:8089?mjsonrpc'

        header = {"Content-Type":"application/json","Accept":"application/json"}
        pload={"jsonrpc":"2.0","id":None,"method":"db_delete","params":{"paths":[ODBpath]}}
        r=requests.post(httpODB, json=pload, headers=header, timeout=50)
        # print(r.text)
        ODBr=json.loads(r.text)
        # print(ODBr)
        return ODBr["result"]["status"]


    except requests.exceptions.ConnectionError:
        print("Midas http connection failed! Establish connetion to Midas ODB")

#Create subdirectory in ODB
def CreateODBSubDir(httpODB, ODBpath):
    try:
        #httpODB='http://131.225.179.174:8089?mjsonrpc'

        header = {"Content-Type":"application/json","Accept":"application/json"}

        #type 15 is subdirectory
        pload={'jsonrpc':'2.0','id':None,'method':'db_create','params':[{'path':ODBpath, 'type':15}]}

        r=requests.post(httpODB, json=pload, headers=header, timeout=50)
        #print("Reply:")
        #print(r.text)
        ODBr=json.loads(r.text)

        #return ODBr["result"]["data"][0]
        return ODBr

    except requests.exceptions.ConnectionError:
        print("Midas http connection failed! Establish connection to Midas ODB")
        # return(-9876543210)
#get the date and time cheked the server

def RaiseAlarm(Subfol,Key,KeyValue):

    ODB_RS=CreateODBSubDir(URL, "/Alarms/Alarms/"+hostoutput+ " " + Subfol)
    print "result of CreateODBSubDir" +" "+ hostoutput + " " + Subfol + " =", ODB_RS

    rep = 2
    for x in range(rep):
        ODB_val=setODBkeyvalue(URL, "/Alarms/Alarms/"+hostoutput+ " " + Subfol +"/" , Key, KeyValue)
        # print "result of setODBkeyvalue Active = ", ODB_val_1

    print "result of setODBkeyvalue Active = ", ODB_val

def CreateODBkeyInt(httpODB, ODBpath, ODBvar):
    try:
        # httpODB='http://131.225.179.174:8089?mjsonrpc'

        header = {"Content-Type":"application/json","Accept":"application/json"}
        # pload={'jsonrpc':'2.0','id':None,'method':'db_create','params':[{'path':ODBpath+ODBvar, 'type':9, 'string_length':64}]}
        pload={'jsonrpc':'2.0','id':None,'method':'db_create','params':[{'path':ODBpath+ODBvar, 'type':7}]}

        r=requests.post(httpODB, json=pload, headers=header, timeout=50)
        # print(r.text)
        ODBr=json.loads(r.text)
        # print(ODBr)

        return ODBr["result"]["status"]


    except requests.exceptions.ConnectionError:
        print("Midas http connection failed! Establish connetion to Midas ODB")




timeinfo_raw = subprocess.Popen("date", shell=True, stdout=subprocess.PIPE)
timeoutput = timeinfo_raw.communicate()[0].decode("utf-8")
# print("\n"+"Last Read:"+ timeoutput +"\n")

#get the hostnaame of the server
# hostinfo_raw = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE)
# # str_hostinfo_raw=hostinfo_raw.communicate()[0].decode("utf-8")
# str_hostinfo_raw=hostinfo_raw.communicate()[0]
# host_split = str_hostinfo_raw.split(".")
# # print(host_split[0])
# type(host_split[0].decode("utf-8"))
# print(len(host_split))
# hostoutput = hostinfo_raw.communicate()[0].decode("utf-8")
# print("\n"+"Host Name:"+ hostoutput +"\n")


hostinfo_raw = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE)
str_hostinfo_raw=hostinfo_raw.communicate()[0].decode("utf-8")
host_split = str_hostinfo_raw.split(".")
hostoutput=host_split[0]
# print (hostoutput)


# ///////////////////////////////////////////////////////////////////////////
#
#
#
#
#
#
# alrm_gen = subprocess.Popen("echo $1 | mail -s \'Level Alarm\' ruslan.podviianiuk@usd.edu <<< 'TEST ALARM'", shell=True, stdout=subprocess.PIPE)





# ///////////////////////////////////////////////////////////////////////////////////////////
# def disk_Utilization():
#     # ODB_test_variable=dublicateODBkeyvalue(URL, "/Health monitoring/Disk Space Utilization/", 'Threshold value for Partitions')
#     # print(ODB_test_variable)
#     ODB_test_variable = 90
#     print("Threshold Percentage Value for Disk = "+ str(ODB_test_variable) +'%'+'\n')
#     print("Partitions with Utilization")
#
#     # max_value = df["splitbyspace[5]"].max()
#
#     # To make a command initiate on shell for check disk
#     # diskinfo_raw = subprocess.Popen("df -h", shell=True, stdout=subprocess.PIPE)
#     diskinfo_raw = subprocess.Popen("df -hT", shell=True, stdout=subprocess.PIPE)
#     output = diskinfo_raw.communicate()[0]
#
#     # split the output
#     splitted = output.splitlines()
#
#     num_of_partitions = 0
#     higher_than_threshold = 0
#     max_usage = 0
#     min_usage =100
#
#     for x in splitted:
#         # num_of_partitions += 1
#         splitbyspace = x.split()
#     	# making splitted output(bite format) into a string format
#         filesystem = splitbyspace[0].decode("utf-8")
#     	# selet the filesystem column with first character
#     	# if filesystem[0] == '/' or filesystem[0] == 't' :
#     	# if filesystem == "/dev/sda7":
#         if re.search('/dev/sd.+',filesystem):
#             num_of_partitions += 1
#     		# select 4th column
#             # percentageval = splitbyspace[5]
#             # max_percentagevalue = max(percentageval)
#             percentage = (splitbyspace[5].decode("utf-8"))
#     		# getrid of "%" sign
#             percentage_value = int(percentage.rstrip("%"))
#             print(filesystem  + " used space=" + percentage )
#             # list_of_percentage_value = list(percentage_value)
#             # print(list_of_percentage_value)
#             if percentage_value > max_usage:
#                 max_usage =percentage_value
#             # print(max_usage)
#
#             if percentage_value < min_usage:
#                 min_usage = percentage_value
#             # print(min_usage)
#             if percentage_value > ODB_test_variable:
#                 higher_than_threshold += 1
#                 # print(filesystem  + " used space=" + percentage )
#             #     # percentagevalue = new_percentagevalue
#             #
#             #     print(filesystem  + " used space=" + percentage )
#
#     print("\n" +"Number of partitions checked: " +str(num_of_partitions))
#     print("\n"+ "number of partitions higher than threshold value: "+ str(higher_than_threshold))
#     print("\n" +"Maximum Utilized partition: " +str(max_usage))
#     print("\n" +"Minimum Utilized partition: " +str(min_usage) +"\n"+"\n")
#
#
#     print "\nDisk Space Utilization ODB keys\n"
#     ODB_var_1=CreateODBkeyString(URL, "/Health monitoring/Disk Space Utilization/", hostoutput + " " + 'lastRead')
#     ODB_val_1=setODBkeyvalue(URL, '/Health monitoring/Disk Space Utilization/', hostoutput + " " + 'lastRead',timeoutput)
#     print "rusult of CreateODBkeyString" + " " +  hostoutput + " " + 'lastRead' " =", ODB_var_1
#     print "rusult of setODBkeyvalue of " + " " +  hostoutput + " " + 'lastRead' " =", ODB_val_1
#     # print(ODB_val_1)
#     # if ODB_val_1[0]==1:
#     #     print( hostoutput+'lastRead' + " " + "OBD key set successfully to Disk Space Utilization")
#     # else:
#     #     print("Error!" + hostoutput + " " + 'lastRead'+ " cannot be created!... check the lenth of name the key")
#
#     # ODB_var_1=CreateODBkeyString(URL, "/Health monitoring/Disk Space Utilization/", hostoutput + " " + 'maxDiskSpaceChecked')
#     ODB_var_1=CreateODBkeyInt(URL, "/Health monitoring/Disk Space Utilization/", hostoutput + " " + 'maxDiskSpaceChecked' + ' %')
#     # ODB_val_1=setODBkeyvalue(URL, '/Health monitoring/Disk Space Utilization/', hostoutput + " " + 'maxDiskSpaceChecked',str(max_usage)+"%")
#     ODB_val_1=setODBkeyvalue(URL, '/Health monitoring/Disk Space Utilization/', hostoutput + " " + 'maxDiskSpaceChecked' + ' %',max_usage )
#     print "rusult of CreateODBkeyString" + " " +  hostoutput + " " + 'maxDiskSpaceChecked' " =", ODB_var_1
#     print "rusult of setODBkeyvalue of " + " " +  hostoutput + " " + 'maxDiskSpaceChecked' " =", ODB_val_1
#     # print(ODB_val_1)
#     # if ODB_val_1[0]==1:
#     #     print( hostoutput + " " + 'maxDiskSpaceChecked' + " " + "OBD key set successfully to Disk Space Utilization")
#     # else:
#     #     print("Error!" + hostoutput + " " + 'maxDiskSpaceChecked'+ " cannot be created!... check the lenth of name the key")
#
#     # ODB_var_1=CreateODBkeyString(URL, "/Health monitoring/Disk Space Utilization/", hostoutput + " " + 'minDiskSpaceChecked')
#     ODB_var_1=CreateODBkeyInt(URL, "/Health monitoring/Disk Space Utilization/", hostoutput + " " + 'minDiskSpaceChecked' + ' %')
#     # ODB_val_1=setODBkeyvalue(URL, '/Health monitoring/Disk Space Utilization/', hostoutput + " " + 'minDiskSpaceChecked',str(min_usage)+"%")
#     ODB_val_1=setODBkeyvalue(URL, '/Health monitoring/Disk Space Utilization/', hostoutput + " " + 'minDiskSpaceChecked' + ' %',min_usage )
#     print "rusult of CreateODBkeyString" + " " +  hostoutput + " " + 'minDiskSpaceChecked' " =", ODB_var_1
#     print "rusult of setODBkeyvalue of " + " " +  hostoutput + " " + 'minDiskSpaceChecked' " =", ODB_val_1
#     # print(ODB_val_1)
#     # if ODB_val_1[0]==1:
#     #     print( hostoutput + " " + 'minDiskSpaceChecked' + " " + "OBD key set successfully to Disk Space Utilization")
#     # else:
#     #     print("Error!" + hostoutput + " " + 'minDiskSpaceChecked'+ " cannot be created!... check the lenth of name the key")
#
#     # ODB_var_1=CreateODBkeyString(URL, "/Health monitoring/Disk Space Utilization/", hostoutput + " " + 'numDiskSpaceChecked')
#     ODB_var_1=CreateODBkeyInt(URL, "/Health monitoring/Disk Space Utilization/", hostoutput + " " + 'numDiskSpaceChecked')
#     # ODB_val_1=setODBkeyvalue(URL, '/Health monitoring/Disk Space Utilization/', hostoutput + " " + 'numDiskSpaceChecked',str(num_of_partitions))
#     ODB_val_1=setODBkeyvalue(URL, '/Health monitoring/Disk Space Utilization/', hostoutput + " " + 'numDiskSpaceChecked',num_of_partitions )
#     # print type(num_of_partitions)
#     # print num_of_partitions
#     print "rusult of CreateODBkeyString" + " " +  hostoutput + " " + 'numDiskSpaceChecked' " =", ODB_var_1
#     print "rusult of setODBkeyvalue of " + " " +  hostoutput + " " + 'numDiskSpaceChecked' " =", ODB_val_1
#     # print(ODB_val_1)
#     # if ODB_val_1[0]==1:
#     #     print( hostoutput + " " + 'numDiskSpaceChecked' + " " + "OBD key set successfully to Disk Space Utilization")
#     # else:
#     #     print("Error!" + hostoutput + " " + 'numDiskSpaceChecked'+ " cannot be created!... check the lenth of name the key")
#
#     # ODB_var_1=CreateODBkeyString(URL, "/Health monitoring/Disk Space Utilization/", hostoutput + " " + 'numDSCheckedThanThr')
#     ODB_var_1=CreateODBkeyInt(URL, "/Health monitoring/Disk Space Utilization/", hostoutput + " " + 'numDSCheckedThanThr')
#     # ODB_val_1=setODBkeyvalue(URL, '/Health monitoring/Disk Space Utilization/', hostoutput + " " + 'numDSCheckedThanThr',str(higher_than_threshold))
#     ODB_val_1=setODBkeyvalue(URL, '/Health monitoring/Disk Space Utilization/', hostoutput + " " + 'numDiskSpaceChecked',higher_than_threshold )
#     # print type(higher_than_threshold)
#     # print higher_than_threshold
#     print "rusult of CreateODBkeyString" + " " +  hostoutput + " " + 'numDSCheckedThanThr' " =", ODB_var_1
#     print "rusult of setODBkeyvalue of " + " " +  hostoutput + " " + 'numDSCheckedThanThr' " =", ODB_val_1
#
#
# disk_Utilization()
#
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# ODB_var_1=CreateODBkeyInt(URL, "/Health monitoring/Disk Space Utilization/", hostoutput + " " + 'int')
# ODB_val_1=setODBkeyvalue(URL, '/Health monitoring/Disk Space Utilization/', hostoutput + " " + 'int',10)
# print "rusult of CreateODBkeyString" + " " +  hostoutput + " " + 'minDiskSpaceChecked' " =", ODB_var_1
# print "rusult of setODBkeyvalue of " + " " +  hostoutput + " " + 'minDiskSpaceChecked' " =", ODB_val_1

ODB_val_1=setODBkeyvalue(URL, '/Health monitoring/Disk Space Utilization/', hostoutput + " " + 'numDiskSpaceChecked', 0.2 )
print "rusult of setODBkeyvalue of " + " " +  hostoutput + " " + 'numDiskSpaceChecked' " =", ODB_val_1
# ODB_test_variable=dublicateODBkeyvalue(URL, "/Health monitoring/Disk Space Utilization/", 'numDSCheckedThanThr')
# print(ODB_test_variable)



# RaiseAlarm('test3','Active',0)
#
# print("\n" + "****************This is Processors Utilization Info*******************"  + "\n\n")
#
# def processors_Utilization():
#
#     # To make a command initiate on shell
#     procinfo_raw = subprocess.Popen("mpstat -P ALL", shell=True, stdout=subprocess.PIPE)
#     # convert bite format into a string format
#     str_processors_raw=procinfo_raw.communicate()[0].decode("utf-8")
#
#     lst_proc_split = str_processors_raw.splitlines()
#
#
#     lst_CPU = []        #CPU number
#     lst_CPU_util = []   #CPU utilization in %
#     lst_CPU_idle = []   #CPU idle in %
#     for i in range(3, len(lst_proc_split)):
#         lst_proc_util = lst_proc_split[i].split()
#         lst_CPU.append(lst_proc_util[2])
#         lst_CPU_util.append(round(100-float(lst_proc_util[12]),2))
#         lst_CPU_idle.append(float(lst_proc_util[12]))
#
#     print("Number of CPU = "+str(len(lst_CPU)-1))
#     for i in range(1, len(lst_CPU)):
#         print("CPU "+lst_CPU[i]+" utilization = "+str(lst_CPU_util[i])+"%"+" (idle "+str(lst_CPU_idle[i])+"%)")
#
#     #returned tuple: CPU number, CPU utilization in %, CPU idle in %
#     return(lst_CPU, lst_CPU_util, lst_CPU_idle)
#
# processorsUtilization = processors_Utilization()
#
# # /////////////////////////////////// creat a sub derictory /////////////////////////




# print("create path:")
#
# ODB_RS=CreateODBSubDir(URL, "/Alarms/Alarms/"+hostoutput+ " " + "Memory Utilization")
# print(ODB_RS)
#
# # ODB_val_1=setODBkeyvalue(URL, '/Alarms/Alarms/Testnew', 'Condition',"/Health monitoring/Disk Space Utilization > 0")
# # print(ODB_val_1)
#
# ODB_val_1=setODBkeyvalue(URL, "/Alarms/Alarms/"+hostoutput+ " " + "Memory Utilization/", 'Active',1)
# print(ODB_val_1)

# ODB_val_1=setODBkeyvalue(URL, '/Alarms/Alarms/'+hostoutput+ " " + "Processors Utilization/", 'Condition','Health monitoring/Disk Space Utilization/nero numDSCheckedThanThr > 1')
# print(ODB_val_1)
#
# ODB_val_1=setODBkeyvalue(URL, "/Alarms/Alarms/"+hostoutput+ " " + "Processors Utilization/", 'Alarm Message','Some partition(s) has been filled more than threshold value')
# print(ODB_val_1)
# ODB_val_1=setODBkeyvalue(URL, '/Health monitoring/Disk Space Utilization/', hostoutput + " " + 'lastRead',timeoutput)


# def POSTrequestODBpaste(httpODB, ODBpath, ODBvar):
#     try:
#         # httpODB='http://131.225.179.174:8089?mjsonrpc'
#
#         header = {"Content-Type":"application/json","Accept":"application/json"}
#         pload={"jsonrpc":"2.0","id":None,"method":"db_paste","params":{"paths":[ODBpath], "values":[ODBvar]}}
#         r=requests.post(httpODB, json=pload, headers=header, timeout=50)
#         # print(r.text)
#         ODBr=json.loads(r.text)
#         # print(ODBr)
#         return ODBr["result"]["status"]
#
#
#     except requests.exceptions.ConnectionError:
#         print("Midas http connection failed! Establish connetion to Midas ODB")
#
# info_raw = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE)
# output = info_raw.communicate()[0].decode("utf-8")
# # # strtimeoutput = timeoutput
# # print(timeoutput)
# # cpuUtilization = get_processors_utilization()
# # print(len(cpuUtilization[1])-1)
# # chkVar=POSTrequestODBpaste(URL, "/Health monitoring/Processors Utilization/",  output)
# # if chkVar[0]==1:
# #     print("OBD key has been set successfully")
# # else:
# #     print("Error!")
#
# # chkVar=POSTrequestODBdelete(URL, "/Health monitoring/amila")
# # if chkVar[0]==1:
# #     print("OBD key has been set successfully")
# # else:
# #     print("Error!",chkVar)
#
# # chkVar=POSTrequestODBcreate(URL, "/Health monitoring/amila")
# # if chkVar[0]==1:
# #     print("OBD key has been set successfully")
# # else:
# #     print("Error!",chkVar)
#
# #get the hostnaame of the server
# hostinfo_raw = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE)
# hostoutput = hostinfo_raw.communicate()[0].decode("utf-8")
# # print("\n"+"Host Name:"+ hostoutput +"\n")
#
# ODB_RS=POSTrequestODBcreateString(URL, "/Health monitoring/", hostoutput+'amila1')
#
# # ODB_val=POSTrequestODBpaste(URL, "/Health monitoring/"+hostoutput+'amila1',"test")
# ODB_val=POSTrequestODBpaste(URL, '/Health monitoring/'+hostoutput+'amila1','test')
# print(ODB_val)









# //////////////////////////////////////////////////////////////
# -----------------------------Raise Alarm-------------------


# print "\nAlarm ODB keys\n"
# ODB_RS=CreateODBSubDir(URL, "/Alarms/Alarms/"+hostoutput+ " " + "Disk Space Utilization")
# print "result of CreateODBSubDir" +" "+ hostoutput + " " + "Disk Space Utilization" " =", ODB_RS
# #print("result" + "=" + "1")
# rep = 2
# for x in range(rep):
#     ODB_val_1=setODBkeyvalue(URL, "/Alarms/Alarms/"+hostoutput+ " " + "Disk Space Utilization/", 'Active',1)
#     # print "result of setODBkeyvalue Active = ", ODB_val_1
#
#     ODB_val_2=setODBkeyvalue(URL, '/Alarms/Alarms/'+hostoutput+ " " + "Disk Space Utilization/", 'Condition','Health monitoring/Disk Space Utilization/nero numDSCheckedThanThr > 1')
#     # print "result of setODBkeyvalue Condition = ", ODB_val_2
#
#     ODB_val_3=setODBkeyvalue(URL, "/Alarms/Alarms/"+hostoutput+ " " + "Disk Space Utilization/", 'Alarm Message','Some partition(s) has been filled more than threshold value')
#     # print "result of setODBkeyvalue Alarm Message = ", ODB_val_3
#
# print "result of setODBkeyvalue Active = ", ODB_val_1
# print "result of setODBkeyvalue Condition = ", ODB_val_2
# print "result of setODBkeyvalue Alarm Message = ", ODB_val_3
#
# # ODB_val_1=setODBkeyvalue(URL, "/Alarms/Alarms/"+hostoutput+ " " + "Disk Space Utilization/", 'Active',1)
# # print "result of setODBkeyvalue Active = ", ODB_val_1
# #
# # ODB_val_1=setODBkeyvalue(URL, '/Alarms/Alarms/'+hostoutput+ " " + "Disk Space Utilization/", 'Condition','Health monitoring/Disk Space Utilization/nero numDSCheckedThanThr > 1')
# # print "result of setODBkeyvalue Condition = ", ODB_val_1
# #
# # ODB_val_1=setODBkeyvalue(URL, "/Alarms/Alarms/"+hostoutput+ " " + "Disk Space Utilization/", 'Alarm Message','Some partition(s) has been filled more than threshold value')
# # print "result of setODBkeyvalue Alarm Message = ", ODB_val_1
#
# ODB_RS=CreateODBSubDir(URL, "/Alarms/Alarms/"+hostoutput+ " " + "Processors Utilization")
# print "\nresult of CreateODBSubDir" +" "+ hostoutput + " " + "Processors Utilization" " =", ODB_RS
# #print("result" + "=" + "1")
#
# ODB_val_1=setODBkeyvalue(URL, "/Alarms/Alarms/"+hostoutput+ " " + "Processors Utilization/", 'Active',1)
# print "result of setODBkeyvalue Active = ", ODB_val_1
#
# ODB_val_1=setODBkeyvalue(URL, '/Alarms/Alarms/'+hostoutput+ " " + "Processors Utilization/", 'Condition','Health monitoring/Pocessors Utilization/nero maxCPUchecked > 80%')
# print "result of setODBkeyvalue Condition = ", ODB_val_1
#
# ODB_val_1=setODBkeyvalue(URL, "/Alarms/Alarms/"+hostoutput+ " " + "Processors Utilization/", 'Alarm Message','Some processors are being overused')
# print "result of setODBkeyvalue Alarm Message = ", ODB_val_1
