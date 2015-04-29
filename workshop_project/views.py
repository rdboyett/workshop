import json
import datetime

from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.mail import send_mail

#from userInfo_profile.models import UserInfo, MyAnswer, MyGrade
from classrooms.models import ClassUser, Classroom, HashTag, Message
from google_login.models import GoogleUserInfo



import logging
log = logging.getLogger(__name__)



def index(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        if User.objects.filter(id=user_id):
            user = User.objects.get(id=user_id)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return HttpResponseRedirect("/dashboard/")
        
        else:
            user_id = False
    else:
        return redirect('/google/auth/')



@login_required
def dashboard(request):
    userInfo = ClassUser.objects.get(user=request.user)
    
    availableClassTimes = []
    availableTimeSlots = []
        
    if userInfo.classrooms.all():
        mySessions = userInfo.classrooms.all()
        possibleDates = []
        for session in mySessions:
            if session.classDate not in possibleDates:
                possibleDates.append(session.classDate)
        
        #Check each date against all available classes
        if possibleDates:
            for date in possibleDates:
                startTimes_to_exclude = [x.startTime for x in mySessions.filter(classDate=date)]
                if Classroom.objects.filter(classDate=date).exclude(startTime__in=startTimes_to_exclude):
                    allClasses = Classroom.objects.filter(classDate=date).exclude(startTime__in=startTimes_to_exclude).order_by('name')
                    availableClassTimes.extend(allClasses)
                    
            tempDateTime = []
            for currentClass in availableClassTimes:
                currentClassDateTime = datetime.datetime.combine(currentClass.classDate, currentClass.startTime)
                if currentClassDateTime not in tempDateTime:
                    tempDateTime.append(currentClassDateTime)
                    availableTimeSlots.append(currentClass)
        
    else:
        mySessions = False
        
    args = {
            'user':request.user,
            'userInfo':userInfo,
            'dashboard':True,
            'mySessions':mySessions,
            'today':datetime.date.today(),
            'availableTimeSlots':availableTimeSlots,
        }
    args.update(csrf(request))
    
    return render_to_response("dashboard.html", args)



@login_required
def classView(request, classID=False):
    userInfo = ClassUser.objects.get(user=request.user)
    
    bPostSort=False
    if request.method == 'POST':
        date = request.POST['date'].strip()
        startTime = request.POST['startTime'].strip()
        bPostSort = True
        
        
        
    if userInfo.classrooms.all():
        mySessions = userInfo.classrooms.all()
    else:
        mySessions = False
        
    if classID:
        if Classroom.objects.filter(id=classID):
            currentSession = Classroom.objects.get(id=classID)
            sessions = False
    elif bPostSort and Classroom.objects.filter(active=True, classDate=date, startTime=startTime):
        sessions = Classroom.objects.filter(active=True, classDate=date, startTime=startTime)
        currentSession = False
    elif Classroom.objects.filter(active=True, classDate__gte=datetime.date.today()):
        sessions = Classroom.objects.filter(active=True, classDate__gte=datetime.date.today())
        currentSession = False
    else:
        sessions = False
        currentSession = False
        
    args = {
            'user':request.user,
            'userInfo':userInfo,
            'classView':True,
            'sessions':sessions,
            'currentSession':currentSession,
            'mySessions':mySessions,
        }
    args.update(csrf(request))
    
    return render_to_response("classView.html", args)




@login_required
def studentView(request, studentID=False):
    userInfo = ClassUser.objects.get(user=request.user)
    
    if studentID:
        if ClassUser.objects.filter(id=studentID):
            currentUser = ClassUser.objects.get(id=studentID)
            userInfos = False
    elif ClassUser.objects.filter(teacher=False):
        userInfos = ClassUser.objects.filter(teacher=False)
        currentUser = False
    else:
        currentUser = False
        userInfos = False
        
    args = {
            'user':request.user,
            'userInfo':userInfo,
            'studentView':True,
            'userInfos':userInfos,
            'currentUser':currentUser,
        }
    args.update(csrf(request))
    
    return render_to_response("studentView.html", args)




@login_required
def conferenceView(request):
    userInfo = ClassUser.objects.get(user=request.user)
    
    #I'me creating a table by room(heading) and startTime(on left side)
    
    #need to first get all possible locations by date
    
    sessionTables = []
    
    #first get all possible dates for sessions
    if Classroom.objects.filter(active=True, classDate__gte=datetime.date.today()):
        allSessions = Classroom.objects.filter(active=True, classDate__gte=datetime.date.today())
        possibleDates = []
        for session in allSessions:
            if session.classDate not in possibleDates:
                possibleDates.append(session.classDate)
        
        
        if possibleDates:
            for date in possibleDates:
                #get all possible classes
                allClasses = Classroom.objects.filter(classDate=date).order_by('location')
                
                #get all possible locations
                availableLocations = []
                bSessionsLocked = False
                for currentClass in allClasses:
                    if not currentClass.allowJoin:
                        bSessionsLocked = True
                    if currentClass.location not in availableLocations:
                        availableLocations.append(currentClass.location)
                        
                #get all possible time slots for sessions
                possibleStartTimes = []
                for currentClass in allClasses:
                    if currentClass.startTime not in possibleStartTimes:
                        possibleStartTimes.append(currentClass.startTime)
                        
                #Now lets build sessions object row by row and column by column
                #loop through the classes and check that they correspond with the correct location and startTime if not place an empty object
                #sessionsTableObject = {'date':date, 'columns':['column1', 'column2'...], 'rows':['row1','row2'...], 'TwoD_Sessions':[[classObject, classObject, 'empty'], [classObject, classObject, 'empty']]}
                # sessions above is a 2D array
                
                sessionsTableObject = {}
                sessionsTableObject['date'] = date  #this starts a new table
                sessionsTableObject['lockedStatus'] = bSessionsLocked  #In order to keep track if all sessions are locked or unlocked
                sessionsTableObject['columns'] = availableLocations  #these are the room locations
                sessionsTableObject['rows'] = possibleStartTimes  #these are the startTimes
                
                #Next create the list of classes checked against the column and row if necessary add False for blank spots
                TwoD_Sessions = []
                for startTime in possibleStartTimes:
                    currentRow = []
                    currentRow.append({'rowStarter':startTime})
                    for location in availableLocations:
                        if allClasses.filter(startTime=startTime, location=location):
                            currentRow.append(allClasses.get(startTime=startTime, location=location))
                        else:
                            currentRow.append({'empty':'Empty'})
                            
                    TwoD_Sessions.append(currentRow)  #add the row to the 2D array
                    
                #finally add to table object
                sessionsTableObject['TwoD_Sessions'] = TwoD_Sessions
                
                #Then append that to the sessionTables
                sessionTables.append(sessionsTableObject)
        
        
        
        
    log.info(sessionTables)
    
    args = {
            'user':request.user,
            'userInfo':userInfo,
            'sessionTables':sessionTables,
            'conferenceView':conferenceView,
        }
    args.update(csrf(request))
    
    return render_to_response("conferenceView.html", args)































