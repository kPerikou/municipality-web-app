from django.shortcuts import render, redirect
from numpy.core import double

from .models import Employee, Direction, Department, DeptDirector, \
    Activity, Task, Notification, Project, Office, OfficeClerk, Comment
from passlib.hash import pbkdf2_sha256


# Returns the password of the user if the username exists
def authenticate_employee(username, password):
    try:
        employee = Employee.objects.get(username=username)
        if employee is not None:
            return pbkdf2_sha256.verify(password, employee.password)
        else:
            return False
    except Employee.DoesNotExist:
        return False


# The list of employees that is appearing on create task depending of the user's direction or department
def setTaskEmployees(employeeId):
    employee = Employee.objects.get(username=employeeId)
    if hasattr(employee, 'deptdirector'):
        deptDirectorEmp = DeptDirector.objects.get(username=employeeId)
        officeClerks = OfficeClerk.objects.filter(department=deptDirectorEmp.department)
        return officeClerks
    else:
        directorEmp = employee
        deptDirectors1 = DeptDirector.objects.filter(direction=directorEmp.direction)
        deptDirectors2 = OfficeClerk.objects.filter(direction=directorEmp.direction)
        deptdirectors = list(deptDirectors1) + list(deptDirectors2)
        return deptdirectors


# Checks if the username already is being used by another user
def checkUsername(username):
    if Employee.objects.filter(username=username).exists():
        return True
    else:
        return False

# Registers a director of a direction
def register_director(request):
    directions = {'directions_list': Direction.objects.all()}
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        username = request.POST['username']
        password = request.POST['password']
        direction = request.POST['direction']
        email = request.POST['email']

        if not name or not surname or not username or not password or not direction or not email:
            directions = {'directions_list': Direction.objects.all(),
                          'messageUserExists': 'Παρακαλώ συμπληρώστε όλα τα πεδία.'}
            return render(request, 'activities/register_Director.html', directions)
        else:
            encrypted_password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)
            exists = checkUsername(username)
            if not exists:

                Employee.objects.create(
                    name=name,
                    surname=surname,
                    username=username,
                    password=encrypted_password,
                    direction=direction,
                    email=email
                )
                return redirect('login')
            else:
                directions = {'directions_list': Direction.objects.all(), 'messageUserExists': 'To όνομα χρήστη που πληκτρολογήσατε υπάρχει ήδη. Παρακαλώ προσπαθήστε ξανά.'}
                return render(request, 'activities/register_Director.html', directions)
    else:
        return render(request, 'activities/register_Director.html', directions)

# Registers a director of a department
def register_deptDirector(request):
    deptdirector = {'directions_list': Direction.objects.all(), 'departments_list': Department.objects.all()}
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        username = request.POST['username']
        password = request.POST['password']
        direction = request.POST['direction']
        department = request.POST['department']
        email = request.POST['email']

        if not name or not surname or not username or not password or not direction or not email or not department:
            deptdirector = {'directions_list': Direction.objects.all(), 'departments_list': Department.objects.all(),
                            'messageUserExists': 'Παρακαλώ συμπληρώστε όλα τα πεδία.'}
            return render(request, 'activities/register_deptDirector.html', deptdirector)
        else:
            encrypted_password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)
            exists = checkUsername(username)
            if not exists:
                DeptDirector.objects.create(
                    name=name,
                    surname=surname,
                    username=username,
                    password=encrypted_password,
                    direction=direction,
                    department=department,
                    email=email
                )
                return redirect('login')
            else:
                deptdirector = {'directions_list': Direction.objects.all(), 'departments_list': Department.objects.all(),
                                'messageUserExists': 'To όνομα χρήστη που πληκτρολογήσατε υπάρχει ήδη. Παρακαλώ προσπαθήστε ξανά.'}
                return render(request, 'activities/register_deptDirector.html', deptdirector)

    else:
        return render(request, 'activities/register_deptDirector.html', deptdirector)

