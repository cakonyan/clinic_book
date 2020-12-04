from __future__ import print_function
import os
from datetime import datetime, time
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
import verify.verify_user_email as verify
import view_cal as view_cal

def get_volunteer_and_clinic_json():
    '''
    converts both json files into a variable
    returns that variables in a tuple
    '''

    student_json = verify.path_for_files("view_calendar_data_file_student.json")
    cclinc_jason = verify.path_for_files("view_calendar_data_file_clinic.json")

    with open("view_calendar_data_file_student.json", 'r') as json_file: 
        j_dict = json.load(json_file)
    with open("view_calendar_data_file_clinic.json", 'r') as json_file: 
        j_dict_c = json.load(json_file)
    
    return j_dict, j_dict_c


def load_token():
    '''
    Loads data from the token file and returns the service build
    '''

    token_pickle_path = verify.path_for_files('token.pickle')

    try:
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    except FileNotFoundError:
        print('Please Register')

    return build('calendar', 'v3', credentials=creds)


def process_json_to_list(cal_dict):
    '''
    Func takes a dict variable from a json file and converts it in to a 
    list if events

    returns the list of events
    '''
    event_list = []
    try:
        for i in cal_dict['events_list']:
            for key in i:
                event_list.append([ i[key]['date'], 
                                    i[key]['start'], 
                                    i[key]['end']])
    except:
        return []
    
    return event_list


def seven_day_list():
    '''
    creates a list of dates for the next seven days
    returns the list
    '''
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    seven_day = [today]
    for i in range(1,7):
        date = datetime.datetime.today() + datetime.timedelta(i)
        date = date.strftime('%Y-%m-%d')
        seven_day.append(date)

    return seven_day


def datetime_convert(date_str, time_str):
    '''
    converts str date in format YYYY-MM-DD to a datetime object
        returns datetime obj
    '''

    date_int = [int(i) for i in date_str.split('-')]
    time_int = [int(i) for i in time_str.split(':')]

    return datetime.datetime(date_int[0],date_int[1],date_int[2],time_int[0], time_int[1])

        
def volunteer_topics():
    '''
    This will display the topics at the school
    Volenteer will be allowed to choose a topic from a list
    after the topic has been chosen, topics will be displayed again
    they will have the choice of choosing anither topic or quit
    will print the list of topics for volunteer

    return the topic that the volunteer can assist with
    '''
    
    num_1 =     'HANGMAN'
    num_2 =     'PYRAMID'
    num_3 =     'PROBLEM - OUTLINE'
    num_4 =     'MASTERMIND'
    num_5 =     'TOY ROBOT 1 to 4'
    num_6 =     'WORD PROCESSING'
    num_7 =     'ACCOUNTING APP'
    num_8 =     'TOY ROBOT 5'
    num_9 =     'FIX THE BUGS'
    num_10 =    'GROUP PROJECT'

    topic_list = [num_1,num_2,num_3,num_4,num_5,num_6,num_7,num_8,num_9]

    print('Please choose from the following topics to assist with:\n')
    count = 1
    for i in topic_list:
        print(f'{count}.    {i}')
        count += 1
    while True:

        print('Please choose your topic according to the numbers listed above:')
        try:
            number = int(input())
        except ValueError:
            print('Invalid')
            continue

        if number > 9 or number < 1:
            print('Invalid num')
            continue

        break
    return topic_list[number-1]


def is_time_between(begin_time, end_time, check_time):
    '''
    function checks whether a particular time is between the begin_time and end_time
        All params are supposed to be a time(hh, mm)
        NB: Doesnt take overnight into consideration

        returns True if check_time is inbetween else False
    '''

    if check_time >= begin_time and check_time <= end_time:
        return True
    else:
        return False


def convert_to_time_object(time_str):
    '''
    coverts 'HH:MM' to time(HH,MM)
    returns time(HH"MM) object
    '''

    time_str = [int(i) for i in time_str.split(':')]

    return time(time_str[0],time_str[1])


def verify_token_exists():
    '''
    Returns true if token file is available
    else: False
    '''
    
    if os.path.exists('token.pickle'):
        return True
    else:
        return False


