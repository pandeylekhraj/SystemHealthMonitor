import subprocess
import sys
import re
import os
import pandas as pd
from io import StringIO
import requests
import json

URL = "http://dcrc02.triumf.ca:8081/?mjsonrpc"

def setODBkeyvalue(httpODB, ODBpath, ODBvar, ODBval):
    """for setting the specific datatype value in ODB keys for given webpage
    """
    try:
        header = {"Content-Type":"application/json","Accept":"application/json"}
        pload={"jsonrpc":"2.0","id":None,"method":"db_paste","params":{"paths":[ODBpath+ODBvar], "values":[ODBval]}}
        r=requests.post(httpODB, json=pload, headers=header, timeout=50)
        ODBr=json.loads(r.text)
        return ODBr["result"]["status"]
    except requests.exceptions.ConnectionError:
        print("Midas http connection failed! Establish connetion to Midas ODB")


def CreateODBkeyString(httpODB, ODBpath, ODBvar):
    """for creating string variable ODB key in the given webpage
    """
    try:
        header = {"Content-Type":"application/json","Accept":"application/json"}
        pload={'jsonrpc':'2.0','id':None,'method':'db_create','params':[{'path':ODBpath+ODBvar, 'type':12, 'string_length':64}]}
        r=requests.post(httpODB, json=pload, headers=header, timeout=50)
        ODBr=json.loads(r.text)
        return ODBr["result"]["status"]
    except requests.exceptions.ConnectionError:
        print("Midas http connection failed! Establish connetion to Midas ODB")


def CreateODBkeyInt(httpODB, ODBpath, ODBvar):
    """for creating Integer variable ODB key in the given webpage
    """
    try:
        header = {"Content-Type":"application/json","Accept":"application/json"}
        # pload={'jsonrpc':'2.0','id':None,'method':'db_create','params':[{'path':ODBpath+ODBvar, 'type':9, 'string_length':64}]}
        pload={'jsonrpc':'2.0','id':None,'method':'db_create','params':[{'path':ODBpath+ODBvar, 'type':7}]}
        r=requests.post(httpODB, json=pload, headers=header, timeout=50)
        ODBr=json.loads(r.text)
        return ODBr["result"]["status"]
    except requests.exceptions.ConnectionError:
        print("Midas http connection failed! Establish connetion to Midas ODB")


def CreateODBkeyFloat(httpODB, ODBpath, ODBvar):
    """for creating float variable 4 bytes ODB key in the given webpage
    """
    try:
        header = {"Content-Type":"application/json","Accept":"application/json"}
        # pload={'jsonrpc':'2.0','id':None,'method':'db_create','params':[{'path':ODBpath+ODBvar, 'type':9, 'string_length':64}]}
        # pload={'jsonrpc':'2.0','id':None,'method':'db_create','params':[{'path':ODBpath+ODBvar, 'type':7}]}
        pload={'jsonrpc':'2.0','id':None,'method':'db_create','params':[{'path':ODBpath+ODBvar, 'type':9}]}
        r=requests.post(httpODB, json=pload, headers=header, timeout=50)
        ODBr=json.loads(r.text)
        return ODBr["result"]["status"]
    except requests.exceptions.ConnectionError:
        print("Midas http connection failed! Establish connetion to Midas ODB")


def CreateODBSubDir(httpODB, ODBpath):
    """for creating subdirectory (15 is type for that)and finally for ODB keys in the given webpage
    """
    try:
        header = {"Content-Type":"application/json","Accept":"application/json"}
        pload={'jsonrpc':'2.0','id':None,'method':'db_create','params':[{'path':ODBpath, 'type':15}]}
        r=requests.post(httpODB, json=pload, headers=header, timeout=50)
        ODBr=json.loads(r.text)
        #return ODBr["result"]["data"][0]
        return ODBr["result"]["status"]

    except requests.exceptions.ConnectionError:
        print("Midas http connection failed! Establish connection to Midas ODB")


#get the date and time cheked the serve
timeinfo_raw = subprocess.Popen("date", shell=True, stdout=subprocess.PIPE)
#print(timeinfo_raw)
timeoutput = timeinfo_raw.communicate()[0].decode("utf-8")
#print(timeoutput)
hostinfo_raw = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE)
str_hostinfo_raw=hostinfo_raw.communicate()[0].decode("utf-8")
#print (str_hostinfo_raw)
#print (hostinfo_raw)
host_split = str_hostinfo_raw.split(".")
#first four letter of the machine
hostoutput=host_split[0]

# # print(host_split)
# print(hostoutput)

