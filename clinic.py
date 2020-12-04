import sys
import os
import sync
from book import *
import json

from commands import help_page
from contextlib import contextmanager
import subprocess


def open_user_details():
    with open(".user_cred.txt", "r") as saved_creds:

        creds = saved_creds.read()
        user_email, password = creds.split(':')

        temp_storage = ''
        for char in user_email:
            if char != '' and char != ' ':
                temp_storage += char
        
        return temp_storage

def get_username():


    pass

def verify_token():
    if os.path.exists('token.pickle'):
        return True
    
    print("Please login!")
    sys.exit()


@contextmanager      # Suppress system output
def suppress_output():
    """
    - supress the function output
    - usage : with suppress_output():
    """
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


if __name__ == '__main__':

    blue, red, green, yellow, pink, default = sync.colors()

    if len(sys.argv) > 1 and sys.argv[1] == 'open':
        sync.open_events()
    
    elif len(sys.argv) > 1 and sys.argv[1] == 'update':
        sync.store_data()
        print(red+"LOCAL DATA UPDATED!")
        sys.exit()

    elif len(sys.argv) > 1 and sys.argv[1] == 'view':
        with open('.slots_data.json', 'r') as data_file:
            events = json.load(data_file)
            sync.sort_calendar_data(events)
            sys.exit()

    elif len(sys.argv) > 1 and sys.argv[1] == 'book':
        
        with open('.slots_data.json', 'r') as data_file:           
            
            if len(sys.argv) == 3:

                code = sys.argv[2]
                events = json.load(data_file)
                event = events[code]                # extracting event with unique_id
                event_id = event['id']
                
                creds = sync.authorize()
                user_mail = open_user_details()
                sync.book_event(events, creds, user_mail, event_id)
                sys.exit()
            else:
                print(red+"ERROR MESSAGE WANTED!")
                sys.exit()

    elif len(sys.argv) > 1 and sys.argv[1] == 'cancel_book':
        with open('.slots_data.json', 'r') as data_file:           
            
            if len(sys.argv) == 3:

                code = sys.argv[2]
                events = json.load(data_file)
                event = events[code]                # extracting event with unique_id
                event_id = event['id']
                
                creds = sync.authorize()
                user_mail = open_user_details()
                sync.cancel_book(event, creds, user_mail, event_id)
                sys.exit()
            else:
                print(red+"ERROR MESSAGE WANTED!")
                sys.exit()

    elif len(sys.argv) > 1 and sys.argv[1] == 'cancel_slot':
        with open('.slots_data.json', 'r') as data_file:           
            
            if len(sys.argv) == 3:

                code = sys.argv[2]
                events = json.load(data_file)
                event = events[code]                # extracting event with unique_id
                event_id = event['id']
                creds = sync.authorize()
                user_mail = open_user_details()

                sync.cancel_volunteer(event, creds, user_mail, event_id)
                sys.exit()
                
            else:
                print(red+"ERROR MESSAGE WANTED!")
                sys.exit()


    else:
        print(help_page.help_sheet())
        sys.exit()

    
    

    pass
