from django.conf.urls import patterns, include, url

urlpatterns = patterns('classrooms.views',
	(r'^test/', 'test'),
)

urlpatterns += patterns('classrooms.ajax',
    (r'^createGroup/$', 'createGroup'),
    (r'^deleteSession/$', 'deleteSession'),
    (r'^changeGroupName/$', 'changeGroupName'),
    (r'^toggleLockGroup/$', 'toggleLockGroup'),
    (r'^joinGroup/$', 'joinGroup'),
    (r'^postMessage/$', 'postMessage'),
    (r'^deleteMessage/$', 'deleteMessage'),
    (r'^editProfile/$', 'editProfile'),
    (r'^getOldMessages/$', 'getOldMessages'),
    (r'^getNewMessages/$', 'getNewMessages'),
    (r'^addSession/$', 'addSession'),
    (r'^editSession/$', 'editSession'),
    (r'^allSessionsPrint/(?P<sessionID>\d+)/$', 'allSessionsPrint'),
    (r'^allSessionsPrint/$', 'allSessionsPrint'),
    (r'^mySchedulePrint/(?P<userID>\d+)/$', 'mySchedulePrint'),
    (r'^mySchedulePrint/$', 'mySchedulePrint'),
    (r'^unscheduled/$', 'unscheduled'),
    
)