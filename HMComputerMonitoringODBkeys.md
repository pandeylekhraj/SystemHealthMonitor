### HealthMonitoring/ComputerMonitoring ODBkeys
[detailed documentation](https://confluence.slac.stanford.edu/display/CDMS/SuperCDMS+DAQ+Documentation?preview=/225983675/363460667/DAQ_DQM%20Introduction.pdf)
## HealthMonitoring/ComputerMonitoring/ThresholdControl/cdms-dqsurf
               
**ODB_Test_Value** Threshold to check for disk partition. for example Disk partition used % =[35, 65], let think an array, if **ODB_Test_Value=80 ** means, 80 iscompared with 35, 65 ( 2 partition ). Both the values are lesser than 80. So, DiskSpaceUtilizationODBkey i.e **nmGtrThreshold=0**(This ODBkeys lies on HealthMonitoring/ComputerMonitoring/ cdms-dqsurf <one of respective server>/DiskSpaceUtilization. If Disk partition used % =[35, 85], than **nmGtrThreshold=1**

**NumDiskaboveTest_Value**This is the threshold value for comparing DiskSpaceUtilization. for example,  **nmGtrThreshold=0**(This ODBkeys lies on HealthMonitoring/ComputerMonitoring/ cdms-dqsurf <one of respective server>/DiskSpaceUtilization.if  user gives the **NumDiskaboveTest_Value=1** then value is 0 and threshold value is 1 so no alarm for DiskSpaceUtilization is created.  if value are higher or equal to threshold we observe from the respective server. if we keep thrshold values higher alarm stops.

**MeanCPUUtilThreshold** This is the thrshold value for comparing ProcessorUtilization,which is used to compare with **MeanCPUutilized%** (This ODBkeys lies on HealthMonitoring/ComputerMonitoring/ cdms-dqsurf <one of respective server>/ProcessorUtilization). If utilization value is greater than set values for then alarm is set.

**MemUtilThreshold** This is the threshold value for comparing MemoryUtilization, which is used to compare with **memoryUsed%** (This ODBkeys lies in HealthMonitoring/ComputerMonitoring/ cdms-dqsurf <one of respective server>/MemoryUtilization.


### Utilization Values
## 1) DiskSpace Utilization
It lies in  HealthMonitoring/ComputerMonitoring/cdms-dqsurf(one server)/DiskSpaceUtilization. It has the following ODB Keys
**LastRead** We will retrieve datetime using python modules. It helps to know the latest check time.
**nmDiskSpaceChk** It checks number of disk partition
**MaxDiskSpaceChk%** Maximum values of disk partition
**MinDiskSpaceChk%** minimum values of disk partition
**nmGtrThreshold** disk partition values are compares withthreshold value **ODB_Test_Value**(set by the user) which we can see (HealthMonitoring/ComputerMonitoring/ThresholdControl/cdms-dqsurf(respective server)/). This ** ODB_Test_Value** is lower then **nmGtrThreshold** will be higher and  more chances to get alarm. Setting right threshols for ODB_Test_Value is necessary.

## 2) ProcessorUtilization
It lies in  HealthMonitoring/ComputerMonitoring/cdms-dqsurf(one server)/ProcessorUtilization. It has the following ODB Keys
**LastRead** We will retrieve datetime using python modules. It helps to know the latest check time.
**nmCPUs* checks number of CPU used
**MaxDiskSpaceChk%** maximum CPU Utilization value for 1 sec duration
**MinDiskSpaceChk%** minimun CPU Utilization value for 1 sec duration
**MeanCPUutilized%** It gives average values of all the processor. If mean value is greater than threshold set (Look at threshold control values) in ODB then alerts the user.

## 3) MemoryUtilization
It lies in  HealthMonitoring/ComputerMonitoring/cdms-dqsurf(one server)/MemoryUtilization. It has the following ODB Keys
**LastRead** We will retrieve datetime using python modules. It helps to know the latest check time.
**MemoryUsed%** gives the memory utilized value. If utilized value is greater than threshold value(check at threshod control values) then alarm is created for respective server.


### Alarms
If the respective conditions are meet for their respective server then alarms are created. So, to control over alarm the respective thrshold control values is to and run the python script kept in the cronjob in gateway by changing time for 1 sec
