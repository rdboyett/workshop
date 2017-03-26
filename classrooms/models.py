import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    text = models.TextField(max_length=150)
    timeDate = models.DateTimeField(auto_now=True)
    
    
    def __unicode__(self):
      return u'%s' % (self.text)
    
    
    class Meta:
        ordering = ['-timeDate']
    

class HashTag(models.Model):
    tag = models.CharField(max_length=45)
    timeDate = models.DateTimeField(auto_now=True)
    messages = models.ManyToManyField(Message, blank=True, null=True)
    classroomID = models.IntegerField()
    
    
    def __unicode__(self):
      return u'%s' % (self.tag)

    
class Classroom(models.Model):
    name = models.CharField(max_length=45)
    code = models.CharField(max_length=10)
    messages = models.ManyToManyField(Message, blank=True, null=True)
    allowJoin = models.BooleanField(default=True)
    classOwnerID = models.IntegerField()
    allUserClass = models.BooleanField(default=False)
    description = models.CharField(max_length=210, blank=True, null=True)
    classDate = models.DateField(auto_now=False, blank=True, null=True)
    startTime = models.TimeField(blank=True, null=True)
    endTime = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=45, blank=True, null=True)
    active = models.BooleanField(default=True)
    classLimit = models.IntegerField(default=30)
    classSize = models.IntegerField(default=0)
    classFull = models.BooleanField(default=False)
    
    


    def __unicode__(self):
      return u'%s on: %s from: %s to %s in %s' % (self.name, self.classDate, self.startTime, self.endTime, self.location)
    
    
    class Meta:
        ordering = ['classDate', 'startTime']
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'

class ClassUser(models.Model):
    user = models.ForeignKey(User)
    teacher = models.BooleanField(default=False)
    readOnly = models.BooleanField(default=False)
    messages = models.ManyToManyField(Message, blank=True, null=True)
    classrooms = models.ManyToManyField(Classroom, blank=True, null=True)
    avatarBackColor = models.CharField(max_length=45, blank=True, null=True)
    avatarTextColor = models.CharField(max_length=45, blank=True, null=True)


    def __unicode__(self):
      return u'%s, %s' % (self.user.last_name, self.user.first_name)
    
    
    class Meta:
        ordering = ['user__last_name',]
        verbose_name = 'Session Attendee'
        verbose_name_plural = 'Session Attendees'
    
    
    def user_full_name(self):
        return u'%s, %s' % (self.user.last_name, self.user.first_name)

    user_full_name.allow_tags = True
    user_full_name.admin_order_field = 'user'
    
    
    
    
    
    
    
    
    
    
    
    
    