ODB_var_1=CreateODBSubDir(URL, "/HealthMonitoring/"+hostoutput)
print('result of CreateODBSubDir {} = {}'.format(hostoutput,ODB_var_1))


print("\n\n****************This is DiskSpaceUtilization Info*******************\n\n")
#
def disk_Utilization():

    """if we hit "df -hT" in our linux terminal or ssh terminal we can see partition knowledge.
    Particularly, we use subprocess, one of the python modules and use pandas Dataframes
    to read out the output of df -hT. Here, we are interested on '/dev/' and also '/dev/'
    memory utilize less than 100%. After that we count number of partition, max_usage,
    min usage. Also, we set ODB_test_variable which is 90 (threshold but may be changed )and find
    the number of partition higher than that.
    At last we keep  current run datetime and 4 results (number of partion, min_usage, max_usage,
    number higher_than_threshold) using webcalling or using CreateODB function
    """
    ODB_test_variable = 90
    num_of_partitions = 0
    higher_than_threshold = 0
    max_usage = 0
    min_usage =100
    print('Threshold Percentage Value for Disk =  {} % \n'.format(str(ODB_test_variable)))
    print("Partitions Utilization")
    meminfo_raw = subprocess.Popen("df -hT", shell=True, stdout=subprocess.PIPE)
    #  calling df -hT terminal command by python scripts using subprocess
    df = pd.read_csv(StringIO(meminfo_raw.communicate()[0].decode("utf-8")))
    #heading=df.columns.str.split()
    #print(heading, '*****')
    #converting the table we see in df -hT into data frame
    # list_column = list(df)
    # x=df.columns.values.to_list()
    # print(x,'apple')
    # print("datafro",list_column)
    # print("type_datafro", list_column[1])

    list=[df.loc[i].str.split()[0] for i in range(len(df))]
    df1=pd.DataFrame(list, columns= ['filesystem',"Type","Size","Used","Avail","Use%","Mounted on"])
    #df1=pd.DataFrame(list, columns=heading)
    #Rearranging the columns we can see the csv file
    df1['Use']=df1['Use%'].str.replace('%','')
    # creating new columns replacing %
    df2 = df1[df1['filesystem'].str.contains('/dev/')]
    #selecting /dev/ partition of of other partition
    df3_df = df2[df2['Use'].astype(int) < 100]
    #there comes one partition with 100% used so removing that partition
    #print(df3_df)
    df_new = df3_df[['filesystem','Use']]
    #df3_df.to_csv('file_name.csv')
    #df1.to_csv('file_name1.csv')
    #print(df_new)
    for values in df3_df['Use']:
        #print(df3_df['filesystem'],values)
        values = float(values)
        #converting string into float
        num_of_partitions += 1
        if values > max_usage:
            max_usage =values
            #print(max_usage)
        if values < min_usage:
            min_usage =values
            #print(min_usage)
        if values > ODB_test_variable:
            higher_than_threshold += 1
    if higher_than_threshold < 1:
        higher_than_threshold = 0
    print('Number of partitions checked: {}'.format(str(num_of_partitions)))
    print('number of partitions higher than threshold value: {}'.format(str(higher_than_threshold)))
    print('Maximum Utilized partition percentage: {} %'.format(str(max_usage)))
    print('Minimum Utilized partition percentage: {} %'.format(str(min_usage)))

    ODB_var_1=CreateODBkeyString(URL, "/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/",'lastRead')
    print ('result of CreateODBkeyString lastRead = {}'.format(ODB_var_1))
    ODB_val_1=setODBkeyvalue(URL, "/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/",'lastRead', timeoutput)
    print ('result of setODBkeyvalue of lastRead = {}'.format(ODB_val_1))
    ODB_var_1=CreateODBkeyInt(URL, "/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/",'MaxDiskSpceChk%')
    print('result of CreateODBkeyInt of maxDiskSpaceChecked = {}'.format(ODB_var_1))
    # ODB_val_1=setODBkeyvalue(URL, '/HealthMonitoring/DiskSpaceUtilization/', hostoutput + " " + 'maxDiskSpaceChecked',str(max_usage)+"%"
    ODB_val_1=setODBkeyvalue(URL, "/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/",'MaxDiskSpceChk%', max_usage)
    print('result of setODBkeyvalue of maxDiskSpaceChecked = {}'.format(ODB_val_1))
    ODB_var_1=CreateODBkeyInt(URL, "/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/",'MinDiskSpaceChk%')
    print('result of CreateODBkeyInt minDiskSpaceChecked = {}'.format(ODB_var_1))
    ODB_val_1=setODBkeyvalue(URL, "/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/",'MinDiskSpaceChk%',min_usage)
    print('result of setODBkeyvalue of minDiskSpaceChecked = {}'.format(ODB_val_1))
    #ODB_var_1=CreateODBkeyBkeyvalue of {} numDiskSpaceChecked = {}'.format(hostoutput, ODB_val_1))
    ODB_var_1=CreateODBkeyFloat(URL, "/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/",'nmDiskSpaceChk')
    print('result of CreateODBkeyFloat numDiskSpaceChecked = {}'.format(ODB_var_1))
    # ODB_val_1=setODBkeyvalue(URL, '/HealthMonitoring/DiskSpaceUtilization/', hostoutput + " " + 'numDiskSpaceChecked',str(num_of_partitions))
    ODB_val_1=setODBkeyvalue(URL, "/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/",'nmDiskSpaceChk', num_of_partitions)
    print('result of setODBkeyvalue of numDiskSpaceChecked = {}'.format(ODB_val_1))
    ODB_var_1=CreateODBkeyFloat(URL, "/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/",'NumGtrThreshold')
    print('result of CreateODBkeyFloat NumGtrThanThreshold = {}'.format(ODB_var_1))
    ODB_val_1=setODBkeyvalue(URL, "/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/",'NumGtrThreshold',higher_than_threshold)
    print('result of setODBkeyvalue NumGtrThanThreshold = {}'.format(ODB_val_1))

