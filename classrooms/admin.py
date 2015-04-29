from django.contrib import admin
from classrooms.models import Classroom, ClassUser



def lastName(self):
    return self.user.last_name

class ClassroomAdmin(admin.ModelAdmin):
    fields = ('name','allowJoin','classDate','description','startTime','endTime','location','active','classLimit','classSize','classFull')
    list_display = ('classDate','name','allowJoin','startTime','endTime','location','active')
    list_filter = ('classDate','allowJoin','startTime','endTime','location','active')
    search_fields = ['classDate','name','location']



class ClassUserAdmin(admin.ModelAdmin):
    fields = ('teacher','classrooms')
    list_display = ('user_full_name','teacher')
    list_filter = ('teacher',)
    search_fields = ['user__last_name', 'user__first_name']
    
    
    
    
    
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(ClassUser, ClassUserAdmin)