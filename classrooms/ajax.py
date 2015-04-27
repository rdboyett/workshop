import json
import re
import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from classrooms.models import ClassUser, Classroom, HashTag, Message
from classrooms.views import generateCode


import logging
log = logging.getLogger(__name__)



@login_required
def createGroup(request):
    if request.method == 'POST':
        userInfo = ClassUser.objects.get(user=request.user)
        name = request.POST['session_name'].strip().title()
        description = request.POST['description'].strip()
        date = request.POST['date'].strip()
        location = request.POST['location'].strip()
        startTime = request.POST['startTime'].strip()
        endTime = request.POST['endTime'].strip()
        classLimit = int(request.POST['classSize'])
        groupCode = generateCode()
        
        newStartTime = datetime.time(*map(int, startTime.split(':')))
        newEndTime = datetime.time(*map(int, endTime.split(':')))
        #log.info('here is my test time: '+str(newTime))
        
        
        if Classroom.objects.filter(classDate=date, location=location):
            classrooms = Classroom.objects.filter(classDate=date, location=location)
            for session in classrooms:
                if newStartTime >= session.startTime and newStartTime < session.endTime:
                    #log.info('Session: '+session.name+' is already happening from '+session.startTime.strftime('%H:%I %p')+' to '+session.endTime.strftime('%H:%I %p')+' at that location.')
                    data = {'error':'Session: '+session.name+' is already happening from '+session.startTime.strftime('%H:%M %p')+' to '+session.endTime.strftime('%H:%M %p')+' at that location. Your new session starts during this session.'}
                    return HttpResponse(json.dumps(data))
                elif newEndTime >= session.startTime and newEndTime < session.endTime:
                    #log.info('Session: '+session.name+' is already happening from '+session.startTime.strftime('%H:%I %p')+' to '+session.endTime.strftime('%H:%I %p')+' at that location.')
                    data = {'error':'Session: '+session.name+' is already happening from '+session.startTime.strftime('%H:%M %p')+' to '+session.endTime.strftime('%H:%M %p')+' at that location. Your new session runs into this session.'}
                    return HttpResponse(json.dumps(data))
                elif newStartTime <= session.startTime and newEndTime >= session.endTime:
                    #log.info('Session: '+session.name+' is already happening from '+session.startTime.strftime('%H:%I %p')+' to '+session.endTime.strftime('%H:%I %p')+' at that location.')
                    data = {'error':'Session: '+session.name+' is already happening from '+session.startTime.strftime('%H:%M %p')+' to '+session.endTime.strftime('%H:%M %p')+' at that location. Your new session envelopes this session.'}
                    return HttpResponse(json.dumps(data))
        
        classroom = Classroom.objects.create(
            name = name,
            code = groupCode,
            classOwnerID = userInfo.id,
            classDate = date,
            startTime = startTime,
            endTime = endTime,
            location = location,
            description = description,
            classLimit = classLimit
        )
        # We don't need this to automatically add
        #userInfo.classrooms.add(classroom)
        
        data = {'groupID':classroom.id}
        #log.info("SessionName: "+str(name)+ " and GroupCode: "+str(groupCode)+ " and date: "+str(date)+ " and location: "+str(location)+ " and startTime: "+str(startTime)+ " and endTime: "+str(endTime)+ " and description: "+str(description))
    else:
        data = {'error':"didn't work"}
                
    return HttpResponse(json.dumps(data))



@login_required
def deleteSession(request):
    if request.method == 'POST':
        classID = request.POST["sessionID"]
        #log.info("classID: "+str(classID))
        
        userInfo = ClassUser.objects.get(user=request.user)
                
        if Classroom.objects.filter(id=classID):
            Classroom.objects.get(id=classID).delete()
                
                
            data = {
                    'classID': classID,
                }
        else:
            data = {
                'error': "There is no class by that id",
            }
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))




@login_required
def changeGroupName(request):
    if request.method == 'POST':
        classID = request.POST["groupID"]
        group_name = request.POST["group_name"]
        #log.info("classID: "+str(classID))
        
        if Classroom.objects.filter(id=classID):
            classRoom = Classroom.objects.get(id=classID)
            classRoom.name = group_name
            classRoom.save()
            
            data = {
                'groupID': classID,
            }
        else:
            data = {
                'error': "There is no class by that id",
            }
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))





@login_required
def toggleLockGroup(request):
    if request.method == 'POST':
        classID = request.POST["groupID"]
        #log.info("classID: "+str(classID))
        
        if Classroom.objects.filter(id=classID):
            classRoom = Classroom.objects.get(id=classID)
            
            if classRoom.allowJoin:
                classRoom.allowJoin = False
            else:
                classRoom.allowJoin = True
                
            classRoom.save()
            
            data = {
                'allowJoin': classRoom.allowJoin,
            }
        else:
            data = {
                'error': "There is no class by that id",
            }
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))