disk_Utilization()

print("\n \nDiskSpaceUtilization ODB keys\n")


def processors_Utilization():
    """if we hit "mpstat -P ALL" in our linux terminal or ssh terminal we can see processors knowledge clearly.
    Particularly, we use subprocess, one of the python modules and use pandas Dataframes
    to read out the output of mpstat -P ALL. Here, we are interested on "CPU" & "%idle" columns and we create next
    column used doing (100 -"idle"). After that we count number of processors, min CPU processors utilized, max
    CPU utilized.
    At last we keep  current run datetime and 3 results (number of processors,min CPU processors utilizes,max
    CPU utilized) using webcalling or using CreateODB function
    """
    ProcInfoRaw = subprocess.Popen("mpstat -P ALL", shell=True, stdout=subprocess.PIPE)
    # convert bite format into a string format
    df_Proc = pd.read_csv(StringIO(ProcInfoRaw.communicate()[0].decode("utf-8")))
    listProc=[df_Proc.loc[i].str.split()[0] for i in range(len(df_Proc))]
    dfProc1=pd.DataFrame(listProc)
    dfProc1.columns = dfProc1.iloc[0]
    #columns names
    dfProc1.drop(0 , axis=0, inplace=True)
    dfProc1= dfProc1.loc[:, ["CPU","%idle"]]
    #print(dfProc1)
    dfProc1['%utilize'] = round(100 - dfProc1["%idle"].astype('float'),2)
    #makes columns we need
    # print(dfProc1)
    #print(dfProc1.columns)
    # print(len(dfProc1["CPU"]))
    #max(lst_CPU_util)
    # print(max(dfProc1['%utilize']))
    # print(min(dfProc1['%utilize']))

    for index, row in dfProc1.iterrows():
        # print(index)
        if(index!=1):
            print('CPU {} utilization = {} % (idle {} %)'.format(row['CPU'],str(row["%utilize"]),str(row["%idle"])))

    # #we got the desired columns
    ##Below lines also work dataframe is converted into list
    # lst_CPU = dfProc1["CPU"].to_list()
    # lst_CPU_idle =dfProc1["%idle"].to_list()
    # lst_CPU_util= [round(100 - float(x),2) for x in lst_CPU_idle]
    # print(lst_CPU_util)
    # #CPU number, CPU utilization in %, CPU idle from Series to list
    # print('Number of CPU = {}'.format(str(len(lst_CPU)-1)))
    # for i in range(1, len(lst_CPU)):
    #     print('CPU {} utilization = {} % (idle {} %)'.format(lst_CPU[i],str(lst_CPU_util[i]),str(lst_CPU_idle[i])))
    print("\nProcessorsUtilization ODB keys\n \n")

    #creating ODB keys and respective values in order to keep in webpage
    ODB_var_2=CreateODBkeyString(URL, "/HealthMonitoring/"+hostoutput+"/ProcessorsUtilization/",'lastRead')
    ODB_val_2=setODBkeyvalue(URL, "/HealthMonitoring/"+hostoutput+"/ProcessorsUtilization/",'lastRead',timeoutput)
    print('result of CreateODBkeyString lastRead = {}'.format(ODB_var_2))
    print('result of setODBkeyvalue lastRead = {}'.format(ODB_val_2))
    ODB_var_3=CreateODBkeyInt(URL, "/HealthMonitoring/"+hostoutput+"/ProcessorsUtilization/",'nmCPUChk')
    ODB_val_3=setODBkeyvalue(URL, "/HealthMonitoring/"+hostoutput+"/ProcessorsUtilization/",'nmCPUChk',len(dfProc1["CPU"])-1)
    print('result of CreateODBkeyInt numCPUchecked ={}'.format(ODB_var_3))
    # ODB_val_3=setODBkeyvalue(URL, '/HealthMonitoring/ProcessorsUtilization/', hostoutput + " " + 'numCPUchecked',str(len(processorsUtilization[1])-1))
    print('result of setODBkeyvalue numCPUchecked ={}'.format(ODB_val_3))
    ODB_var_4=CreateODBkeyFloat(URL, "/HealthMonitoring/"+hostoutput+"/ProcessorsUtilization/",'minCPUchk%')
    ODB_val_4=setODBkeyvalue(URL, "/HealthMonitoring/"+hostoutput+"/ProcessorsUtilization/",'minCPUchk%',min(dfProc1['%utilize']))
    print('result of CreateODBkeyFloat  minCPUchecked ={}'.format(ODB_var_4))
    print('result of setODBkeyvalue of  minCPUchecked ={}'.format(ODB_val_4))
    # ODB_var_5=CreateODBkeyString(URL, "/HealthMonitoring/Processors Utilization/", hostoutput + " " + 'maxCPUchecked')
    ODB_var_5=CreateODBkeyFloat(URL, "/HealthMonitoring/"+hostoutput+"/ProcessorsUtilization/",'maxCPUchk%')
    ODB_val_5=setODBkeyvalue(URL, "/HealthMonitoring/"+hostoutput+"/ProcessorsUtilization/",'maxCPUchk%',max(dfProc1['%utilize']))
    print('result of CreateODBkeyFloat  maxCPUchecked ={}'.format(ODB_var_5))
    # ODB_val_5=setODBkeyvalue(URL, '/HealthMonitoring/Processors Utilization/', hostoutput + " " + 'maxCPUchecked',str(max(processorsUtilization[1])) )
    print('result of setODBkeyvalue of  maxCPUchecked ={}'.format(ODB_val_5))