# Registers an office clerk
def register_officeClerk(request):
    officeClerk = {'directions_list': Direction.objects.all(), 'departments_list': Department.objects.all(),
                   'offices_list': Office.objects.all()}
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        username = request.POST['username']
        password = request.POST['password']
        direction = request.POST['direction']
        department = request.POST['department']
        office = request.POST['office']
        email = request.POST['email']

        if not name or not surname or not username or not password or not direction or not email or not department or not office:
            officeClerk = {'directions_list': Direction.objects.all(), 'departments_list': Department.objects.all(),
                           'offices_list': Office.objects.all(),
                           'messageUserExists': 'Παρακαλώ συμπληρώστε όλα τα πεδία.'}
            return render(request, 'activities/register_OfficeClerk.html', officeClerk)
        else:
            encrypted_password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)
            exists = checkUsername(username)
            if not exists:
                OfficeClerk.objects.create(
                    name=name,
                    surname=surname,
                    username=username,
                    password=encrypted_password,
                    direction=direction,
                    department=department,
                    office=office,
                    email=email
                )
                return redirect('login')
            else:
                officeClerk = {'directions_list': Direction.objects.all(), 'departments_list': Department.objects.all(),
                           'offices_list': Office.objects.all(), 'messageUserExists': 'To όνομα χρήστη που πληκτρολογήσατε υπάρχει ήδη. Παρακαλώ προσπαθήστε ξανά.'}
                return render(request, 'activities/register_OfficeClerk.html', officeClerk)
    else:
        return render(request, 'activities/register_OfficeClerk.html', officeClerk)

# Checks if the user is an office clerk, a director of a department or a director of a direction
def checkUserType(user):
    if not hasattr(user, 'officeclerk'):
        if not hasattr(user, 'deptdirector'):
            return 'director'
        else:
            return 'deptdirector'
    else:
        return 'officeclerk'

# Signs in the user (handles the login process)
def login(request, **kwargs):
    if request.session.has_key('errorMessage'):
        message = request.session['errorMessage']
        del request.session['errorMessage']
        return render(request, 'activities/login.html', {'message': message})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            return render(request, 'activities/login.html',
                          {'message': 'Παρακαλώ συμπληρώστε όλα τα πεδία.'})
        else:
            user = authenticate_employee(username=username, password=password)
            if user is not False:
                employee = Employee.objects.get(username=username)
                request.session['user'] = employee.username
                userType = checkUserType(employee)
                if userType == 'director':
                    return redirect('home')
                else:
                    return redirect('myactivities')
            else:
                return render(request, 'activities/login.html', {'message': 'Λανθασμένο όνομα χρήστη ή κωδικός πρόσβασης. Παρακαλώ προσπαθήστε ξανά.'})
    else:
        return render(request, 'activities/login.html')

# Signs out the user
def logout(request):
    if request.session.has_key('user'):
        del request.session['user']
        return render(request, 'activities/logout.html')
    else:
        return redirect('login')