@login_required
def joinGroup(request):
    if request.method == 'POST':
        joinCode = request.POST["groupCode"]
        #log.info("classID: "+str(classID))
        
        
        userInfo = ClassUser.objects.get(user=request.user)
                
        #Get all users classes
        if userInfo.classrooms.all():
            allClasses = userInfo.classrooms.all()
        else:
            allClasses = False
        
        
        #get the the class with that joinCode
        if Classroom.objects.filter(code=joinCode):
            newClass = Classroom.objects.get(code=joinCode)
            
                
            if allClasses and newClass in allClasses:
                data = {'error': "Sorry, you already have this class.",}
            else:
                #check to see if you are allowed to join
                if newClass.allowJoin:
                    userInfo.classrooms.add(newClass)
                    data = {
                        'groupID': newClass.id,
                    }
                else:
                    data = {'error': "Sorry, this class is locked by the owner.",}
            
            
            
            
        else:
            data = {'error': "Sorry, there are no classes with that code.",}
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))




@login_required
def postMessage(request):
    if request.method == 'POST':
        tweetText = request.POST["post_message"]
        classroomID = request.POST["classID"]
        
        userInfo = ClassUser.objects.get(user=request.user)
        currentClass = Classroom.objects.get(id=classroomID)
        
        #Scrub hashtags out
        reg = re.compile(r'(?:^|\s)[#?](\S*)')
        hashTagList = re.findall(reg, tweetText)
        
        #Save the message
        newTweet = Message.objects.create(
            text = tweetText,
        )
        
        currentClass.messages.add(newTweet)
        userInfo.messages.add(newTweet)
        
        #Save the hashtag individually and point it back to the messages its found in.
        if hashTagList:
            for tag in hashTagList:
                if HashTag.objects.filter(tag=tag):
                    newHashTag = HashTag.objects.get(tag=tag)
                else:
                    newHashTag = HashTag.objects.create(
                        tag = tag,
                        classroomID = classroomID,
                    )
                    
                newHashTag.messages.add(newTweet)
        
        return render_to_response('post_message.html', {
            'message':newTweet,
            'groupID':classroomID,
            'userInfo':userInfo,
        } )
        data = {
            'success': 'True',
            'tweetID': newTweet.id,
            'tweetText': tweetText,
        }
    
    else:
        data = {'error':'Did not post correctly',}
            
    return HttpResponse(json.dumps(data))



@login_required
def deleteMessage(request):
    if request.method == 'POST':
        tweetID = request.POST["messageID"]
        
        userInfo = ClassUser.objects.get(user=request.user)
        
        if Message.objects.filter(id=tweetID):
            oldTweet = Message.objects.get(id=tweetID)
            
            #delete any records for hashtags
            if HashTag.objects.filter(messages=oldTweet):
                hashTagList = HashTag.objects.filter(messages=oldTweet)
                for hashTag in hashTagList:
                    hashTag.messages.remove(oldTweet)
                    if hashTag.messages.all().count() == 0:
                        hashTag.delete()
                        
                    
            userInfo.messages.remove(oldTweet)
            
            for classRoom in oldTweet.classroom_set.all():
                classRoom.messages.remove(oldTweet)
            
            oldTweet.delete()
                    
            data = {
                    'success': 'success',
                    'messageID': tweetID,
                }
                
        
        else:
            data = {
                'error': "Oh no! I can't find that darn message anywhere!",
            }
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
        
            
    return HttpResponse(json.dumps(data))





@login_required
def editProfile(request):
    if request.method == 'POST':
        userFirstName = request.POST["userFirstName"]
        background_color = request.POST["background_color"]
        text_color = request.POST["text_color"]
        
        if ClassUser.objects.filter(user=request.user):
            classUser = ClassUser.objects.get(user=request.user)
            classUser.user.first_name = userFirstName
            classUser.user.save()
            classUser.avatarBackColor = background_color
            classUser.avatarTextColor = text_color
            classUser.save()
            
            data={'success':'success'}
            
        else:
            return HttpResponse(json.dumps({'error':"Sorry, something went wrong."}))
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
        
            
    return HttpResponse(json.dumps(data))




