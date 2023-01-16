import midas.client
client=midas.client.MidasClient('pytest')
ODB_test=client.odb_get('/HealthMonitoring/ComputerMonitoring/ThresholdControl/cdms-dqsurf/ODB_Test_Value')
print(ODB_test)
