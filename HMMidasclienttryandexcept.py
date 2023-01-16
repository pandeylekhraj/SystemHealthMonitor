
import subprocess
import pandas as pd
from io import StringIO
import midas.client
from collections import OrderedDict

client = midas.client.MidasClient("pytest",host_name="cdms-back-10g.cdmsdaq.snolab.ca")

#get the date and time cheked the serve
timeinfo_raw = subprocess.Popen("date", shell=True, stdout=subprocess.PIPE)
#print(timeinfo_raw)
timeoutput = timeinfo_raw.communicate()[0].decode("utf-8")
#print(timeoutput)
hostinfo_raw = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE)
str_hostinfo_raw=hostinfo_raw.communicate()[0].decode("utf-8")
host_split = str_hostinfo_raw.split(".")
#first four letter of the machine
hostoutput=host_split[0]

# print(host_split)
# print(hostoutput)
#create the hostname of the machine as subdirectory
#dqm.daq.midas.create("/HealthMonitoring/"+hostoutput, 15)

print("\n\n****************This is DiskSpaceUtilization Info*******************\n\n")


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
    for i in range(0,2):
        try:
            content=OrderedDict({"lastRead": timeoutput, "MaxDiskSpceChk%":max_usage, "MinDiskSpaceChk%":min_usage,"nmDiskSpaceChk":num_of_partitions , "nmGtrThreshold":higher_than_threshold })
            client.odb_set("/HealthMonitoring/"+hostoutput+"/DiskSpaceUtilization/",content,create_if_needed=True)
        except:
            pass


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


    #creating ODB keys and respective values in order to keep in webpage
    for i in range(0,2):
        try:
            content=OrderedDict({"lastRead": timeoutput, "nmCPUChk":len(dfProc1["CPU"])-1, "minCPUchk%": min(dfProc1['%utilize']),"maxCPUchk%": max(dfProc1['%utilize']) })
            client.odb_set("/HealthMonitoring/"+hostoutput+"/ProcessorsUtilization/",content,create_if_needed=True)
        except:
            pass


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

    #creating ODB keys and respective values in order to keep in webpage
    for i in range(0,2):
        try:
            content=OrderedDict({"lastRead": timeoutput, "MemChk%": MemUtilization, "TotMemChkWtSwap%": TotUtilization })
            client.odb_set("/HealthMonitoring/"+hostoutput+"/Mem/",content,create_if_needed=True)
        except:
            pass


memory_Utilization()

