from django.contrib import admin

from .models import Course, Person, Assessment, Module, Sessions, Person_data, AuditLog, AuditTableColumn, AuditTable, AuditAction, MarkAllocation, AllocatePerson, AggregateAssessment, LeafAssessment

#Contains 14 tables

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

class SessionsAdmin(admin.ModelAdmin):
    class Meta:
        model = Sessions

admin.site.register(Sessions, SessionsAdmin)


class MarkAllocationAdmin(admin.ModelAdmin):
    class Meta:
        model = MarkAllocation

admin.site.register(MarkAllocation, MarkAllocationAdmin)


class AuditActionAdmin(admin.ModelAdmin):
    class Meta:
        model = AuditAction

admin.site.register(AuditAction, AuditActionAdmin)


class AuditTableAdmin(admin.ModelAdmin):
    class Meta:
        model = AuditTable

admin.site.register(AuditTable, AuditTableAdmin)


class AuditTableColumnAdmin(admin.ModelAdmin):
    class Meta:
        model = AuditTableColumn

admin.site.register(AuditTableColumn, AuditTableColumnAdmin)


class AuditLogAdmin(admin.ModelAdmin):
    class Meta:
        model = AuditLog

admin.site.register(AuditLog, AuditLogAdmin)


class Person_dataAdmin(admin.ModelAdmin):
    class Meta:
        model = Person_data

admin.site.register(Person_data, Person_dataAdmin)

class AllocatePersonAdmin(admin.ModelAdmin):
    class Meta:
        model = AllocatePerson
        
admin.site.register(AllocatePerson, AllocatePersonAdmin)

class AggregateAssessmentAdmin(admin.ModelAdmin):
    class Meta:
        model = AggregateAssessment
        
admin.site.register(AggregateAssessment, AggregateAssessmentAdmin)
    
class LeafAssessmentAdmin(admin.ModelAdmin):
    class Meta:
        model = LeafAssessment
        
admin.site.register(LeafAssessment, LeafAssessmentAdmin)
    

    
