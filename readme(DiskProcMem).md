###Which files and folders are used?
 
**The main works of this Repo is monitoring the CPU, diskspace and memory & POE monitoring**

###Monitoring CPU, DiskSpace and Memory

**CPU/DiskSpace/Memory** - It gives the information about DiskSpace, Processor Utilization and Memory Utilization and writes individual information to the ODB page.Also, it takes threshold values from user(ODB)page and compare with values obtained from each servers respectively and generate the alarms [Detailed Documentation](https://confluence.slac.stanford.edu/display/CDMS/1.6+Data+Acquisition+and+Triggering?preview=%2F187007679%2F363458660%2FDAQ_DQMComputermointoringsnolab.pdf). The folder **./SystemHealthMonitor/FinalCompMonitoring** has all the code reuired to run the scripts. We can set the cronjob in cdms-gateway computer to communicate with ODB page.

## Different type of files in ./SystemHealthMonitor/FinalCompMonitoring 

**CreateThresFirstTime.py** This is  one time running code which is required forinitilizing. for example [("ODB_Test_Value", 80),("NumDiskaboveTest_Value", 2),("MeanCPUutilThreshold", 75),("MemUtilThreshold", 75)] are initilized.

**dqsurfthreshold.py** This python scripts used for passing argument to **HMdqsurf.py** (from Midas Client not -installed server) to obtained utilization, threshold values.

**HMdqsurf.py** This code should reside in Midas Clientnot-installed server and takes threshold values from **dqsurfthreshold.py**.  We redirect the output to form Json file where all the information about utilization, threshold values and alarm inforamative are kept.

**FinalCodeCompileJson.py** We using threading python library and using os.system we run the scrpits to obtained different JSON files. Also, this script read the JSON and takes the values in required format and writes to ODB. This is the **main scrpit** which does the whole works taking other file. And also, cronjob is set in this file.

**/Json**It contains all the JSON files we obtained and has information about utilization, threshold values and alarm information.

### POEMonitoting

**POEMonitoring.py**- Monitors port power levels for both POE modules. If any ports go outside of the acceptable range (9-18 Watts), it writes to the ODB to trigger an alarm.


## Get the files & folder

To get the files you see in this repository, run the following command in a terminal:

```
git clone git@gitlab.com:supercdms/DAQ/SystemHealthMonitor.git
```

Here is the link for this [page](https://gitlab.com/supercdms/DAQ/SystemHealthMonitor) .

### Python requirements for ComputerMonitoring
The following libraries are required to run this code: **python3**, **numpy**, **psutill**, **pytz**, **os**, **datetime**,
**timezone**, **socket**,**threading**. Also, **midas.client** should be set up in that system.

These libraries should be installed in the system.
