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
        
    if userInfo.classrooms.all():
        mySessions = userInfo.classrooms.all()
    else:
        mySessions = False
        
    args = {
            'user':request.user,
            'userInfo':userInfo,
            'dashboard':True,
            'mySessions':mySessions,
            'today':datetime.date.today(),
        }
    args.update(csrf(request))
    
    return render_to_response("dashboard.html", args)



@login_required
def classView(request, classID=False):
    userInfo = ClassUser.objects.get(user=request.user)
        
    if userInfo.classrooms.all():
        mySessions = userInfo.classrooms.all()
    else:
        mySessions = False
        
    if classID:
        if Classroom.objects.filter(id=classID):
            currentSession = Classroom.objects.get(id=classID)
            sessions = False
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
    elif ClassUser.objects.all():
        userInfos = ClassUser.objects.all()
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


