@login_required
def getOldMessages(request):
    if request.method == 'POST':
        lastMessageID = request.POST["lastMessageID"]
        classroomID = request.POST["groupID"]
        
        userInfo = ClassUser.objects.get(user=request.user)
        currentClass = Classroom.objects.get(id=classroomID)
        
        lastMessage = get_object_or_404(Message, id=lastMessageID)
        
        if Message.objects.filter(classroom__id=classroomID, timeDate__lte=lastMessage.timeDate):
            nextMessages = Message.objects.filter(classroom__id=classroomID, timeDate__lte=lastMessage.timeDate).order_by('-timeDate')[1:21]
        else:
            nextMessages = False
            
        return render_to_response('get_messages.html', {
            'messages':nextMessages,
            'userInfo':userInfo,
        } )
    
    else:
        data = {'error':'Did not post correctly',}
            
    return HttpResponse(json.dumps(data))



@login_required
def getNewMessages(request):
    if request.method == 'POST':
        firstMessageID = request.POST["firstMessageID"]
        classroomID = request.POST["groupID"]
        
        userInfo = ClassUser.objects.get(user=request.user)
        currentClass = Classroom.objects.get(id=classroomID)
        
        firstMessage = get_object_or_404(Message, id=firstMessageID)
        
        if Message.objects.filter(classroom__id=classroomID, timeDate__lte=firstMessage.timeDate):
            nextMessages = Message.objects.filter(classroom__id=classroomID, timeDate__gte=firstMessage.timeDate).order_by('timeDate')[1:21]
        else:
            nextMessages = False
            
        return render_to_response('get_messages.html', {
            'messages':nextMessages,
            'userInfo':userInfo,
        } )
    
    else:
        data = {'error':'Did not post correctly',}
            
    return HttpResponse(json.dumps(data))





@login_required
def addSession(request):
    if request.method == 'POST':
        sessionID = request.POST["sessionID"].strip()
        addRemove = request.POST["addRemove"].strip()
        
        
        userInfo = ClassUser.objects.get(user=request.user)
                
        #Get all users classes
        if userInfo.classrooms.all():
            allClasses = userInfo.classrooms.all()
        else:
            allClasses = False
        
        
        #get the the class with that id
        if Classroom.objects.filter(id=sessionID):
            newClass = Classroom.objects.get(id=sessionID)
                
            if allClasses and newClass in allClasses:
                if addRemove == 'remove':
                    userInfo.classrooms.remove(newClass)
                    if newClass.classSize > 0:
                        newClass.classSize = newClass.classSize-1
                        newClass.classFull = False
                    elif newClass.classSize < 0:
                        newClass.classSize = 0
                        
                    newClass.save()
                        
                
                data = {'groupID': newClass.id,}
            else:
                #check to see if you are allowed to join
                if newClass.allowJoin:
                    if addRemove == 'add':
                        
                        #Check if the class is full
                        if not newClass.classFull:
                            #You are checking that the user doesn't already have a session scheduled for the same time and date.
                            #You are also checking that the user doesn't already have a session with the same name and location
                            #Check if user has a session already during this date, time and location.
                            #Check if user has already signed up for the session with the same name, location and date.
                            #The 2 the above they have in common are date and location EXCLUDE THE CURRENT CLASS
                                #Then check individually for same time different location
                                #Then check individually for same name
                            
                            #Name and location check
                            #You are also checking that the user doesn't already have a session with the same name and location.
                            if Classroom.objects.filter(classuser__id=userInfo.id, name=newClass.name, location=newClass.location):
                                mySessions = Classroom.objects.filter(classuser__id=userInfo.id, name=newClass.name, location=newClass.location)
                                for session in mySessions:
                                    data = {'error':'Sorry, you already have session: '+session.name+' scheduled from '+session.startTime.strftime('%H:%M %p')+' to '+session.endTime.strftime('%H:%M %p')+' at that location. Your new session has the same name and location. Please remove the old session first or find a new session.'}
                                    return HttpResponse(json.dumps(data))
                                
                                
                            #You are checking that the user doesn't already have a session scheduled for the same time and date.
                            elif Classroom.objects.filter(classuser__id=userInfo.id, classDate=newClass.classDate):
                                mySessions = Classroom.objects.filter(classuser__id=userInfo.id, classDate=newClass.classDate)
                                bFoundSession = False
                                for session in mySessions:
                                    if newClass.startTime >= session.startTime and newClass.startTime < session.endTime:
                                        #log.info('Session: '+session.name+' is already happening from '+session.startTime.strftime('%H:%I %p')+' to '+session.endTime.strftime('%H:%I %p')+' at that location.')
                                        data = {'error':'Sorry, you already have session: '+session.name+' scheduled from '+session.startTime.strftime('%H:%M %p')+' to '+session.endTime.strftime('%H:%M %p')+' during that time. Your new session starts during this scheduled session. Please remove the old session first or find a new session.'}
                                        bFoundSession = True
                                    elif newClass.endTime >= session.startTime and newClass.endTime < session.endTime:
                                        #log.info('Session: '+session.name+' is already happening from '+session.startTime.strftime('%H:%I %p')+' to '+session.endTime.strftime('%H:%I %p')+' at that location.')
                                        data = {'error':'Sorry, you already have session: '+session.name+' scheduled from '+session.startTime.strftime('%H:%M %p')+' to '+session.endTime.strftime('%H:%M %p')+' during that time. Your new session runs into this scheduled session. Please remove the old session first or find a new session.'}
                                        bFoundSession = True
                                    elif newClass.startTime <= session.startTime and newClass.endTime >= session.endTime:
                                        #log.info('Session: '+session.name+' is already happening from '+session.startTime.strftime('%H:%I %p')+' to '+session.endTime.strftime('%H:%I %p')+' at that location.')
                                        data = {'error':'Sorry, you already have session: '+session.name+' scheduled from '+session.startTime.strftime('%H:%M %p')+' to '+session.endTime.strftime('%H:%M %p')+' during that time. Your new session envelopes this scheduled session. Please remove the old session first or find a new session.'}
                                        bFoundSession = True
                                        
                                if bFoundSession:
                                    return HttpResponse(json.dumps(data))
                                else:
                                    userInfo.classrooms.add(newClass)
                                    #Now add to class size and check if full
                                    if newClass.classSize < 0:
                                        newClass.classSize = 0
                                    
                                    newClass.classSize +=1
                                    if newClass.classSize >= newClass.classLimit:  #then class is full
                                        newClass.classFull = True
                                        
                                    newClass.save()
                                    
                                    data = {'groupID': newClass.id,}
                                    
        
                            
                            else:
                                userInfo.classrooms.add(newClass)
                                #Now add to class size and check if full
                                if newClass.classSize < 0:
                                    newClass.classSize = 0
                                
                                newClass.classSize +=1
                                if newClass.classSize >= newClass.classLimit:  #then class is full
                                    newClass.classFull = True
                                    
                                newClass.save()
                                
                                data = {'groupID': newClass.id,}
                            
                            
                        else:
                            data = {'error': 'Sorry, this session is full.'}
                            
                    else:
                        data = {'groupID': newClass.id,}
                        
                else:
                    data = {'error': "Sorry, this session is locked.",}
            
            
            
            
        else:
            data = {'error': "Sorry, there are no sessions with that name.",}
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))