# Shows user's info
def info(request):
    if request.session.has_key('user'):
        user = Employee.objects.get(username=request.session['user'])
        userType = checkUserType(user)
        notShownNotifications = Notification.objects.filter(isShown=False, receiverId=request.session['user'])
        notCompletedTasks = Task.objects.filter(receiverId=request.session['user'], complete=False, approved=False)
        if userType == 'deptdirector':
            user = DeptDirector.objects.get(username=request.session['user'])
        elif userType == 'officeclerk':
            user = OfficeClerk.objects.get(username=request.session['user'])
        direction = Direction.objects.all()
        department = Department.objects.all()
        office = Office.objects.all()
        return render(request, 'activities/info.html', {'user': Employee.objects.get(username=request.session['user']), 'userinfo': user, 'usertype': userType, 'navbar': 'info',
                                                        'notShownNotifications': notShownNotifications, 'notCompletedTasks': notCompletedTasks,
                                                        'directions': direction, 'departments': department, 'offices': office})
    else:
        request.session['errorMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα. Παρακαλώ συνδεθείτε.'
        return redirect('login')

# Shows the homepage of the user with his/her tasks if the user is an office clerk,
# and with the assigned activities (projects or tasks) if the user is a director
def homepage_view(request):
    if request.session.has_key('user'):
        user = Employee.objects.get(username=request.session['user'])
        userType = checkUserType(user)
        if userType != 'officeclerk':
            allApprovedTasks = Task.objects.filter(approved=True, senderId=request.session['user']).values_list('activityId', flat=True)
            allTasks = Task.objects.filter(senderId=request.session['user'], projectId=0).values_list('activityId', flat=True)
            allProjects = Project.objects.filter(senderId=request.session['user']).values_list('activityId', flat=True)
            notShownNotifications = Notification.objects.filter(isShown=False, receiverId=request.session['user'])
            notCompletedTasks = Task.objects.filter(receiverId=request.session['user'], complete=False, approved=False)
            sentActivities = {'activities_list': Activity.objects.filter(senderId=request.session['user']).order_by('deadline'),
                          'approvedtasks': allApprovedTasks, 'tasks': allTasks, 'projects': allProjects,
                          'user': user, 'usertype': userType, 'navbar': 'sentactivities', 'notShownNotifications': notShownNotifications,
                              'notCompletedTasks': notCompletedTasks}
            if request.session.has_key('noAccessMessage'):
                noaccessmessage = request.session['noAccessMessage']
                del request.session['noAccessMessage']
                sentActivities = {'activities_list': Activity.objects.filter(senderId=request.session['user']),
                              'approvedtasks': allApprovedTasks, 'tasks': allTasks, 'projects': allProjects,
                              'user': user, 'usertype': userType, 'navbar': 'sentactivities',
                              'notShownNotifications': notShownNotifications,'notCompletedTasks': notCompletedTasks,
                            'noAccessMessage': noaccessmessage}
                return render(request, 'activities/home.html', sentActivities)
            else:
                return render(request, 'activities/home.html', sentActivities)
        else:
            request.session['noAccessMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα.'
            return redirect('myactivities')
    else:
        request.session['errorMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα. Παρακαλώ συνδεθείτε.'
        return redirect('login')

# Shows the activities assigned by the user
def myactivities(request):
    if request.session.has_key('user'):
        user = Employee.objects.get(username=request.session['user'])
        userType = checkUserType(user)
        if userType != 'director':
            emps = Employee.objects.all()
            notShownNotifications = Notification.objects.filter(isShown=False, receiverId=request.session['user'])
            myActivities = {'myactivities_list': Task.objects.filter(receiverId=request.session['user'],approved=False).order_by('deadline'),
                        'emps': emps, 'user': user, 'usertype': userType, 'navbar': 'myactivities',
                        'notShownNotifications': notShownNotifications}
            if request.session.has_key('noAccessMessage'):
                noaccessmessage = request.session['noAccessMessage']
                del request.session['noAccessMessage']
                myActivities = {'myactivities_list': Task.objects.filter(receiverId=request.session['user'],
                                                                         approved=False).order_by('deadline'),
                                'emps': emps, 'user': user, 'usertype': userType, 'navbar': 'myactivities',
                                'notShownNotifications': notShownNotifications, 'noAccessMessage': noaccessmessage}
                return render(request, 'activities/myactivities.html', myActivities)
            else:
                return render(request, 'activities/myactivities.html', myActivities)
        else:
            request.session['noAccessMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα.'
            return redirect('home')
    else:
        request.session['errorMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα. Παρακαλώ συνδεθείτε.'
        return redirect('login')

# Creates an activity (project)
def create_activity(request):
    if request.session.has_key('user'):
        user = Employee.objects.get(username=request.session['user'])
        userType = checkUserType(user)
        if userType != 'officeclerk':
            notShownNotifications = Notification.objects.filter(isShown=False, receiverId=request.session['user'])
            notCompletedTasks = Task.objects.filter(receiverId=request.session['user'], complete=False, approved=False)
            return render(request, 'activities/create_activity.html', {'user': user, 'usertype': userType,
                                                                       'navbar': 'createactivity',
                                                                       'notShownNotifications': notShownNotifications,
                                                                       'notCompletedTasks': notCompletedTasks})
        else:
            request.session['noAccessMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα.'
            return redirect('myactivities')
    else:
        request.session['errorMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα. Παρακαλώ συνδεθείτε.'
        return redirect('login')

# Creates a task
def create_task(request):
    if request.session.has_key('user'):
        user = Employee.objects.get(username=request.session['user'])
        userType = checkUserType(user)
        if userType != 'officeclerk':
            notShownNotifications = Notification.objects.filter(isShown=False, receiverId=request.session['user'])
            notCompletedTasks = Task.objects.filter(receiverId=request.session['user'], complete=False, approved=False)
            employees = {'employees_list': setTaskEmployees(user.username), 'user': user, 'usertype': userType,
                         'navbar': 'createactivity', 'notShownNotifications': notShownNotifications,
                         'notCompletedTasks': notCompletedTasks}
            if request.method == 'POST':
                activityId = Activity.objects.count() + 1
                title = request.POST['title']
                description = request.POST['description']
                deadline = request.POST['date']
                senderId = request.session['user']
                receiverId = request.POST['employee_department']

                if not title or not deadline or not receiverId:
                    employees = {'employees_list': setTaskEmployees(user.username), 'user': user, 'usertype': userType,
                             'navbar': 'createactivity', 'notShownNotifications': notShownNotifications,
                                 'message': 'Παρακαλώ συμπληρώστε τα πεδία: Τίτλο, Προθεσμία, Υπάλληλο',
                                 'notCompletedTasks':notCompletedTasks}
                    return render(request,'activities/create_task.html', employees)
                else:

                    approved = False
                    complete = False
                    projectId = 0
                    Task.objects.create(
                        activityId=activityId,
                        title=title,
                        description=description,
                        deadline=deadline,
                        complete=complete,
                        senderId=senderId,
                        receiverId=receiverId,
                        projectId=projectId,
                        approved=approved
                    )

                    Notification.objects.create(
                        notId=Notification.objects.count() + 1,
                        message='Ο χρήστης ' + senderId + ' σας ανέθεσε την αρμοδιότητα ' + title,
                        activityId=activityId,
                        receiverId=receiverId,
                    )
                    return redirect('home')
            else:
                return render(request, 'activities/create_task.html', employees)
        else:
            request.session['noAccessMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα.'
            return redirect('myactivities')
    else:
        request.session['errorMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα. Παρακαλώ συνδεθείτε.'
        return redirect('login')

# Shows user's notifications
def notifications(request):
    if request.session.has_key('user'):
        user = Employee.objects.get(username=request.session['user'])
        userType = checkUserType(user)
        notCompletedTasks = Task.objects.filter(receiverId=request.session['user'], complete=False, approved=False)
        notificationsList = {'notifications_list': Notification.objects.filter(receiverId=request.session['user']).order_by('-notDate'),
                             'user': user, 'usertype': userType, 'navbar': 'notifications',
                             'notCompletedTasks': notCompletedTasks}
        return render(request, 'activities/notifications.html', notificationsList)
    else:
        request.session['errorMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα. Παρακαλώ συνδεθείτε.'
        return redirect('login')

# Checks if an activity is a project or a single task
def isProject(activityid):
    activity = Activity.objects.get(activityId=activityid)
    if hasattr(activity, 'project'):
        return True
    else:
        return False


def getProjectTasksByProjectId(activityid):
    projectTasks = []
    allTasks = Task.objects.all()
    for task in allTasks:
        if str(task.projectId) == str(activityid):
            projectTasks.append(task)

    return projectTasks


def getCompletedTasks(activityid):
    tasksOfProject = getProjectTasksByProjectId(activityid)
    count = 0
    for t in tasksOfProject:
        if t.complete:
            count = count + 1
    return count

# Calculates the progress of a project (based on the completed tasks)
def percentageCalculator(size, numberCompletedTasks):
    return ((double) (100 / size)) * numberCompletedTasks


def getProjectByTask(taskid):
    task = Task.objects.get(activityId=taskid)
    if task.projectId != 0:
        project = Project.objects.get(activityId=task.projectId)
    else:
        project = None
    return project

# Shows an activity's details
def show_activity(request, activity_id=0):
    if request.session.has_key('user'):
        user = Employee.objects.get(username=request.session['user'])
        userType = checkUserType(user)
        try:
            act = Activity.objects.get(activityId=activity_id)
            notShownNotifications = Notification.objects.filter(isShown=False, receiverId=request.session['user'])
            notCompletedTasks = Task.objects.filter(receiverId=request.session['user'], complete=False, approved=False)

            if request.method == 'GET':
                isproject = isProject(activity_id)
                if isproject:
                    activity = Project.objects.get(activityId=activity_id)
                    sender = Employee.objects.get(username=activity.senderId)
                    tasksProject = getProjectTasksByProjectId(activity_id)
                    numberOfCompletedTasks = getCompletedTasks(activity_id)
                    if numberOfCompletedTasks != 0:
                        percentage = percentageCalculator(len(tasksProject), numberOfCompletedTasks)
                        formatPercentage = "{:.2f}".format(percentage)
                        activities = {'activity': activity, 'sender': sender, 'user': user, 'tasks': tasksProject,'usertype': userType, 'numberOfCompletedTasks': numberOfCompletedTasks,
                                  'percentage': percentage, 'formatPercentage': formatPercentage,'notShownNotifications': notShownNotifications,
                                      'notCompletedTasks':notCompletedTasks}
                    else:
                        activities = {'activity': activity, 'sender': sender, 'user': user, 'tasks': tasksProject,
                                      'usertype': userType, 'numberOfCompletedTasks': numberOfCompletedTasks,
                                      'notShownNotifications': notShownNotifications, 'notCompletedTasks': notCompletedTasks}
                    return render(request, 'activities/ProjectRow.html', activities)
                else:
                    activity = Task.objects.get(activityId=activity_id)
                    sender = Employee.objects.get(username=activity.senderId)
                    receiver = Employee.objects.get(username=activity.receiverId)
                    comments = Comment.objects.filter(activity=activity)
                    project = getProjectByTask(activity_id)
                    if activity.projectId != 0:
                        project = Activity.objects.get(activityId=activity.projectId)
                    else:
                        project = None
                    activities = {'activity': activity, 'sender': sender, 'receiver': receiver, 'user': user,
                                  'usertype': userType, 'comments': comments, 'project': project,
                                  'notShownNotifications': notShownNotifications, 'notCompletedTasks': notCompletedTasks}
                    return render(request, 'activities/TaskRow.html', activities)
            else:
                return render(request, 'activities/home.html')
        except Activity.DoesNotExist:
            if userType!= 'director':
                return redirect('myactivities')
            else:
                return redirect('home')
    else:
        request.session['errorMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα. Παρακαλώ συνδεθείτε.'
        return redirect('login')


def show_activity_byNot(request, activity_id, notification_id):
    notification = Notification.objects.get(notId=notification_id)
    notification.isShown = True
    notification.save()
    return show_activity(request, activity_id)


def progressProject(request, project_id=0):
    if request.session.has_key('user'):
        user = Employee.objects.get(username=request.session['user'])
        userType = checkUserType(user)
        try:
            act = Project.objects.get(activityId=project_id)
            if userType != 'officeclerk':
                notShownNotifications = Notification.objects.filter(isShown=False, receiverId=request.session['user'])
                notCompletedTasks = Task.objects.filter(receiverId=request.session['user'], complete=False,
                                                        approved=False)
                if request.method == 'GET':
                    activity = Project.objects.get(activityId=project_id)
                    tasksProject = getProjectTasksByProjectId(project_id)
                    progress = {'activity': activity, 'tasksProject': tasksProject, 'user': user,
                                'usertype': userType, 'navbar': 'sentactivities',
                                'notShownNotifications': notShownNotifications, 'notCompletedTasks':notCompletedTasks}
                    return render(request, 'activities/progressProject.html', progress)

                else:
                    return render(request, 'activities/home.html')
            else:
                return redirect('myactivities')
        except Project.DoesNotExist:
            if userType != 'officeclerk':
                return redirect('home')
            else:
                return redirect('myactivities')
    else:
        request.session['errorMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα. Παρακαλώ συνδεθείτε.'
        return redirect('login')


def create_project(request):
    if request.session.has_key('user'):
        user = Employee.objects.get(username=request.session['user'])
        userType = checkUserType(user)
        if userType != 'officeclerk':
            notShownNotifications = Notification.objects.filter(isShown=False, receiverId=request.session['user'])
            notCompletedTasks = Task.objects.filter(receiverId=request.session['user'], complete=False,
                                                    approved=False)
            if request.method == 'POST':
                activityId = Activity.objects.count() + 1
                title = request.POST['titleProject']
                description = request.POST['descriptionProject']
                deadline = request.POST['dateProject']
                complete = False
                senderId = request.session['user']
                numberOfTasks = 0

                if not title or not deadline:
                    return render(request, 'activities/create_project.html',
                              {'user': user, 'usertype': userType, 'navbar': 'createactivity',
                               'notShownNotifications': notShownNotifications,
                               'message': 'Παρακαλώ συμπληρώστε τα πεδία: Τίτλο, Προθεσμία',
                               'notCompletedTasks': notCompletedTasks})
                else:

                    employees = Employee.objects.all()
                    employee = {'employees_list': employees}
                    number = {'numberOfTasks': numberOfTasks + 1}
                    project = {'project_id': activityId, 'title': title, 'description': description, 'deadline': deadline,
                       'complete': complete, 'sender': senderId, 'numberOfTasks': numberOfTasks}
                    request.session['project'] = project
                    request.session['number'] = number
                    return redirect('create_projectTask')
            else:
                return render(request, 'activities/create_project.html', {'user': user, 'usertype': userType,
                                                                          'navbar': 'createactivity',
                                                                          'notShownNotifications': notShownNotifications,
                                                                          'notCompletedTasks':notCompletedTasks})
        else:
            request.session['noAccessMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα.'
            return redirect('myactivities')
    else:
        request.session['errorMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα. Παρακαλώ συνδεθείτε.'
        return redirect('login')


tasks = {}
numberOfTasks = 0
def create_projectTask(request):
    if request.session.has_key('user'):
        user = Employee.objects.get(username=request.session['user'])
        userType = checkUserType(user)
        if userType != 'officeclerk':
            notShownNotifications = Notification.objects.filter(isShown=False, receiverId=request.session['user'])
            notCompletedTasks = Task.objects.filter(receiverId=request.session['user'], complete=False,
                                                    approved=False)
            if request.session.has_key('project'):
                number = request.session['number']
                employee = setTaskEmployees(user.username)
                employees = {'employees_list': employee, 'numberOfTasks': number['numberOfTasks'],
                             'user': user, 'projectSession': request.session['project'],
                             'usertype': userType, 'navbar': 'createactivity',
                             'notShownNotifications': notShownNotifications, 'notCompletedTasks':notCompletedTasks}

                if 'done' in request.POST:
                    titleTask = request.POST['title']
                    descriptionTask = request.POST['description']
                    deadlineTask = request.POST['date']
                    receiverIdTask = request.POST['employee_department']

                    if not titleTask or not deadlineTask or not receiverIdTask:
                        employees = {'employees_list': employee, 'numberOfTasks': number['numberOfTasks'], 'user': user,
                                 'projectSession': request.session['project'], 'usertype': userType,
                                 'navbar': 'createactivity', 'notShownNotifications': notShownNotifications,
                                     'message': 'Παρακαλώ συμπληρώστε τα πεδία: Τίτλος, Προθεσμία, Υπάλληλο',
                                     'notCompletedTasks': notCompletedTasks}
                        return render(request, 'activities/create_projectTask.html', employees)
                    else:
                        project = request.session['project']
                        number['numberOfTasks'] = number['numberOfTasks'] + 1
                        numberOfTasks = number['numberOfTasks']

                        completeTask = False
                        senderIdTask = request.session['user']
                        projectIdTask = project['project_id']
                        approvedTask = False
                        nameTask = 'task' + str(numberOfTasks)
                        tasks[nameTask] = {'activityId': 0, 'title': titleTask, 'description': descriptionTask,
                               'deadline': deadlineTask, 'complete': False, 'sender': senderIdTask,
                               'projectId': projectIdTask, 'receiver': receiverIdTask, 'approved': approvedTask}
                        project['numberOfTasks'] = project['numberOfTasks'] + 1
                        request.session['tasks'] = tasks

                        projectid = Activity.objects.count() + 1
                        projectTitle = project['title']
                        projectDescription = project['description']
                        projectDeadline = project['deadline']
                        projectSender = project['sender']
                        projectComplete = project['complete']
                        projectnumberOfTasks = project['numberOfTasks']

                        Project.objects.create(
                            activityId=projectid,
                            title=projectTitle,
                            description=projectDescription,
                            deadline=projectDeadline,
                            complete=projectComplete,
                            senderId=projectSender,
                            numberOfTasks=projectnumberOfTasks
                        )

                        tasksProject = request.session['tasks']
                        for task in tasksProject:
                            taskId = Activity.objects.count() + 1
                            taskTitle = tasksProject[task]['title']
                            taskDescription= tasksProject[task]['description']
                            taskDeadline = tasksProject[task]['deadline']
                            taskComplete = tasksProject[task]['complete']
                            taskSender = tasksProject[task]['sender']
                            taskProjectId = projectid
                            taskReceiver = tasksProject[task]['receiver']
                            taskApproved = tasksProject[task]['approved']

                            Task.objects.create(
                                activityId=taskId,
                                title=taskTitle,
                                description=taskDescription,
                                deadline=taskDeadline,
                                complete=taskComplete,
                                senderId=taskSender,
                                receiverId=taskReceiver,
                                projectId=taskProjectId,
                                approved=taskApproved
                            )

                            Notification.objects.create(
                                notId=Notification.objects.count() + 1,
                                message='Ο χρήστης ' + taskSender + ' σας ανέθεσε την αρμοδιότητα ' + taskTitle,
                                activityId=taskId,
                                receiverId=taskReceiver
                            )

                        del request.session['project']
                        del request.session['number']
                        del request.session['tasks']

                        return redirect('home')
                elif 'next' in request.POST:
                    titleTask = request.POST['title']
                    descriptionTask = request.POST['description']
                    deadlineTask = request.POST['date']
                    receiverIdTask = request.POST['employee_department']
                    if not titleTask or not deadlineTask or not receiverIdTask:
                        employees = {'employees_list': employee, 'numberOfTasks': number['numberOfTasks'], 'user': user,
                                 'projectSession': request.session['project'], 'usertype': userType,
                                 'navbar': 'createactivity', 'notShownNotifications': notShownNotifications,
                                     'message': 'Παρακαλώ συμπληρώστε τα πεδία: Τίτλος, Προθεσμία, Υπάλληλο',
                                     'notCompletedTasks':notCompletedTasks}
                        return render(request, 'activities/create_projectTask.html', employees)
                    else:
                        project = request.session['project']
                        number['numberOfTasks'] = number['numberOfTasks'] + 1
                        numberOfTasks = number['numberOfTasks']

                        Id = Activity.objects.count() + 1
                        completeTask = False
                        senderIdTask = request.session['user']
                        projectIdTask = project['project_id']
                        approvedTask = False
                        nameTask = 'task' + str(numberOfTasks)
                        tasks[nameTask] = {'activityId': Id, 'title': titleTask, 'description': descriptionTask,
                               'deadline': deadlineTask, 'complete': False, 'sender': senderIdTask,
                               'projectId': projectIdTask, 'receiver': receiverIdTask, 'approved': approvedTask}
                        project['numberOfTasks'] = project['numberOfTasks'] + 1
                        request.session['tasks'] = tasks

                        number = {'numberOfTasks': numberOfTasks}
                        employees = {'employees_list': employee, 'numberOfTasks': number['numberOfTasks'], 'projectSession': request.session['project'], 'usertype': userType, 'navbar': 'createactivity', 'notShownNotifications': notShownNotifications}
                        request.session['number'] = number

                        return render(request, 'activities/create_projectTask.html', employees)
                else:
                    return render(request, 'activities/create_projectTask.html', employees)
            else:
                return redirect('home')
        else:
            request.session['noAccessMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα.'
            return redirect('myactivities')
    else:
        request.session['errorMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα. Παρακαλώ συνδεθείτε.'
        return redirect('login')


def submitTask(request, task_id):
    if request.session.has_key('user'):
        task = Task.objects.get(activityId=task_id)
        task.complete = True
        task.save()
        receiver = Employee.objects.get(username=task.receiverId)
        taskReceiver = receiver.name + ' '+receiver.surname
        taskTitle = task.title

        Notification.objects.create(
            notId=Notification.objects.count() + 1,
            message='Ο χρήστης ' + taskReceiver + ' υπέβαλε την αρμοδιότητα ' + taskTitle + '. Αναμένεται έγκριση',
            activityId=task_id,
            receiverId=task.senderId
        )
        return redirect('myactivities')
    else:
        request.session['errorMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα. Παρακαλώ συνδεθείτε.'
        return redirect('login')


def approveTask(request, task_id):
    if request.session.has_key('user'):
        task = Task.objects.get(activityId=task_id)
        task.approved = True
        task.save()

        sender = Employee.objects.get(username=task.senderId)
        taskSender = sender.name + ' '+sender.surname
        taskTitle = task.title

        Notification.objects.create(
            notId=Notification.objects.count() + 1,
            message='Ο χρήστης ' + taskSender + ' ενέκρινε την αρμοδιότητα ' + taskTitle,
            activityId=task_id,
            receiverId=task.receiverId
        )
        return redirect('home')
    else:
        request.session['errorMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα. Παρακαλώ συνδεθείτε.'
        return redirect('login')


def rejectTask(request, task_id):
    if request.session.has_key('user'):
        task = Task.objects.get(activityId=task_id)
        task.complete = False
        task.deadline = request.POST['date']
        task.save()

        sender = Employee.objects.get(username=task.senderId)
        taskSender = sender.name + ' '+sender.surname
        taskTitle = task.title

        message = request.POST['commentArea']

        Comment.objects.create(
            commentId=Comment.objects.count() + 1,
            message=message,
            sentBySender=True,
            activity=task
        )

        Notification.objects.create(
            notId=Notification.objects.count() + 1,
            message='Ο χρήστης ' + taskSender + ' απέρριψε την αρμοδιότητα ' + taskTitle + ' και πρόσθεσε ένα σχόλιο.',
            activityId=task_id,
            receiverId=task.receiverId
        )

        return redirect('home')
    else:
        request.session['errorMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα. Παρακαλώ συνδεθείτε.'
        return redirect('login')


def sendComment(request):
    if request.session.has_key('user'):
        count = request.POST['count']
        commentArea = 'commentArea' + count
        message = request.POST[commentArea]
        sentBySenderString = request.POST['sentBySender']

        if message:
            sentBySender = False
            task = Task.objects.get(activityId=request.POST['activityId'])
            if sentBySenderString == 'false':
                notReceiverId = task.senderId
                sentBySender = False
            else:
                notReceiverId = task.receiverId
                sentBySender = True

            Comment.objects.create(
                commentId=Comment.objects.count() + 1,
                message=message,
                sentBySender=sentBySender,
                activity=task
            )

            employee = Employee.objects.get(username=request.session['user'])
            name = '' + employee.name + ' ' + employee.surname + ''
            messageNot = 'Ο χρήστης ' + name + ' προσέθεσε σχόλιο στην αρμοδιότητα ' + task.title + '.'

            Notification.objects.create(
                notId=Notification.objects.count() + 1,
                message=messageNot,
                activityId=task.activityId,
                receiverId=notReceiverId
            )

            if sentBySenderString == 'false':
                return redirect('myactivities')
            else:
                return redirect('home')
        else:
            if sentBySenderString == 'false':
                return redirect('myactivities')
            else:
                return redirect('home')
    else:
        request.session['errorMessage'] = 'Δεν επιτρέπεται η πρόσβαση σε αυτή τη σελίδα. Παρακαλώ συνδεθείτε.'
        return redirect('login')