processors_Utilization()


print("\n \n****************This is MemoryUtilization Info*******************\n")


def memory_Utilization():

    """if we hit "free -t" in our linux terminal or ssh terminal we can see memory knowledge clearly.
    Particularly, we use subprocess, one of the python modules and use pandas Dataframes
    to read out the output of free -t. Here, we are interested on "total" & "used" columns of Mem and
    total (Mem plus Swap). After that we calculate corresponding percentage memory_Utilization (used *100%/total)
    for mem and total (Mem plus Swap).
    At last we keep  current run datetime and 2 results (memory_Utilization,TotalMemNSwap) using webcalling or using CreateODB function
    """
    memInfoRaw = subprocess.Popen("free -t", shell=True, stdout=subprocess.PIPE)
    dfMem = pd.read_csv(StringIO(memInfoRaw.communicate()[0].decode("utf-8")))
    listMem=[dfMem.loc[i].str.split()[0] for i in range(len(dfMem))]
    #print(listMem)
    dfMem1=pd.DataFrame(listMem,columns= ['','total',"used",'free',"shared","buff/cache","available"])
    #print(dfMem1)
    UsedMem = dfMem1["used"].to_list()
    TotMem = dfMem1["total"].to_list()
    #print(type(UsedMem[0]), '#########')
    #print(UsedMem,TotMem)
    MemUtilization= round((float(UsedMem[0])/float(TotMem[0]))*100, 2)
    TotUtilization= round((float(UsedMem[2])/float(TotMem[2]))*100, 2)
    print(type(MemUtilization),'**********')
    print('Memoryutilization = {} %'.format(MemUtilization))
    print('TotalUtilizationMemSwap = {} %'.format(TotUtilization))
    print("\nMemoryUtilization ODB keys\n")

    ODB_var_6=CreateODBkeyString(URL, "/HealthMonitoring/"+hostoutput+"/MemoryUtilization/", 'lastRead')
    ODB_val_6=setODBkeyvalue(URL, "/HealthMonitoring/"+hostoutput+"/MemoryUtilization/", 'lastRead',timeoutput)
    print('result of CreateODBkeyString lastRead = {}'.format(ODB_var_6))
    print('result of setODBkeyvalue of lastRead = {}'.format(ODB_val_6))
    # ODB_var_7=CreateODBkeyString(URL, "/HealthMonitoring/MemoryUtilization/", hostoutput + " " + 'memChecked')
    ODB_var_7=CreateODBkeyFloat(URL, "/HealthMonitoring/"+hostoutput+"/MemoryUtilization/",'memChk%')
    # ODB_val_7=setODBkeyvalue(URL, '/HealthMonitoring/MemoryUtilization/', hostoutput + " " + 'memChecked',str(max(processorsUtilization[1])) )
    ODB_val_7=setODBkeyvalue(URL, "/HealthMonitoring/"+hostoutput+"/MemoryUtilization/",'memChk%', MemUtilization)
    print('result of CreateODBkeyFloat lastRead = {}'.format(ODB_var_7))
    print('result of setODBkeyvalue of lastRead = {}'.format(ODB_val_7))
    ODB_var_8=CreateODBkeyFloat(URL, "/HealthMonitoring/"+hostoutput+"/MemoryUtilization/",'TotMemChkWtSwap%')
    ODB_val_8=setODBkeyvalue(URL, "/HealthMonitoring/"+hostoutput+"/MemoryUtilization/",'TotMemChkWtSwap%', TotUtilization)
    print('result of CreateODBkeyFloat lastRead = {}'.format(ODB_var_8))
    print('result of setODBkeyvalue of lastRead = {}'.format(ODB_val_8))