@login_required
def editSession(request):
    if request.method == 'POST':
        userInfo = ClassUser.objects.get(user=request.user)
        sessionID = request.POST['sessionID'].strip().title()
        name = request.POST['session_name'].strip().title()
        description = request.POST['description'].strip()
        date = request.POST['date'].strip()
        location = request.POST['location'].strip()
        startTime = request.POST['startTime'].strip()
        endTime = request.POST['endTime'].strip()
        classLimit = int(request.POST['classSize'])
        groupCode = generateCode()
        
        newStartTime = datetime.time(*map(int, startTime.split(':')))
        newEndTime = datetime.time(*map(int, endTime.split(':')))
        #log.info('here is my test time: '+str(newTime))
        
        #First Check if the times were changed and if they were check that it does not overlap with another session
        if Classroom.objects.filter(id=sessionID):
            currentSession = Classroom.objects.get(id=sessionID)
            bTimeChanged = False
            if currentSession.startTime != newStartTime or currentSession.endTime != newEndTime:
                bTimeChanged = True
        
            if Classroom.objects.filter(classDate=date, location=location).exclude(id=sessionID) and bTimeChanged:
                classrooms = Classroom.objects.filter(classDate=date, location=location).exclude(id=sessionID)
                for session in classrooms:
                    if newStartTime >= session.startTime and newStartTime < session.endTime:
                        #log.info('Session: '+session.name+' is already happening from '+session.startTime.strftime('%H:%I %p')+' to '+session.endTime.strftime('%H:%I %p')+' at that location.')
                        data = {'error':'Session: '+session.name+' is already happening from '+session.startTime.strftime('%H:%M %p')+' to '+session.endTime.strftime('%H:%M %p')+' at that location. Your new session starts during this session.'}
                        return HttpResponse(json.dumps(data))
                    elif newEndTime >= session.startTime and newEndTime < session.endTime:
                        #log.info('Session: '+session.name+' is already happening from '+session.startTime.strftime('%H:%I %p')+' to '+session.endTime.strftime('%H:%I %p')+' at that location.')
                        data = {'error':'Session: '+session.name+' is already happening from '+session.startTime.strftime('%H:%M %p')+' to '+session.endTime.strftime('%H:%M %p')+' at that location. Your new session runs into this session.'}
                        return HttpResponse(json.dumps(data))
                    elif newStartTime <= session.startTime and newEndTime >= session.endTime:
                        #log.info('Session: '+session.name+' is already happening from '+session.startTime.strftime('%H:%I %p')+' to '+session.endTime.strftime('%H:%I %p')+' at that location.')
                        data = {'error':'Session: '+session.name+' is already happening from '+session.startTime.strftime('%H:%M %p')+' to '+session.endTime.strftime('%H:%M %p')+' at that location. Your new session envelopes this session.'}
                        return HttpResponse(json.dumps(data))
            
            #Check if class size hase changed
            if not classLimit == currentSession.classLimit:
                if classLimit > currentSession.classLimit:
                    currentSession.classFull = False
                elif classLimit < currentSession.classLimit and currentSession.classSize >= classLimit:
                    currentSession.classFull = True
            
            currentSession.name = name
            currentSession.code = groupCode
            currentSession.classOwnerID = userInfo.id
            currentSession.classDate = date
            currentSession.startTime = newStartTime
            currentSession.endTime = newEndTime
            currentSession.location = location
            currentSession.description = description
            currentSession.classLimit = classLimit
            currentSession.save()
            
            # We don't need this to automatically add
            #userInfo.classrooms.add(classroom)
            
            data = {'groupID':currentSession.id}
            #log.info("SessionName: "+str(name)+ " and GroupCode: "+str(groupCode)+ " and date: "+str(date)+ " and location: "+str(location)+ " and startTime: "+str(startTime)+ " and endTime: "+str(endTime)+ " and description: "+str(description))
        
        else:
            data = {'error':"Sorry, I can't find the session."}
        
    else:
        data = {'error':"didn't work"}
                
    return HttpResponse(json.dumps(data))






