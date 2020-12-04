#!/usr/bin/python3
from __future__ import print_function
# import main
import os
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import subprocess
from io import StringIO
import sys
import volunteer as vol

def captured_io():
    ''' suppresses output
    
        returns text_capture'''

    text_capture = StringIO()
    sys.stdout = text_capture

    return text_capture
    

def convert_time_and_date(events):
    '''
    #Getting date and time of the calender
    '''
    
    date_time = events[0]['start']['dateTime']
    print(date_time)

    date_time = date_time.split('T')
    date, time = date_time[0:]
    time = time.split('+')[0]

    return date_time


def get_email(service):
    '''
    Function returns the email that the calender belongs to
    Param: service = build('calendar', 'v3', credentials=creds)
    '''
    service = vol.load_token()
    email_id = service.calendarList().get(calendarId='primary').execute()

    return email_id['id']


def get_username_from_email(email_id):
    '''
    This function takes an email address(str) and returns the str before the @
    '''

    return email_id.split('@')[0]


def check_if_user_wtc(email_id):
    '''
    Will check is the google auth email is a WTC email
        Param 1 : str email
        Returns bool
    '''

    wtc_email = '@student.wethinkcode.co.za'
    if wtc_email in email_id:
        print('\n')
        print(f'Welcome {get_username_from_email(email_id)}')
        print('\n')
        return True
    
    else:
        print('Your email isnt a WTC email')
        print('You will be required to login again')
        os.system('rm token.pickle')
        stall = input('To try again please press enter, to quit press "q" and enter: ')
        if stall != '':
            print('Goodbye')
            sys.exit()
        return False


def path_for_files(file_name):
    '''
    maps out the path of a file to make sure that file is found by the function
        Param : str file name
        returns joined path
    '''

    this_folder = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(this_folder, file_name)


def google_api_and_data_file(user_name):
    """
    Runs the Google Calender API
    Verifies if the login provided corresponds with the email
    Param 1 : user_name is the login username provided in main.py
    returns the user email
    """
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    # this_folder = os.path.dirname(os.path.abspath(__file__))
    # cred_json = os.path.join(this_folder, 'credentials_quick.json')

    cred_json = path_for_files('client_id.json')
    print(cred_json)

    print('Welcome to your google calender service')
    print('You will be required to verify you WTC email')
    continue_or_quit = input('To continue press enter or type "q" to quit: ')

    if continue_or_quit != '':
            print('Goodbye')
            sys.exit()

    while True:
        creds =None
        if os.path.exists('token.pickle'):
            first_time_login = False
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)


        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            first_time_login = True
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # text_capture = captured_io()
                flow = InstalledAppFlow.from_client_secrets_file(
                    cred_json, SCOPES)
                creds = flow.run_local_server(port=0)
                # sys.__stdout__ = text_capture

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        # Building the resource Calendar
        service = build('calendar', 'v3', credentials=creds)
        email_id = get_email(service)
        if user_name == get_username_from_email(email_id) and check_if_user_wtc(email_id):
            break
        else:
            print('\n\nPlease verify your email according to your login')
            stall = input("If you want to register again, type q to quit, otherwise press enter:").lower()
            os.system('rm token.pickle')
            if stall == 'q':
                print('Please run the registration again')
                sys.exit()

    # print(first_time_login)
    # if first_time_login:
    #     return service

    print('Your account has been verified')


if __name__ == '__main__':

    google_api_and_data_file('mmehloma')