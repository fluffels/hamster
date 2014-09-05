from django.contrib import admin

from .models import  SimpleSumAggregator, BestOfAggregator, WeightedSumAggregator, Aggregator, Person, Assessment, Module, Sessions, Person_data, MarkAllocation, AllocatePerson, AggregateAssessment, LeafAssessment,  AuditLogAssessment, AuditLogAllocatePerson, AuditLogSession, AuditLogMarkAllocation

'''
class CourseAdmin(admin.ModelAdmin):
    class Meta:
        model = Course

admin.site.register(Course, CourseAdmin)
'''
class AggregatorAdmin(admin.ModelAdmin):
    class Meta:
        model = Aggregator

admin.site.register(Aggregator, AggregatorAdmin)
       
class SimpleSumAggregatorAdmin(admin.ModelAdmin):
    class Meta:
        model = SimpleSumAggregator
        
admin.site.register(SimpleSumAggregator, SimpleSumAggregatorAdmin)
       
class BestOfAggregatorAdmin(admin.ModelAdmin):
    class Meta:
        model = BestOfAggregator
        
admin.site.register(BestOfAggregator, BestOfAggregatorAdmin)

class WeightedSumAggregatorAdmin(admin.ModelAdmin):
    class Meta:
        model = WeightedSumAggregator
        
admin.site.register(WeightedSumAggregator, WeightedSumAggregatorAdmin)

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


class AuditLogAssessmentAdmin(admin.ModelAdmin):
    class Meta:
        model = AuditLogAssessment

admin.site.register(AuditLogAssessment, AuditLogAssessmentAdmin)


class AuditLogAllocatePersonAdmin(admin.ModelAdmin):
    class Meta:
        model = AuditLogAllocatePerson

admin.site.register(AuditLogAllocatePerson, AuditLogAllocatePersonAdmin)

class AuditLogSessionAdmin(admin.ModelAdmin):
    class Meta:
        model = AuditLogSession

admin.site.register(AuditLogSession, AuditLogSessionAdmin)

class AuditLogMarkAllocationAdmin(admin.ModelAdmin):
    class Meta:
        model = AuditLogMarkAllocation

admin.site.register(AuditLogMarkAllocation, AuditLogMarkAllocationAdmin)

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

    