def check_availability(start_time, end_time):
    '''
    func will check if a time is available for opening a slot
        takes start_time and end_time which is a datetime object
        returns True if time is ok else False
    '''

    vol_cal, c_cal = get_volunteer_and_clinic_json()
    vol_cal = process_json_to_list(vol_cal)
    c_cal = process_json_to_list(c_cal)

    date = start_time.strftime('%Y-%m-%d')

    start_time = start_time.strftime('%H:%M')
    end_time = end_time.strftime('%H:%M')
    start_time = convert_to_time_object(start_time)
    end_time = convert_to_time_object(end_time)

    events = []
    for i in vol_cal:
        if date in i[0]:
            events.append([i[1],i[2]])
        
    for i in c_cal:
        if date in i[0]:
            events.append([i[1],i[2]])

    if events == None:
        return True

    event_time_obj = []
    for i in events:
        for y in i:
            event_time_obj.append(convert_to_time_object(y))


    if any(is_time_between(start_time,end_time, i) for i in event_time_obj):
        return False
    else:
        return True


def get_date():
    '''
    Promots user for a date format yyyy-mm-dd
    If date is entered incorrectly it will promt again until the date is
    yyyy-mm-dd
    '''

    print('Date formate must be yyyy-mm-dd')
    while True:
        date = input('Please enter date:')
        try:
            test_date = [int(i) for i in date.split('-')]
        except ValueError:
            print('Please enter the correct format\n')
            continue

        if len(test_date) != 3:
            print('Please enter the correct format\n')
            continue
            

        try:
            date_time = datetime.datetime(test_date[0], test_date[1], test_date[2])
        except ValueError:
            print('Date must be a real date\n')
            continue

        now = datetime.datetime.now()

        # if date_time < now:
        #     print('You cant open a slot in the past')
        #     continue
        
        print(f'The date entered is {date}\n')
        choose_again = input('Press enter to continue or "n" to choose another date: ')
        if choose_again == 'n':
            continue

        break
    
    return date


def get_time(date):
    '''
    Allows user to enter a start time for open slot
    End time will be 30 mins later
    returns start and end time in a str
    '''
    print('\nTime format should be mm:hh')
    while True:

        time = input('Please enter the start time: ')

        y, m, d = [int(i) for i in date.split('-')]
        try:
            h, mi = [int(i) for i in time.split(':')]
        except ValueError:
            print('Please enter the correct time format\n')
            continue


        # print(y,m,d,h,mi)
        try:
            start_time = datetime.datetime(y, m, d, h, mi)
        except ValueError:
            print('Please enter the correct time format\n')
            continue

        now = datetime.datetime.now()
        if start_time < now:
            print('You cannot enter a time in the past\n') 
            sys.exit()
        
        day_start = datetime.datetime(y,m,d, hour=6, minute=00)
        day_end = datetime.datetime(y, m, d, hour=17,minute=30)

        
        if start_time < day_start or start_time > day_end:
            print('Your time is outside the school hours\n')
            continue

        break

    end_time = start_time + datetime.timedelta(minutes=30)

    return [start_time.strftime('%H:%M'), end_time.strftime('%H:%M')] 


def creat_slot():
    '''
    We run the get_time, get_date and volunteer_topic
        return a date, start time, enn time and topic as description    
    '''
    
    main.check_login_time_and_if_registered()

    while True:
        date = get_date()
        time = get_time(date)
        topic = volunteer_topics()
        start_time = datetime_convert(date, time[0])
        end_time = datetime_convert(date, time[1])
        if  not check_availability(start_time, end_time):
            print('There is an appointment at that time')
            print('Please choose a different time')
            continue

        break
        

    slot =  {'slot': {
                        'date': date, 
                        'start': time[0], 
                        'end': time[1],
                        'topic': topic}}

    

    gcal_create_slot(slot)


