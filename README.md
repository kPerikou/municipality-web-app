# Municipality Web App 

This repository serves as a storage for a project that was created at the `Information Systems Implementation and Architectures` course during my 5th semester offered by the Department of Management Science & Technology of Athens University of Economics and Business.

## Overview

This web project is developed on `Django framework` and is created for delegating responsibilities inside a municipal organization. The initial idea for this website was generated from a survey that me and my colleagues conducted concerning the management of a Greek municipality. Insufficient responsibilities' management was found to be the main problem.
This system provides the solution to this problem by giving the possibility to assign tasks and projects and keep track of their progress. In this way, the workflow is faster and better managed by handling deadlines and new responsibilities and thus, the whole organisation operates more efficiently.

The use cases that are covered on this project are:
- sign in as a direction director/department director/office clerk
- create projects and tasks 
- assign projects and tasks to a department director or to an office clerk
- send notifications to the assignee and showing to them their tasks
- submit a task as completed
- approve or decline a task
- leave a comment on the tasks and send the corresponding notification


### Prerequisites

1. Install ubuntu 18.04 for Windows
2. Install [latest python version](https://www.python.org/downloads/)
3. Install [pip](https://pypi.org/project/pip/)
4. Clone this repository

### Running the project (setup)

1. Clone this repository:
```
$ git clone https://github.com/kPerikou/municipality-web-app.git
$ cd municipality-web-app
```

2. Create a virtual environment to install dependencies in and activate it:
```
$ virtualenv env
$ source env/bin/activate
```

3. Then install the dependencies:
```
(env)$ pip install -r requirements.txt
```

4. Run the project:
```
(env)$ python manage.py make migrations
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```

### Credits

For the initial idea credits are also given to [Elvira Antonogiannaki](https://github.com/Elviraant/), [Maria Gkoulta](https://github.com/MariaGkoulta/) and [Dora Andreadi](https://github.com/tandreadi).