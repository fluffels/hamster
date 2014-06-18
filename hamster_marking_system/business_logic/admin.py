from django.contrib import admin

from .models import Course, Person, Assessment, Module

class CourseAdmin(admin.ModelAdmin):
    class Meta:
        model = Course
        
admin.site.register(Course, CourseAdmin)
    
class PersonAdmin(admin.ModelAdmin):
    class Meta:
        model = Person
        
admin.site.register(Person, PersonAdmin)

class AssessementAdmin(admin.ModelAdmin):
    class Meta:
        model = Assessment
        
admin.site.register(Assessment, AssessementAdmin)

class ModuleAdmin(admin.ModelAdmin):
    class Meta:
        model = Module
        
admin.site.register(Module, ModuleAdmin)