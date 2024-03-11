# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


def reg_user(x, y, z):
    # - Check if the new password and confirmed password are the same.
    if y == z:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[x] = y
            
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


def add_task(w, x, y, z):
    # Finds the number for new task, based on existed number
    task_count = 0
    for t in task_list:
        task_count += 1
    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": w,
        "title": x,
        "description": y,
        "due_date": z,
        "assigned_date": curr_date,
        "completed": False,
        "number": str(task_count+1)
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No",
                t['number']
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


def view_all(x):
    # Loops through task list, prints it in an easy to read way
    for t in x:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


def view_mine(x):
    # Recounts tasks to account for any changes
    task_count = 0
    for t in task_list:
        task_count += 1
    # Iterates through task list and checks username, if same as current user, display task
    for t in task_list:
        if t['username'] == x:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Task Number: \t {t['number']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
    # Asks if view_specific is needed, and checks to ensure the input is valid
    while True:
        try:
            vm_menu = input("Enter the task number you wish to view or -1 to return to menu: ")
            if int(vm_menu) not in range(-1, (task_count+1)):
                raise ValueError
            elif int(vm_menu) == 0:
                raise ValueError
            # Stops users accessing tasks not assigned to them unless they are the admin
            elif int(vm_menu) != -1 and task_list[int(vm_menu)-1].get('username') != curr_user and curr_user != 'admin':
                raise ValueError
            break
        except (TypeError, ValueError):
            print("That is not a valid input, please try again")
    if vm_menu == str(-1):
        return
    else:
        view_specific(vm_menu)


def view_specific(x):
    # Iterates through task list, if task is correct number, return it, prompt input
    for t in task_list:
        if t['number'] == x:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Task Number: \t {t['number']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
            title = t['title']
    while True:
        vs_menu = input(''' Select one of the following below:
        e - Edit selected task
        c - Mark as completed
        m - Return to Menu                
        ''')
        # Asks user to confirm completion, updates value of 'completed' to true
        if vs_menu == "c":
            complete_confirm = input(f"Are you sure you want to mark task {title} as complete? (Y/N): ").lower()
            if complete_confirm == "n":
                pass
            elif complete_confirm == "y":
                for t in task_list:
                    if t['number'] == x:
                        task_list[int(x)-1].update({'completed': True})
                        with open("tasks.txt", "w") as task_file:
                            task_list_to_write = []
                            for t in task_list:
                                str_attrs = [
                                    t['username'],
                                    t['title'],
                                    t['description'],
                                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                    "Yes" if t['completed'] else "No",
                                    t['number']
                                ]
                                task_list_to_write.append(";".join(str_attrs))
                            task_file.write("\n".join(task_list_to_write))
                print("Task completed!")

        # Checks if the task is marked as completed before it can be edited
        elif vs_menu == "e":
            y = task_list[int(x)-1].get('completed')
            if y == True:
                print("You cannot edit completed tasks")
            else:
                # Asks what user wants to edit
                edit_what = input(''' Select one of the following below:
                u - Change the user the task is assigned to
                d - Change the due date
                m - Return to menu            
                ''').lower()
                if edit_what == "u":
                    while True:
                        # Checks if user assigned to task exists and updates username to match if true
                        new_assign = input("Who would you like to assign this task to? ")
                        if new_assign not in username_password.keys():
                            print("This user does not exist")
                        else:
                            task_list[int(x)-1].update({'username': new_assign})
                            with open("tasks.txt", "w") as task_file:
                                task_list_to_write = []
                                for t in task_list:
                                    str_attrs = [
                                        t['username'],
                                        t['title'],
                                        t['description'],
                                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                        "Yes" if t['completed'] else "No",
                                        t['number']
                                    ]
                                    task_list_to_write.append(";".join(str_attrs))
                                task_file.write("\n".join(task_list_to_write))
                        break
                    # Asks the user to input a new date, if valid, updates due date to match
                elif edit_what == "d":
                    while True:
                        try:
                            new_task_due_date = input("New due date of task (YYYY-MM-DD): ")
                            new_date_time = datetime.strptime(new_task_due_date, DATETIME_STRING_FORMAT)
                            task_list[int(x)-1].update({'due_date': new_date_time})
                            with open("tasks.txt", "w") as task_file:
                                task_list_to_write = []
                                for t in task_list:
                                    str_attrs = [
                                        t['username'],
                                        t['title'],
                                        t['description'],
                                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                        "Yes" if t['completed'] else "No",
                                        t['number']
                                    ]
                                    task_list_to_write.append(";".join(str_attrs))
                                task_file.write("\n".join(task_list_to_write))  
                            break
                        except ValueError:
                            print("Invalid datetime format. Please use the format specified")
                
                elif edit_what == "m":
                    break

                else:
                    print("That is not a valid input")

        elif vs_menu == "m":
            break   

        else:
            print("That is not a valid input")


# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}
    try:
        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        curr_t['number'] = task_components[6]
    except IndexError:
        curr_t['number'] = 1

    task_list.append(curr_t)



#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

task_count = 0
for t in task_list:
    task_count += 1

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    if curr_user == "admin":
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - Generate Report
    ds - Display statistics
    e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    ds - Display statistics
    e - Exit
    : ''').lower()

    if menu == 'r':
        '''Add a new user to the user.txt file'''
        # - Request input of a new username
        while True:
            new_username = input("New Username: ")
            if new_username in username_password.keys():
                print("User already exists, please try again")
            else:
                break

        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        reg_user(new_username, new_password, confirm_password)

    elif menu == 'a':
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        add_task(task_username, task_title, task_description, due_date_time)

    elif menu == 'va':
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''
        view_all(task_list)         

    elif menu == 'vm':
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''

        view_mine(curr_user)

    elif menu == 'gr' and curr_user == 'admin':
        '''If the user is an admin they can generate reports about number of users
            and tasks.'''
        # Updates task count in case of changes and defines variables
        task_count = 0
        for t in task_list:
            task_count += 1
        complete_tasks = 0
        incomplete_tasks = 0
        late_tasks = 0
        to_be_written = []
        curr_date = date.today()
        # Iterate through task list
        for n, t in enumerate(task_list):
            # Get state of compeleted and due date
            x = task_list[n].get('completed')
            y = task_list[n].get('due_date')
            if x == True:
                # Adds to complete count if complete is true
                complete_tasks += 1
            elif x == False and y.date() < curr_date:
                # Adds to late count if not complete and due date passed
                late_tasks += 1
            elif x == False:
                # Adds to incomplete count if complete false but due date not passed
                incomplete_tasks += 1
        
        # Tries to get a percentage of tasks, if zero tasks, sets percentage to 0
        try:
            incomplete_percent = (incomplete_tasks / task_count) * 100
        except ZeroDivisionError:
            incomplete_percent = 0
        try:
            late_percent = (late_tasks / task_count) * 100
        except ZeroDivisionError:
            late_percent = 0
        # Appends the data to the list and writes it
        to_be_written.append(f"Total number of tasks created and managed: {task_count}")
        to_be_written.append(f"Completed tasks: {complete_tasks}")
        to_be_written.append(f"Incomplete tasks: {incomplete_tasks}")
        to_be_written.append(f"Late Tasks: {late_tasks}")
        to_be_written.append(f"Percentage of tasks incomplete: {incomplete_percent}%")
        to_be_written.append(f"Percentage of tasks late: {late_percent}%")
        
        # Checks if file exists, writes data if true, creates and writes data if not
        while True:
            try:
                with open('task_overview.txt', 'w') as f:
                    for i in to_be_written:
                        f.write(i + "\n")
                break
            except (FileExistsError, FileNotFoundError):
                create = open('task_overview.txt', 'a')
                create.close()
        
        # Defines variables for overview
        to_be_written_user = []
        user_count = 0
        user_task_total = 0
        user_complete_tasks = 0
        user_incomplete_tasks = 0
        user_late_tasks = 0

        # Counts total users and appends the already known data
        for i in user_data:
            user_count += 1

        to_be_written_user.append(f"Total users registered: {user_count}")
        to_be_written_user.append(f"Total tasks generated: {task_count}")

        # Iterates through username password and gets each key (username)
        for i in username_password:
            user = i
            # Counts completed, incomplete and late tasks for each user
            for n, i in enumerate(task_list):
                if i['username'] == user:
                    user_task_total += 1
                    y = task_list[n].get('completed')
                    z = task_list[n].get('due_date')
                    if y == True:
                        user_complete_tasks += 1
                    elif y == False and z.date() < curr_date:
                        user_late_tasks += 1
                    elif y == False:
                        user_incomplete_tasks += 1
            # Tries to calculate percentages, if zero division error, sets percentage to 0
            try:
                user_task_total_percentage = (user_task_total / task_count) * 100
            except ZeroDivisionError:
                user_task_total_percentage = 0
            try:
                user_task_complete_percentage = (user_complete_tasks / user_task_total) * 100
            except ZeroDivisionError:
                user_task_complete_percentage = 0
            try:
                user_task_incomplete_percentage = (user_incomplete_tasks / user_task_total) * 100
            except ZeroDivisionError:
                user_task_incomplete_percentage = 0
            try:   
                user_task_late_percentage = (user_late_tasks / user_task_total) * 100
            except ZeroDivisionError:
                user_task_late_percentage = 0

            # Appends a formatted string with data for each user to a list
            to_be_appended = (f'''User: {user} \n
                Total tasks for user: {user_task_total} \n
                Percentage of overall total tasks: {user_task_total_percentage}% \n
                Percentage of tasks completed: {user_task_complete_percentage}% \n
                Percentage of tasks incomplete: {user_task_incomplete_percentage}% \n
                Percentage of tasks late: {user_task_late_percentage}% ''')
            to_be_written_user.append(to_be_appended + "\n\n")
            user_task_total = 0
            user_complete_tasks = 0
            user_incomplete_tasks = 0
            user_late_tasks = 0
        
        # Checks if file exists, writes data if true, creates and writes data if not
        while True:
            try:
                with open('user_overview.txt', 'w') as f:
                    for i in to_be_written_user:
                        f.write(i + "\n")
                break
            except (FileExistsError, FileNotFoundError):
                create = open('user_overview.txt', 'a')
                create.close()



    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")