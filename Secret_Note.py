import datetime
from os import path
from os import listdir
from os import mkdir
from os import remove
import shutil

db_path = './SNDataBase/'
password_file = db_path+"SNPasswordInfo.txt"

menu ='''
    1. Register to Secret Note
    2. Login to Secret Note
    3. Retrieve Password
    4. Exit
    What do you want to do: '''

menu1 = '''
What do you want to do :
    1. Keep a secret
    2. View old secrets
    3. Delete a secret
    4. Delete profile
    5. Logout
'''

menu2 ='''
secret exists with same title.
    1. Do you want to add more to the same secret.
    2. Do you want to re-write the secret.
    Press other key to Cancel.
'''

def getdatetime():
    """getdate - This function will return current system date and time

    Returns:
        currenttime {str} -- return current time in []
    """
    currenttime = '['+str(datetime.datetime.now()).split('.')[0]+'] : '
    return currenttime

def changetimestamp(filepath):
    """changetimestamp - This function will change the 1st time stamp of the note

    Arguments:
        filepath {str} -- filename
    """
    with open(filepath, 'r+') as fd:
        content = fd.read()
        note = content.split(':',1)[1]
        currenttime = getdatetime()
        new_note = currenttime+note
        fd.write(new_note)
    pass

def check_in_file(username, password='', mode=''):
    """check-in-file - This function read and username and password from SNPasswordInfo file.
    depending on mode valuer it will do the following tasks:
    mode-------------task
    user             It will check if the user is existing user or not.
    password         It will check if password for that perticular user is correct or not.
    retrieve         It will print the password for that given user name


    Arguments:
        username {str} -- User provided username, which will get validated in this function.

    Keyword Arguments:
        password {str} -- User provided password for validation while login (default: {''})
        mode     {str} -- Depending on mode this function will perform below operations (default: {''})
                            mode-------------task
                            user             It will check if the user is existing user or not.
                            password         It will check if password for that perticular user is correct or not.
                            retrieve         It will print the password for that given user name

    Returns:
        {bool}  -- In success cases return True
                -- In failure cases return False
    """
    with open(password_file, 'rt') as fd:
        for line in fd:
            line = line.split('\n')[0].split(',')
            if mode == 'password' and line == [username,password]:
                return True
            if mode == 'user' and line[0] == username:
                return True
            if mode == 'retrieve' and line[0] == username:
                print('Your password : ',line[1])
                return True
        else:
            return False

def password_check(username):
    """password_check - This function will take password as input from user while login and send both username and password for validation.

    Arguments:
        username {str} -- user provided username.

    Returns:
        {bool} --   True - While login if username-password pair is correct.
                    False- If username-password pair is wrong.
    """
    password = input("Password: ")
    check_status = check_in_file(username, password, mode='password')
    return check_status

def create_dic(user):
    """create_dic - This function will create a directory for a user in side database folder.

    Arguments:
        user {str} -- This will be the name of the directory.

    Returns:
        {bool}  --  True  - If directory created successfully
                    False - If failed to create the directory
    """
    user = user.strip()
    if user != "":
        dir_path = db_path+user
        mkdir(dir_path)
        return True
    else:
        return False

def fileWrite(data, filename, mode):
    """fileWrite - It will write the data into the file named 'filename'

    Arguments:
        data     {str} -- data to be written in to the file
        filename {str} -- where the data will be written
        mode     {str} --   'w' - overwrite the old data and re-write the new data
                            'a' - append the new data after the old data.
    """
    with open(filename, mode) as fd:
        fd.write(data+'\n')

def new_password(username):
    """new_password - This will ask user to create password while registering as new user. and send both user and password to store.

    Arguments:
        username {str} -- User given username while registering as new user.

    Returns:
        [bool]  --  True - If password is created successfully
                    False - Failed to create proper password.
    """
    Password = input('Create New Password : ')
    try_count = 3
    while Password == "" and try_count > 0:
        Password = input("Password should contain something. Try again : ")
        try_count -= 1
    if try_count == 0 and Password == "":
        return False
    else:
        data = username+','+Password
        fileWrite(data, password_file, 'a')
        return True