memory_Utilization()


print("\nAlarm ODB keys\n")

# def RaiseAlarm(Subfol,Key,KeyValue):
#     """This is for creating subfolder Key and value for Alraming the ODB Key. Here we are setting the following conditions.
#     DiskSpaceUtilization if NumGtrThanThreshold > 0
#     processorsUtilization if 'maxCPUchecked > 95.00'
#     MemoryUtilizationMem if memChecked > 90.00
#     MemoryUtilizationTotMem if TotMemCheckedMemNSwap > 75.00
#     """
#     ODB_RS=CreateODBSubDir(URL, "/Alarms/Alarms/"+hostoutput+ Subfol)
#     print('result of CreateODBSubDir {} {} = {}'.format(hostoutput,Subfol,ODB_RS))
#     rep = 25
#     for x in range(rep):
#         ODB_val=setODBkeyvalue(URL, "/Alarms/Alarms/"+hostoutput+ Subfol +"/" , Key, KeyValue)
#     print('result of setODBkeyvalue {} = {}'.format(Key, ODB_val,))
#
# RaiseAlarm('DiskSpaceUtilization','Active',1)
# RaiseAlarm('DiskSpaceUtilization','Type',3)
# RaiseAlarm('DiskSpaceUtilization','Condition','HealthMonitoring/DiskSpaceUtilization/'+hostoutput+' '+ 'nmGtrThrhld > 0')
# RaiseAlarm('DiskSpaceUtilization','Alarm Class','Level Alarm')
# RaiseAlarm('DiskSpaceUtilization','Alarm Message','Some partitions of ' + hostoutput +' computer are filled more than 90 percent')
# print()
#
# RaiseAlarm('ProcessorsUtilization','Active',1)
# RaiseAlarm('processorsUtilization','Type', 3)
# RaiseAlarm('ProcessorsUtilization','Condition','HealthMonitoring/ProcessorsUtilization/'+hostoutput+' '+ 'maxCPUchk% > 95.00')
# RaiseAlarm('ProcessorsUtilization','Alarm Class','Level Alarm')
# RaiseAlarm('ProcessorsUtilization','Alarm Message','Some processors of ' + hostoutput + ' computer have reached more than 95 percent')
# print()
#
# RaiseAlarm('MemoryUtilizationMem','Active',1)
# RaiseAlarm('MemoryUtilizationMem','Type', 3)
# RaiseAlarm('MemoryUtilizationMem','Condition','HealthMonitoring/MemoryUtilization/'+hostoutput+' '+ 'memChk% > 90.00')
# RaiseAlarm('MemoryUtilizationMem','Alarm Class','Level Alarm')
# RaiseAlarm('MemoryUtilizationMem','Alarm Message','Memory of ' + hostoutput + ' is filled more than 90 percent')
# print()
#
#
# RaiseAlarm('MemoryUtilizationTMem','Active',1)
# RaiseAlarm('MemoryUtilizationTMem','Type', 3)
# RaiseAlarm('MemoryUtilizationTMem','Condition','HealthMonitoring/MemoryUtilization/'+hostoutput+' ' +'TotMemChkWtSwap% > 75.00')
# RaiseAlarm('MemoryUtilizationTMem','Alarm Class','Level Alarm')
# RaiseAlarm('MemoryUtilizationTMem','Alarm Message','Total Memory including SWAP of ' + hostoutput + ' is filled more than 75 percent')
