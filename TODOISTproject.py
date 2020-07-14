import datetime
import pandas
from todoist import TodoistAPI as tapi

# TODO: 코드 정리하기

print('made by Team COFFEEN')
print('project_version = 0.1.0')


# def fun

# check
def checkUserLog():
    try:
        userIdText = open('./data/UserId.txt')
        projectNameText = open('./data/ProjectName.txt')
        todoistId = userIdText.readline()
        todoistProjectName = projectNameText.readline()
        return todoistId, todoistProjectName
    except:
        return writeUserInfo()


def writeUserInfo():
    todoistId = input('please write your TodoistID : ')
    todoistProjectName = input('please write your project name : ')
    makeFolder()
    if isInputValid(todoistId, todoistProjectName):
        print('\033[33m' + 'WARNING : You have to put the value. Please put your TodoistAPI id or ProjectName.')
        exit()
    makeFile(todoistId, todoistProjectName)
    return todoistId, todoistProjectName


def makeFile(todoistId, todoistProjectName):
    userIdText = open('./data/UserId.txt', 'w')
    projectNameText = open('./data/ProjectName.txt', 'w')
    userIdText.write(todoistId)
    projectNameText.write(todoistProjectName)
    userIdText.close()
    projectNameText.close()


def isInputValid(todoistId, todoistProjectName):
    return todoistId is None or todoistProjectName is None


# GET TODAY VALUE
def getToday():
    today = datetime.date.today()
    if today.month < 10:
        returnValue = str(today.year) + '-0' + str(today.month)
    else:
        returnValue = str(today.year) + '-' + str(today.month)

    if today.day < 10:
        returnValue = returnValue + '-0' + str(today.day)
    else:
        returnValue = returnValue + '-' + str(today.day)
    return returnValue


# PARSE DATA
# 진행순서 - getTodoList -> getToday -> getExcel -> parseExcelData
def getExcel():
    try:
        data = pandas.read_excel('./data/timetable.xls')
        return data
    except:
        print('\033[31m' +
              'ERROR : There is no excel file in data folder.' +
              ' please check your excel and please try again')
        exit()


def makeFolder():
    import os
    if not os.path.isdir('./data'):
        os.mkdir('./data')


def parseExcelData(today, data):
    returnList = []
    for i in range(data['일자'].size):
        if today in data['일자'][i]:
            returnList.append(data['클래스명'][i])
    return returnList


def getTodoList():
    today = getToday()
    data = getExcel()
    return parseExcelData(today, data)


# TODOIST variable
todoistId, todoistProjectName = checkUserLog()
api = tapi(todoistId)
api.sync()
project = api.projects


# TODOIST check id validity
def checkApiValidity():
    if '<not synchronized>' in str(api):
        print('\033[31m' + 'ERROR : Your Todoist ID is not valid. Please check your TodoistID and do it again')
        exit()


# TODOIST project check and make

def checkProjectExist():
    """

    :rtype: object
    """
    for projects in api.state['projects']:
        if todoistProjectName in projects['name']:
            return projects['id']
    return makeProject()


def makeProject():
    print(
        '\033[96m' + 'MESSAGE : this program will make project for save tasks. The name of this project\'s name is ' + todoistProjectName)
    projects = api.projects.add(todoistProjectName)
    api.commit()
    return projects['id']


# TODOIST task making

def checkTaskExist():
    for tasks in api.state['items']:

        condition1 = projectId == tasks['project_id']
        condition2 = tasks['date_completed'] is None
        if condition1 and condition2:
            continueValue = input(
                '\033[33m' + 'WARNING : Project (' + todoistProjectName + ') already has the tasks. Do you want to continue?' + '(Y/n)')
            if continueValue == 'Y' or continueValue == 'y':
                makeTask()
                return
            else:
                exit()
    makeTask()
    return


def makeTask():
    taskList = []
    for i in range(6):
        taskList.append(api.items.add(str(getTodoList()[i]), project_id=projectId))

        taskList[i].update(due={'string': getToday() + ' 22:00'})

        api.commit()


checkUserLog()
print(getTodoList())
checkApiValidity()
projectId = checkProjectExist()
checkTaskExist()