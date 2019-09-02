import requests
import json
import datetime
import time
from prettytable import PrettyTable

tokenr = open('token.txt', 'r')
token = tokenr.read()

if len(token) != 26:
    while True:
        try:
            tokenr.close()
            API_key =  input ("Enter Authorization key here, you can find it in the 'Koppel App' section of the portal:")
            API_key = API_key.replace(" ", "")
            print(API_key)

            school = input('Enter school id (You can find it by going to the portal of your school and selecting the part between the https and the first dot. Example: bc-enschede):')
            url = "https://" + school + ".zportal.nl/api/v2/"
            schoolw = open('school.txt', 'w')
            schoolw.write(school)
            schoolw.close
            
            token = requests.post(url + "oauth/token", data={"grant_type":"authorization_code", "code":API_key}).json()
            token = token['access_token']
            tokenw = open('token.txt', 'w')
            tokenw.write(token)
            tokenw.close()
            break
        except:
            print('Wrong code or schoolcode or the zermelo is down... Try again momentarily...')
else:
    schoolr = open('school.txt', 'r')
    school = schoolr.read()
    url = "https://" + school + ".zportal.nl/api/v2/"
    print("You're logged in into: "+url)

while True:
    try:
        starttime = input('Please enter the time from which you want to know your appointments in this format: DD/MM/YYYY, Example: 06/1/2019: ')
        starttime = time.mktime(datetime.datetime.strptime(starttime, "%d/%m/%Y").timetuple())

        endtime = str(round(starttime + 86400))
        starttime = str(round(starttime))
        break
    except:
        print("Error")

roosterJSON = requests.get(url + "appointments?user=~me&access_token="+token+"&start="+starttime+"&end="+endtime).json()
appointments = roosterJSON['response']['data']

def start_field(appointment):
    return int(appointment['start'])
appointments.sort(key=start_field)

def time_string(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

x = PrettyTable()
x.field_names = ["Timeslot", "Teacher", "Subject", "Location"]

for appointment in appointments:
    teacher = str(appointment['teachers'])
    teacher = teacher.replace("'", "").replace("[", "").replace("]", "")
    subject = str(appointment['subjects'])
    subject = subject.replace("'", "").replace("[", "").replace("]", "")
    location = str(appointment['locations'])
    location = location.replace("'", "").replace("[", "").replace("]", "")
    if(appointment['cancelled']):
        x.add_row(['-', '-', '-', '-'])
    else:
        x.add_row([str(appointment['startTimeSlot']), teacher, subject, location])
print(x)
