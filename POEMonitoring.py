# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 12:24:17 2022

@author: garre
"""

import midas.client
import requests
from bs4 import BeautifulSoup as bs

client = midas.client.MidasClient("pytest")#, host_name="cdms-back-10g.cdmsdaq.snolab.ca")
#MaxPower = 18 #Max power allowed in watts
#MinPower = 9 #Min power allowed in watts
#KeyPath = "HealthMonitoring/POEMonitoring/POETest" #Path to key in ODB
#message = "**TEST** POE Power Levels Abnormal **TEST**"
#message1 = "THIS IS A TEST MESSAGE"


#URL for both POE status pages and port configuration
urlpoe1 = 'http://192.168.3.83/web/P24/view/view_system_status_g_mp_at.htm'
urlpoe2 = 'http://192.168.3.84/web/P24/view/view_system_status_g_mp_at.htm'
urlports1 ='http://192.168.3.83/web/P24/config/cfg_ports_en_dis.htm'
urlports2 ='http://192.168.3.84/web/P24/config/cfg_ports_en_dis.htm'

#Web call to view the POE status web pages. Parse with BeautifulSoup
s = requests.Session()
request = s.get(urlpoe1)
request2 = s.get(urlpoe2)
request3 = s.get(urlports1)
request4 = s.get(urlports2)
POE1content = request.content
POE2content = request2.content
Portconfigcontent1 = request3.content
Portconfigcontent2 = request4.content
POE1soup = bs(POE1content, features="lxml")
POE2soup = bs(POE2content, features="lxml")
Portsoup1 = bs(Portconfigcontent1, features="lxml")
Portsoup2 = bs(Portconfigcontent2, features="lxml")



#Finding enabled ports POE1
findportnums1 = []
for checkbox in Portsoup1.find_all('input', checked=True):
 find1 = ( str(checkbox).split('name="P')[1].split('_')[0] )
 findportnums1.append(find1)
 findportnums1 = [int(x) for x in findportnums1]
 

enports1 = [] #List that will contain enabled port numbers
for i in range(len(findportnums1)):
 calc1 = findportnums1[i] + 1
 enports1.append(calc1)

#Finding enabled ports POE2
findportnums2 = []
for checkbox in Portsoup2.find_all('input', checked=True):
 find2 = ( str(checkbox).split('name="P')[1].split('_')[0] )
 findportnums2.append(find2)
 findportnums2 = [int(x) for x in findportnums2]

enports2 = [] #List that will contain enabled port numbers
for i in range(len(findportnums2)):
 calc2 = findportnums2[i] + 1
 enports2.append(calc2)




#Getting POE port power levels from web status pages
POE1tabledata = []
POE2tabledata = []
for i in POE1soup.find_all('td'):
 content = i.text
 POE1tabledata.append(content)
for i in POE2soup.find_all('td'):
 content = i.text
 POE2tabledata.append(content)

Power1 = POE1tabledata[35:59]
POE1power = [float(x) for x in Power1] #Port power levels as a float
#print(POE1power)
Power2 = POE2tabledata[35:59]
POE2power = [float(x) for x in Power2] #Port power levels as a float
#print(POE2power)

enportspower1 = [POE1power[i] for i in findportnums1] #Power levels for only enabled ports
enportspower2 = [POE2power[i] for i in findportnums2]
#print(enportspower1)
#print(enportspower2)

KeyPath = "/HealthMonitoring/POEMonitoring/POE1" #Path to keys in ODB
KeyPath2 = "/HealthMonitoring/POEMonitoring/POE2"
Condition = "/HealthMonitoring/POEMonitoring/POE1 > 0" #Conditions to trigger alarm
Condition2 = "/HealthMonitoring/POEMonitoring/POE2 > 0"
message = "POE1 port power level(s) abnormal" #Alarm messages
message2 = "POE2 port power level(s) abnormal"
message3 = "Power level(s) too high *TEST MESSAGE*"
message4 = "Power level(s) too low *TEST MESSAGE*"
message5 = "Power levels too high and too low *TEST MESSAGE*"
MaxPower = 18 #Max Power allowed in Watts
MinPower = 9 #Min power allowed in Watts

#Just for testing
#POE1 = [9.5,12.3,15.4,14.5,16.1,17.5,14.1,10.8,9.9,16.5]
#POE2 = [9.5,12.3,15.4,14.5,16.1,17.5,14.1,10.8,9.9,16.5]

#Blank lists to store abnormal power levels
POE1powerhigh = [] #Will store power levels that are too high
POE1powerlow = [] #Will store power levels that are too low
POE2powerhigh = []
POE2powerlow = []

#Check power levels for POE1
for i in enportspower1:
 if (i > MaxPower):
  POE1powerhigh.append(i)
 if (i < MinPower):
  POE1powerlow.append(i)
#print(POE1powerhigh)
#print(POE1powerlow)

#Check power levels for POE2
for i in enportspower2:
 if (i > MaxPower):
  POE2powerhigh.append(i)
 if (i < MinPower):
  POE2powerlow.append(i)
#print(POE2powerhigh)
#print(POE2powerlow)


####################POE1



#If power levels are normal, set key to normal
if (len(POE1powerhigh) == 0 and len(POE1powerlow) == 0):
 client.odb_set(KeyPath, 0, create_if_needed=True)



#If power levels are abnormal, change the key
if (len(POE1powerhigh) >= 1 or len(POE1powerlow) >= 1):
 client.odb_set(KeyPath, 1, create_if_needed=True)

#Create an alarm for POE1
client.create_evaluated_alarm("POE1", Condition, message=message, alarm_class="Level Alarm", activate_immediately=False)

#TESTING MESSAGES
#if (len(POE1powerhigh) > 0):
# client.msg(message3)
#if (len(POE1powerlow) > 0):
# client.msg(message4)



####################POE2



#If power levels are normal, set key to normal
if (len(POE2powerhigh) == 0 and len(POE2powerlow) == 0):
 client.odb_set(KeyPath2, 0, create_if_needed=True)


#If power levels are abnormal, change the key
if (len(POE2powerhigh) >= 1 or len(POE2powerlow) >= 1):
 client.odb_set(KeyPath2, 1, create_if_needed=True)

#Create alarm for POE2
client.create_evaluated_alarm("POE2", Condition2, message=message2, alarm_class="Level Alarm", activate_immediately=False)      

client.disconnect()