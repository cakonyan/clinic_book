from __future__ import print_function
import verify.verify_user_email as verify
import os
from io import StringIO
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import subprocess
import sys
import json
import main


def capture_io():
    ''' This helps us not repeat the below function in the test_robot.py'''

    text_capture = StringIO()
    sys.stdout = text_capture

    return text_capture


def verify_token_exists():
    '''
    Returns true if ltoken file is available
    else: False
    '''

    if os.path.exists('token.pickle'):
        return True
    else:
        return False


def events_result(service, cal_id):
    '''
    Takes service and get the events from the calender
        Param 1 : service = service = build('calendar', 'v3', credentials=creds)
        Param 2 : now = datetime.datetime.utcnow().isoformat() + 'Z'
        Param 3 : number of results that must be displayed int
        Param 4 : Calender ID that will be displayed
        returns items from the events of the calender
    '''

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    seven_later = str(datetime.datetime.utcnow() + datetime.timedelta(7))
    seven_later = seven_later.replace(' ', 'T') + 'Z'

    events_result = service.events().list(calendarId=cal_id, 
                                        timeMin=now,
                                        timeMax=seven_later,
                                        singleEvents=True,
                                        orderBy='startTime').execute()

    return events_result.get('items', [])


def print_cal(events, cal_id):
    '''
    Prints the google cal in a neat way and returns a list of cal entries
        Param 1 : (int) number of results that you want to display
        Param 2 : events = events_result(service, cla_id)
        Param 3 : calender that will be printed
    '''
    events_list = []
    print(f'Getting {cal_id} upcoming events for the next 7 days')
    if not events:
        print('No upcoming events found.')
        return {}
    i = 1
    print(f'Date         Start    End      Description')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        
        date, start = start.split('T')
        start = start.split('+')[0]
        start = start[0:5]

        end = end.split('T')[1]
        end = end.split('+')[0]
        end = end[0:5]
        summary = event['summary']
        print(f'{date}   {start}    {end}    {summary}')
        events_list.append({f'event {i}' : {'date' : date, 'start' : start, 'end' : end, 'description' : summary }})
        i += 1
    
    events_list = {'id' : cal_id, 'events_list' : events_list}
    return events_list


def cal_view():
    '''
    Function Def:
        Prints out calendar events of the users calendar and the code clinics
        then saves the info on two json files to be used later.
    '''
    
    main.check_login_time_and_if_registered()

    token_pickle = verify.path_for_files('token.pickle')

    if verify_token_exists():
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        
    else:
        print(f'You havent registered yet your google WTC student account')
        print(f'Please type register')
        return False

    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    #Preparing the calender

    email_id = verify.get_email(service)

    events_for_volenteer = events_result(service, email_id)
    cclinc_id = 'c_h4803008kmuddgc9i7m939lsuk@group.calendar.google.com'
    practice_cal = 'c_5ah2f5nil2m8jb0kue61cun5d4@group.calendar.google.com'
    events_for_codeclinic = events_result(service, cclinc_id)

    student_events_list = print_cal(events_for_volenteer, email_id)
    print()
    code_clinic_events = print_cal(events_for_codeclinic, "Code Clinic's")

    # print(code_clinic_events)


    student_json = verify.path_for_files("view_calendar_data_file_student.json")
    cclinc_jason = verify.path_for_files("view_calendar_data_file_clinic.json")

    with open("view_calendar_data_file_student.json", "w") as f:
        json.dump(student_events_list, f, indent=1)
    with open("view_calendar_data_file_clinic.json", "w") as f:
        json.dump(code_clinic_events, f, indent=1)

    

if __name__ == "__main__":
    
    cal_view()

