import sys
import datetime
import json
import getpass
import subprocess
from user_names import usernames
import verify.verify_user_email as verify
import os
import volunteer as vol
import view_cal

this_folder = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(this_folder, 'user_names/.usernames.txt')

def colors():
    
    blue = "\033[1;34;10m"
    red = "\033[1;31;10m"
    green = "\033[1;32;10m"
    yellow = "\033[1;33;10m"
    pink = "\033[1;35;10m"

    return blue, red, green, yellow, pink 


def user_credentials(file_name):
    
    """
    - Takes user's Google details
    - student email and password
    - verifies the user credentials
    - if incorrect, it prints a message
    """

    blue, red, green, yellow, pink = colors()

    while True:

        user_email = input("Student email: ")    # check ValueError

        try:

            user_name, verification = user_email.split('@')
            if verify_credentials(user_name, verification, file_name):
                print(red + "Invalid user credentials!")    
                sys.exit()

            break
        except ValueError:
            print(red + "Invalid user credentials!")
            sys.exit()
    
    check_user_cred(user_email)

    verify.google_api_and_data_file(user_name)
    
    print()

    user_password = getpass.getpass("Password:"
        +blue + "*"
        +yellow + "*"
        +red + "*"
        +green + "*"
        +yellow + "*"
        +pink + "*"
        +red + "*"
        )
    
    credentials = [
                    {'user_cred':[  {'user_name' : user_name}, 
                                    {'user_email' : user_email}, 
                                    {'user_password' : user_password}, 
                                    {'verification' : verification}]
                }]

    # credentials = [{user_name: {user_email : user_password} }, verification]
    
    save_users(user_email, user_password)
    return credentials


def save_users(user_email, user_password):
    """
    Take usermail and password as arguments 
    save the user email and password to a text file
    """

    with open(".user_cred.txt", "r+") as saved_creds:
        saved_creds.write(f'{user_email} :{user_password}\n')
        saved_creds.close()

    creds = {'email' : user_email,
             'password' : user_password}
    return creds

   
def verify_credentials(user_name, verification, file_name):
    """
    - Returns user_credentials() if credentials are invalid
    - Returns False if credentials valid
    """


    user_names_list = usernames.read_file(file_name)
    if verification != 'student.wethinkcode.co.za' and verification != 'wethinkcode.co.za':
        return True


    if user_name not in user_names_list:
        return True

    return False


def check_user_cred(user_email):
    '''
    checks if email details are registered already
    returns True if details exist else False
    '''
    with open(".user_cred.txt", "r+") as cred_file:
        files = cred_file.read()
        cred_file.close()
        
    if user_email in files:
        print("Email is already registered, please login or type help")
        sys.exit()


def path_for_files(file_name):
    '''
    maps out the path of a file to make sure that file is found by the function
        Param : str file name
        returns joined path
    '''

    this_folder = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(this_folder, file_name)


def open_user_cred():
    """
    Function opens user credentials file
    """
    while True:
        try:
            with open(".user_cred.txt", "r+") as cred_file:
                user_file = cred_file.readline()
                cred_file.close()
                break
        # print(user_file)
        except FileNotFoundError:
            os.system('touch .user_cred.txt')
            continue
    
    return user_file


def user_reg_check():
    '''
    checks if user is registered already
    '''

    user_file = open_user_cred()

    if len(user_file) != 0:
        print('User already registered')
        sys.exit()


def user_register():
    '''
    executes the login
    returns services from the google API
    '''

    print('Welcome to Code Clinic register\n')
  
    if os.path.exists('.user_cred.txt'):
        pass
    else:
        os.system('touch .user_cred.txt')

    user_reg_check()

    cred = user_credentials('.usernames.txt')
    # print(cred)
    # user_name = cred[0]['user_cred'][0]['user_name']
    
    print('Your account has been Registered')


def write_json(file_name, content):
    '''
    Writes info to the json file
    param1: file_name of json file
    param2: the content that has to be written to the json
    '''

    with open(file_name, "w") as f:
        json.dump(content, f, indent=1)


def open_json_file(file_name):
    '''
    Func opens json file and returns its contents
    '''
    with open(file_name, 'r') as json_file: 
        json_content = json.load(json_file)

    return json_content


def check_login_time_and_if_registered():
    '''
    function will check the login time is not past three hours and if user is registered

        If login time is beyond 3 hours and if user isnt registered, program will break
    '''
    try: 
        user_cred = open_user_cred()
    except FileNotFoundError:
        print('Please Register')
        sys.exit()

    if len(user_cred) == 0:
        print('Please Register')
        sys.exit()

    if not os.path.exists('token.pickle'):
        print('Please Register')
        os.system('rm .user_cred.txt')
        sys.exit()

    login_time = open_json_file('user_login_time.json')

    # print(login_time)

    date, time = login_time.split(' ')
    time = time[0:5]

    date_time = vol.datetime_convert(date, time)

    now = datetime.datetime.now()

    if now-date_time > datetime.timedelta(hours=3):
        print('3 hours has passed since your last login')
        print('Please login')
        sys.exit()
    

def user_login():
    '''
    Will run the login sequence
    '''
    if os.path.exists('.user_cred.txt') and os.path.exists('token.pickle'):
        pass
    else:
        print('Please Register')
        sys.exit()


    blue, red, green, yellow, pink = colors()

    user_password = getpass.getpass("Password:"
        +blue + "*"
        +yellow + "*"
        +red + "*"
        +green + "*"
        +yellow + "*"
        +pink + "*"
        +red + "*"
    )
    
    user_file = open_user_cred()
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')

    if user_password in user_file:
        print('Login ok')
        print(f'login time {now_str}')
        write_json('user_login_time.json', now_str)
    else:
        print('invalid login')


def help_command():
    '''
    Displays the commands that are needed to run the clinic
    '''

    print("""code clinic usage

clinic <use>

These are the code clinic commands that can be used in various situations:     

registration and login

    register        Allows you to register(Register first)
    login           To login(You will be loged out every 3 hours)

To volunteer

    
                """)

if __name__ == "__main__":
    

    if len(sys.argv) > 1 and sys.argv[1] == 'register':
        user_register()
    
    elif len(sys.argv) > 1 and sys.argv[1] == 'login':
        user_login()

    elif len(sys.argv) > 1 and sys.argv[1] == '-v':
        view_cal.cal_view()
    
    elif len(sys.argv) > 1 and sys.argv[1] == '-o':
        vol.creat_slot()

    elif len(sys.argv) > 1 and sys.argv[1] == '-rs':
        vol.remove_slot()
    
    elif len(sys.argv) > 1 and sys.argv[1] == '-b':
        pass

    else:
        help_command()

        