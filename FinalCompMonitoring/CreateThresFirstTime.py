#connecting python to ODB
#Lekhraj USD
#initilize the values if the python script runs for the first time.
 
import midas.client
from collections import OrderedDict
# midas client helps to connect code with odb page
client = midas.client.MidasClient("pytest")

#Keeping some variable and value for initialing User can change from ODB 
content=OrderedDict([("ODB_Test_Value", 80),("NumDiskaboveTest_Value", 2),("MeanCPUutilThreshold", 75),("MemUtilThreshold", 75)])

#Listing all the server 
Server=["cdms-gw","cdms-back","cdms-fe1","cdms-fe2","cdms-fe3","cdms-dq1","cdms-dq2","cdms-dqweb","cdms-dqsurf"]

#Using for loop to initilize the threshold for all the Server
for i in Server:
    client.odb_set("/HealthMonitoring/ComputerMonitoring/ThresholdControl/"+str(i),content)