def gcal_create_slot(slot):
    '''
    Func creates an event on gcal following the process of creat_slot
        param : dictionaries which has event details
        returns none
    '''
    date = slot['slot']['date']
    start = slot['slot']['start']
    end = slot['slot']['end']
    topic = slot['slot']['topic']
    service = load_token()
    print(date,start,end,topic)
    
    vol_id = verify.get_email(service)
    print(vol_id)
    cal_id = 'c_h4803008kmuddgc9i7m939lsuk@group.calendar.google.com'
    practice_cal = 'c_5ah2f5nil2m8jb0kue61cun5d4@group.calendar.google.com'

    event = {
        'summary': f'Code Clinic slot topic: {topic}',
        'description': f'You will be helped by {vol_id}',
    'start': {
        'dateTime': f'{date}T{start}:00+02:00',
        'timeZone': 'Africa/Johannesburg',
        },
    'end': {
        'dateTime': f'{date}T{end}:00+02:00',
        'timeZone': 'Africa/Johannesburg',
        },
    'attendees': [{'email' : vol_id}]
            }


    events = service.events().insert(   calendarId=practice_cal,
                                        maxAttendees=2, 
                                        body=event,
                                        sendNotifications=True
                                    ).execute()

    print('Slot created')
    print(f'Date        start   end     topic')
    print(f'{date}  {start}   {end}   {topic}')


def print_items_to_be_removed(events, cal_id, creator_email):
    '''
    Prints the google cal in a neat way and returns a list of cal entries
        Param 1 : (int) number of results that you want to display
        Param 2 : events = events_result(service, cla_id)
        Param 3 : calender that will be printed
    '''
    events_list = []
    print(f'These are your removable slots')
    if not events:
        print('None found')
        return {}
    i = 1
    print(f'#  Date         Start    End      Description')
    for event in events:
        try:
            att_num = len(event['attendees'])
        except KeyError:
            att_num = 0

        if event['creator']['email'] == creator_email and att_num < 2:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            
            date, start = start.split('T')
            start = start.split('+')[0]
            start = start[0:5]

            end = end.split('T')[1]
            end = end.split('+')[0]
            end = end[0:5]
            summary = event['summary']
            creator = event['creator']['email']
            print(f'{i}. {date}   {start}    {end}    {summary}    {creator}  ')
            events_list.append({f'event {i}' : 
                                            {'date' : date, 
                                            'start' : start, 
                                            'end' : end, 
                                            'description' : summary, 
                                            'id' : event['id'],
                                            'creator' : event['creator'] }})
            i += 1

    return events_list


def remove_slot():
    '''
    function removes a slot from a particular cal_id
        lets user choose the event they want to delete
    '''
    main.check_login_time_and_if_registered()
    service = load_token()

    cal_id = 'c_h4803008kmuddgc9i7m939lsuk@group.calendar.google.com'
    practice_cal = 'c_5ah2f5nil2m8jb0kue61cun5d4@group.calendar.google.com'

    events = view_cal.events_result(service, cal_id)
 
    creator_email = verify.get_email(service)

    event_list = print_items_to_be_removed(events, 'Slots opened', creator_email)

    
    print('Please enter the slot you want to remove:')
    try:
        number = int(input())
    except ValueError:
        print('Please enter a number from above')
        sys.exit()

    event_id = event_list[number-1][f'event {number}']['id']
    date = event_list[number-1][f'event {number}']['date']
    start = event_list[number-1][f'event {number}']['start']
    end = event_list[number-1][f'event {number}']['end']
    creator = event_list[number-1][f'event {number}']['creator']['email']
    summary = event_list[number-1][f'event {number}']['description']

    print()
    
    print('Event to be deleted\n')
    print(f'Date         Start    End      Description    Volunteer')
    print(f'{date}   {start}    {end}    {summary}    {creator}  \n')

    confirmation = input('Is this the slot you want to remove?(y/n)').lower()

    if confirmation == 'y':
        service.events().delete(calendarId=cal_id, 
                        eventId=event_id).execute()
        print('Slot removed')
        sys.exit()
    else:
        print('Slot not removed')
        print('OK')
    



if __name__ == "__main__":
    
    
    creat_slot()
    # remove_slot()