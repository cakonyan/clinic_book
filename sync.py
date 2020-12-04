from __future__ import print_function
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import datetime
import pickle
import os.path
import sys
import random
import time
import subprocess
import string
import json
import clinic


def colors():
    
    default = "\033[1;0;0m"
    blue = "\033[1;34;10m"
    red = "\033[1;31;10m"
    green = "\033[1;32;10m"
    yellow = "\033[1;33;10m"
    pink = "\033[1;35;10m"

    return blue, red, green, yellow, pink, default


def authorize():

    """
    - Connects to the google API
    - Returns creds - from the 'token.pickle'
    """

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)    

    # If there are no (valid) credentials available, let the user log in.
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
        else:
            flow = InstalledAppFlow.from_client_secrets_file('creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def store_data():
    """
    - Downloads the slots data from api
    - Dumps the events in json file(hidden)
    """

    events = view_events()
    events_codes = {}

    for x in events:
        code = unique_Id()
        events_codes[code] = x
    
    with open('.slots_data.json', 'w') as data_file:
        json.dump(events_codes, data_file, indent=4)

    
def view_events():
    """
    - PAR: creds - from authorize()
    - Shows available slot to book
    """

    with clinic.suppress_output():
        creds = authorize()
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        
        # Call the Calendar API
        # 'Z' indicates UTC time

        # clinic calendar_Id to view available slots
        events_result = service.events().list(
            calendarId='c_h4803008kmuddgc9i7m939lsuk@group.calendar.google.com',
            timeMin=now,
            maxResults=10, 
            singleEvents= True,
            orderBy='startTime').execute()

        events = events_result.get('items')
    
    return events


def table_headers():
    print("+------------------------------------------------------------------------------+")
    print("|                                   |                      |                   |")
    print("|             User-ID               |         Date         |        Time       |")
    print("+-----------------------------------+----------------------+-------------------+")


def sort_calendar_data(events):

    """
    - sorts the data in the event
    - returns a table of the available slots
    """
    blue, red, green, yellow, pink, default = colors()

    if not events:
        table_headers()
        print(f"|" + " "*29 + f"{red} No Available slots {default}" + " "*29 + "|")
        print(f"+------------------------------------------------------------------------------+")
        sys.exit()

    table_headers()

    for code, event in events.items():
        
        color = green

        if 'attendees' in event:
            color = red

        cal_time = event['start']['dateTime'][11:16] + " - " + event['end']['dateTime'][11:16]
        cal_date = event['start']['dateTime'][:10]

        print(f"|       {code}       |      {color}{cal_date}{default}      |   {color}{cal_time}{default}   |")
        print("+---------------------+------------------------------------+-------------------+")


def unique_Id():
    """
    - returns a unique code to access the slots easily
    """
    alpha_num   = string.ascii_lowercase + '123456789'
    index       = [random.randint(1,len(alpha_num) -1) for x in range(21)]

    unique_code_i = [alpha_num[x] for x in index]
    unique_code   = ''
    x = 0

    while x <= 20:
        unique_code += unique_code_i[x]
        x +=1 
    
    return unique_code


def user_slot():

    """
    - returns date and time of user
    - returns email id and user-name of user
    - the times are used to open slots
    """

    try:
        date = input("Date [Format YYYYMMDD] : ")
        time = input("Time [Format hhmm] : ")

        year, month, day       = date[:4], date[4:6], date[6:]
        start_hour, start_min  = time[:2], time[2:]
        
        date = datetime.date(int(year), int(month), int(day))
        
        verify_time(start_hour, start_min)

        end_hour, end_min, day  = end_time(start_hour, start_min, year, month, day)
        end_hour, end_min       = str(end_hour), str(end_min)
        updated_date            = datetime.date(int(year), int(month), int(day))

        start_period = datetime.time(int(start_hour), int(start_min), 00)
        end_period   = datetime.time(int(end_hour), int(end_min), 00)
        
        # For the start and end of the api slot

        start_period, end_period = str(start_period), str(end_period)
        start_period = format(date) + "T" + start_period
        end_period   = format(updated_date) + "T" + end_period

        print(start_period)
        print(end_period)
        return start_period, end_period

    except Exception:
        code  = '403'
        error = 'Date & Time'
        error_message(error, code)


def open_events():

    """
    - Creates an availability slot [student] [code clinics]
    - SCOPES is for edit events only
    - PAR - user > email_id
          - slot date and time - date_time
    """
    creds = authorize()
    start_period, end_period = user_slot()

    blue, red, green, yellow, pink, default = colors()

    service = build('calendar', 'v3', credentials=creds)

    try:      

        event = {
            'summary': "Clinic Appointment",
            'description': "Dr Python 3",

            'start': {
                'dateTime' : start_period,
                'timeZone' : 'CAT'
                    },

            'end' : {
                'dateTime' : end_period,
                'timeZone' : 'CAT'
                    }}

        event = service.events().insert(calendarId='c_h4803008kmuddgc9i7m939lsuk@group.calendar.google.com',
                                        body=event,
                                        sendNotifications=True).execute()

        print(green+"Event Created! : You will have a patient soon.")

    except Exception:
        code  = '405'
        error = 'Events'
        error_message(error, code)
        

def error_message(error, code):

    blue, red, green, yellow, pink, default = colors()
    
    print(red + f"{code}. {error} Error.")
    print(default + "Verify your details! That's all you need to do.")
    sys.exit()


def end_time(start_hour, start_min, year, month, day):

    end_hour = int(start_hour)
    end_min  = int(start_min) + 30
    year     = int(year)
    month    = int(month)
    day      = int(day)

    while end_min > 59:
        
        end_hour += 1
        end_min  -= 60

        if end_hour > 23:
            end_hour = 00
            day += 1
        
    return end_hour, end_min, day


def verify_time(start_hour, start_min):

    blue, red, green, yellow, pink, default = colors()

    if int(start_hour) > 23:
        print(red + "ERROR MESSAGE WANTED")
        sys.exit()

    elif int(start_min) > 59:
        print(red + 'ERROR MESSAGE WANTED')
        sys.exit()


def book_event(event, creds, user_mail, event_id):

    maxAttendees = 1

    # First retrieve the event from the API.
    blue, red, green, yellow, pink, default = colors()
    service = build('calendar', 'v3', credentials=creds)
    
    event = service.events().get(calendarId='c_h4803008kmuddgc9i7m939lsuk@group.calendar.google.com',
                                 eventId=event_id,
                                 maxAttendees=maxAttendees
                                ).execute()

    if 'attendees' in event:
        print("slot already booked")
        sys.exit()

    event['attendees']=[{'email': user_mail}]
    

    updated_event = service.events().update(calendarId='c_h4803008kmuddgc9i7m939lsuk@group.calendar.google.com',
                                            eventId=event_id,
                                            body=event).execute()
    print(green+'ALERT: BOOKING MESSAGE WANTED')


def cancel_book(event, creds, user_mail, event_id):

    maxAttendees = 1
    blue, red, green, yellow, pink, default = colors()
    service = build('calendar', 'v3', credentials=creds)
    
    event = service.events().get(calendarId='c_h4803008kmuddgc9i7m939lsuk@group.calendar.google.com',
                                 eventId=event_id,
                                 maxAttendees=maxAttendees
                                ).execute()

    event['attendees']=[]
    updated_event = service.events().update(calendarId='c_h4803008kmuddgc9i7m939lsuk@group.calendar.google.com',
                                            eventId=event_id,
                                            body=event).execute()

    print(green+'ALERT: CANCELLED BOOKING MESSAGE WANTED')


def cancel_volunteer(event, creds, user_mail, event_id):

    maxAttendees = 1

    blue, red, green, yellow, pink, default = colors()
    service = build('calendar', 'v3', credentials=creds)

    event = service.events().get(calendarId='c_h4803008kmuddgc9i7m939lsuk@group.calendar.google.com',
                                 eventId=event_id,
                                 maxAttendees=maxAttendees
                                ).execute()
                                
    
    
    if event['creator']['email'] != user_mail:
        print(red + "You are not the owner of the slot")
        sys.exit()

    elif 'attendees' in event:
        print(red + 'The slot is already booked!')
        sys.exit()

    event['attendees']=[]

    updated_event = service.events().delete(calendarId='c_h4803008kmuddgc9i7m939lsuk@group.calendar.google.com',
                                            eventId=event_id).execute()

    print(green+'ALERT: CANCELLED VOLUNTEER MESSAGE WANTED')
    
# creds = authorize()
# service = build('calendar', 'v3', credentials=creds)
# events  = view_events()

# book_event(events, creds)

# TO DO TODAY XD
# sort users data ***
# start doing the command line ***
# booking a slot (service.events.update(PAR:)) 
# create access control rules for new users to the system[random.randint(1,len(alpha_num)) for x in range(5)]