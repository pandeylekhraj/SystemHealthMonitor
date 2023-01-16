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

# ODB_test_variable=dublicateODBkeyvalue(URL, "/Health monitoring/Disk Space Utilization/", 'Threshold value for Partition')
#
# print(ODB_test_variable)

ODB_test_variable=dublicateODBkeyvalue(URL, "/Health monitoring/Test/", 'test variable')
# print(ODB_test_variable)
print("Threshold Percentage Value for Disk = "+ str(ODB_test_variable) +'%'+'\n')