def create_user(user, user_list=[]):
    """create_user - This will validate and ask user to create new username while registering as new user if 1st username input is invalid.

    Arguments:
        user {str} -- While registering, 1st username given by user

    Keyword Arguments:
        user_list {list} -- list of usernames already available (default: {[]})

    Returns:
        user {str} - new generated username
    """
    user = user.strip()
    if user_list:
        if (not user) or (user in user_list):
            user = input("username already used. Try another username: ").strip().upper()
            user = create_user(user, user_list)
    else:
        if not user :
            user = input("invalid. Try another username: ").strip().upper()
            user = create_user(user, user_list)
    return user

def select_user_or_create():
    """select_user_or_create - This function is responsible for taking the 1st input from user from the following options:
        -register
        -login
        -retrieve password
        -exit
        depending on the user input this will perform that operation.

    Returns:
        (verified_user,user) {tuple} -- verified_user - flag to check user authentication
                                        user - username given by user.
    """
    verified_user = False
    user = ''
    login_check = input(menu)
    if login_check == '1':
        print("\n====Register===")
        try:
            user_list = [d for d in listdir(db_path) if path.isdir(path.join(db_path, d))]
        except Exception:
            mkdir(db_path)
            user_list = [d for d in listdir(db_path) if path.isdir(path.join(db_path, d))]
        user = input("Enter username: ").strip().upper()
        user = create_user(user, user_list)
        verified_user = new_password(user)
        if not verified_user:
                print('Invalid password')
                verified_user, user = select_user_or_create()
        else:
            print(f'''
        ==Welcome {user} to Secret Note==\n
        ''')
    elif login_check == '2':
        print("\n====Login===")
        user = input("Enter username: ").strip().upper()
        if path.exists(password_file) and user != "":
            if check_in_file(user, mode = 'user'):
                verified_user = password_check(user)
                if not verified_user:
                    print('Invalid password')
                    verified_user, user = select_user_or_create()
                else:
                    print(f'''
        ==Welcome Back {user}==\n
        ''')
            else:
                print('Invalid username')
                verified_user, user = select_user_or_create()
        else:
            print('Invalid username')
            verified_user, user = select_user_or_create()
    elif login_check == '3':
        print("\n====Retrieve password===")
        user = input("Enter username: ").strip().upper()
        if path.exists(password_file) and user != "":
            if not check_in_file(user, mode='retrieve'):
                print('username not found\n')
        else:
            print("Username not found\n")
        retrieve_flag = input('Do you want to exit?\n press n/no to continue \n Any other key to exit(No):').strip().lower()
        if retrieve_flag in n_flags:
            verified_user, user = select_user_or_create()
    elif login_check == '4':
        print('Comeback again')
    else:
        print('Invalid input')
        verified_user, user = select_user_or_create()

    return (verified_user,user)

def keep_secrets(user):
    """keep_secrets - This will take input from user about the 'Title' and the 'Note' for a Secret. If given title is same as any old title user has to choose whether to overwrite/append/cancel the operation. after one successfull secret write user will deside whether to keep another secter or exit.

    Arguments:
        user {str} -- logedin user
    """
    while(True):
        filename = input('Title : ').strip()
        if filename == "":
            print("Title should content some characters. Try again")
            filename = input('Title : ').strip()
        if filename != "":
            filepath = db_path+user+'/'+filename+'.txt'
            currenttime = getdatetime()
            if path.exists(filepath):
                note_choice = input(menu2+'Enter your choice : ')
                if(note_choice == '1'):
                    note = input('Note : ').strip()
                    if note != "":
                        fileWrite(currenttime+note, filepath, 'a')
                        # changetimestamp(filepath)
                    print('Your secret is saved successfully\n')
                elif note_choice == '2':
                    note = input('Note : ')
                    if note != "":
                        fileWrite(currenttime+note, filepath, 'w')
                    print('Your secret is saved successfully\n')
                else:
                    print("Canceled successfully.")
            else:
                note = input('Note : ').strip()
                if note != "":
                    fileWrite(currenttime+note, filepath, 'w+')
                else:
                    fileWrite(note, filepath, 'w+')
                print('Your secret is saved successfully\n')
        else:
            print("Invalid Title")
            break
        cont_flag = input('Do you want to keep another secret?(no)').strip().lower()
        if cont_flag in n_flags:
            break
        elif cont_flag not in y_flags:
            print('Invalid parameter')
            break