@login_required
def allSessionsPrint(request, sessionID=False):
    if sessionID:
        if Classroom.objects.filter(id=sessionID):
            oneSession = Classroom.objects.get(id=sessionID)
        else:
            oneSession = False
        
        sessions = False
    elif Classroom.objects.filter(classDate__gte=datetime.date.today()):
        sessions = Classroom.objects.filter(classDate__gte=datetime.date.today())
        oneSession = False
    else:
        sessions = False
        oneSession = False
    
    
    args = {
            'sessions':sessions,
            'oneSession':oneSession,
        }
    
    return render_to_response("classrooms/allSessions.html", args)




@login_required
def mySchedulePrint(request, userID=False):
    if userID:
        if ClassUser.objects.filter(id=userID):
            userInfo = ClassUser.objects.get(id=userID)
    else:
        if ClassUser.objects.filter(user=request.user):
            userInfo = ClassUser.objects.get(user=request.user)
            
    if userInfo.classrooms.all():
        mySessions = userInfo.classrooms.all()
    else:
        mySessions = False
        
    args = {
            'user':request.user,
            'userInfo':userInfo,
            'mySessions':mySessions,
        }
    
    return render_to_response("classrooms/mySchedulePrint.html", args)
        




@login_required
def unscheduled(request):
    studentAttentionList = []
    if ClassUser.objects.filter(teacher=False, classrooms__classDate__gte=datetime.date.today()):
        allStudents = ClassUser.objects.filter(teacher=False, classrooms__classDate__gte=datetime.date.today())
        for student in allStudents:
            if Classroom.objects.filter(classuser__id=student.id, classDate__gte=datetime.date.today()):
                myStudentSessions = Classroom.objects.filter(classuser__id=student.id, classDate__gte=datetime.date.today())
                
                #first get all the possible dates that they are regestered for
                possibleDates = []
                for session in myStudentSessions:
                    if session.classDate not in possibleDates:
                        possibleDates.append(session.classDate)
                        
                if possibleDates:
                    for date in possibleDates:
                        startTimes_to_exclude = [x.startTime for x in myStudentSessions.filter(classDate=date)]
                        if Classroom.objects.filter(classDate=date).exclude(startTime__in=startTimes_to_exclude):
                            #then there are classes on that date that have startTimes that are different from registerd start times
                            if student not in studentAttentionList:
                                studentAttentionList.append(student)
                    
        
        
    else:
        allStudents = False
        
    args = {
            'user':request.user,
            'studentAttentionList':studentAttentionList,
        }
    
    return render_to_response("classrooms/unscheduled.html", args)




