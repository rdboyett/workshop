from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^google/', include('google_login.urls')),
    url(r'^class/', include('classrooms.urls')),
    #url(r'^profile/', include('userInfo_profile.urls')),
    
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),
    
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#local views file
urlpatterns += patterns('workshop_project.views',
    (r'^$', 'index'),
    (r'^dashboard/$', 'dashboard'),
    (r'^classView/(?P<classID>\d+)/$', 'classView'),
    (r'^studentView/(?P<studentID>\d+)/$', 'studentView'),
    (r'^classView/$', 'classView'),
    (r'^studentView/$', 'studentView'),
    
)