def show_sectets(user):
    """show_sectets - This will show user all the sectet titles. and prompt user if user want to view any perticular secret.

    Arguments:
        user {str} -- logedin username
    """
    file_list = [d for d in listdir(db_path + user)]
    if len(file_list) != 0:
        print('=================Your secrets===================')
        for notes in file_list:
            print(notes.split('.')[0])
        print('=================================================')

        open_secret = input('Do you want to open any secret:(no):').lower()
        if open_secret in y_flags:
            secret_name = input('Enter the secret name: ')
            try:
                with open(db_path + user + '/' + secret_name + '.txt') as fd:
                    print('\n<**> Here is your secrect about \"'+secret_name+'\"<**> \n')
                    print(fd.read())
            except Exception:
                print("This secrect is not shared with me")
        elif open_secret not in n_flags:
            print('Invalid parameter')
    else:
        print("No secrets found")

def delete_secret(user):
    """delete_secret - This will prompt all the secrets that perticulat user have and ask user to input the sectet name which user want to delete.

    Arguments:
        user {str} -- username of the logged profile.
    """
    file_list = [d for d in listdir(db_path + user)]
    if len(file_list) != 0:
        print('=================Your secrets===================')
        for notes in file_list:
            print(notes.split('.')[0])
        print('=================================================')
        secret_to_delete = input('Which Secret do you want to delete : ')
        if path.exists(db_path + user + '/' + secret_to_delete + '.txt'):
            delete_confermation = input("Do you really want to delete (No) : ").strip().lower()
            if delete_confermation in y_flags:
                remove(db_path + user + '/' + secret_to_delete + '.txt')
            elif delete_confermation not in n_flags:
                print("Invalid parameter\nBut Your Secret is safe with me\n")
        else:
            print("This secret is not shared with me")
    else:
        print("No secrets found")

def delete_profile(user):
    """delete_profile - This function will delete the profile for that perticular user, including password registry.

    Arguments:
        user {str} -- username of the profile to be deleted.

    Returns:
        {bool} --   True  - If profile got deleted successfully
                    False - If profile is not deleted.
    """
    profile_flag = input('Do you really want to delete the profile(No):').strip().lower()
    if profile_flag in y_flags:
        shutil.rmtree(db_path + user)
        with open(password_file ,"r+") as f:
            new_f = f.readlines()
            f.seek(0)
            for line in new_f:
                if user not in line:
                    f.write(line)
            f.truncate()
        return True
    elif profile_flag not in n_flags:
        print('Invalid input')
    return False

def run():
    """run - This is the starting point.
    """
    verified_user, username = select_user_or_create()
    if verified_user:
        try:
            create_dic(username)
        except Exception:
            pass
        while(True):
            user_choice = input(menu1+'Your choice : ')
            if user_choice == '1':
                keep_secrets(username)
            elif user_choice == '2':
                show_sectets(username)
            elif user_choice == '3':
                delete_secret(username)
            elif user_choice == '4':
                if delete_profile(username):
                    print('Profile deleted successfully')
                    break
            elif user_choice == '5':
                logout_flag = input("Do you really want to log out (no):").strip().lower()
                if logout_flag in y_flags:
                    print('**See you next time**')
                    run()
                    break
                elif logout_flag not in n_flags:
                    print('Invalid parameter')
            else:
                print('Invalid input')
    return

if __name__ == "__main__":
    y_flags = ['y','yes']
    n_flags = ['n','no','']
    run()
