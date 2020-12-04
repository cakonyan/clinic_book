import os


file_name = '.usernames.txt'

def path_for_files(file_name):
    '''
    maps out the path of a file to make sure that file is found by the function
        Param : str file name
        returns joined path
    '''

    this_folder = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(this_folder, file_name)


def read_file(file_name):
    '''
    Reads the file and returns it as a list
    '''

    file_name = path_for_files(file_name)
    
    file = open(file_name, 'r')
    files = file.read()
    files = sort_username_file(files)
    file.close()
    return files


def sort_username_file(files):
    '''
    Function will sort the usernames in a file into a list
    param: takes read file
    returns a list of usernames
    '''

    file_list = files.split(' ')
    file_list = [x for x in file_list if x != '']
    with_new_line = [x for x in file_list if "\n" in x]
    file_list = [x for x in file_list if "\n" not in x]

    user = []

    for username in with_new_line:
        username = username.split('\n')
        username = [x for x in username if x != '']
        user.append(username[0])
                
    file_list = file_list + user 
    file_list = sorted(file_list)
    file_list = file_list[2:]
    return file_list
