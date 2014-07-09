import time                     # [jacques] For audit logging
import datetime
import json

from django.db import models
from django.http import HttpResponse
from polymorphic import PolymorphicModel


#from ldap.ldap import *

def login(request, username, password):
  personInfo = authenticateUser(username, password)
  
def getSessionPerson(request) :
  information = request.session["user"]
  return getPersonFromArr(information)

def getPersonFromArr(data) :
  information = request.session["user"]
  
  objPerson = Person(data["cn"],data["sn"],data["uid"])
  
  for x in data["studentOf"] :
    sessionPerson.studentOfInsert(item[x])
  
  for x in data["tutorFor"] :
    sessionPerson.tutorOfInsert(x)
  
  for x in data["teachingAssistantOf"] :
    sessionPerson.teachingAssistantOfInsert(x)
  
  for x in data["lectureOf"] :
    sessionPerson.lectureOfInsert(x)
  
  return objPerson

class Aggregator(object):
    def aggregateMarks(self,assessment=[]):
        pass

#pass the numContributer as the constructor's parameter
class BestOfAggregator(Aggregator):
    numContributors = 0
    def __init__(value):
            numContributors = value
            
    def aggregateMarks(self,assessment=[]):
        assessment.sort(reversed)
        total = 0.0
        for x in range(0,self.numContributors ):
            total += assessment[x]
        return (total/self.numContributors)

#pass the array of weights as the constructure's parameter
class WeightedSumAggregator(Aggregator):
    weights = []
    
    def __init__(value):
            weights = value
            
    def aggregateMarks(self,assessment=[]):
        total = 0.0
        for x in assessment:
            total += assessment[x] * self.weights[x]
        return total/len(assessment)

class SimpleSumAggregator(Aggregator):
    def aggregateMarks(self,assessment=[]):
        total = 1.0     #Was 0 initially, there is a chance of division by Zero
        for x in range(len(assessment)):
            total += assessment[x]
        return u'%d' % (total/len(assessment))

class Assessment(PolymorphicModel):
    assess_name = models.CharField(max_length=65)
    published = models.BooleanField()
    mod_id = models.ForeignKey('Module')
    parent = models.IntegerField() #the assess_id of the parent will be passed
    assessment_type = models.CharField(max_length=65)
    
    def getname(self):
        return self.assess_name
    def setname(self,value):
        self.assess_name=value
        self.save()
    def getpublished(self):
        return self.published
    def setpublished(self,value): #Shouldn't value be autehnticated to see if it is indeed a boolean
        self.published=value
        self.save()
    def get_mod_id(self ):
        return self.mod_id
    def get_parent():
      return self.parent
    def is_root(self):
      if self.parent is None:
        return True
      return False
    
    def __unicode__(self):
        return self.assess_name
      
#================================Additional Assessment Function===============================
def insertAssessment(name_,assess_type, mod_code,_parent=None):
#  insertAssessment(assessment_name_,assessment_type_,module_code_, parent=None)
    if parent is None:
      asses = Assessment(name=name_,assessment_type = assess_type, mod_id=mod_code, parent=None) 
    else:
      asses = Assessment(name=name_,assessment_type = assess_type, mod_id=mod_code, parent=_parent)
    asses.save()
    return asses

def getAssessment(): #returns all the assessments stored in the database
    asses = Assessment.objects.all()
    return asses

def deleteAssessment(self):
    Assessment.delete(self)

#===================================End of Assessment Function============================

class Module(models.Model):
    module_code = models.CharField(max_length=6)
    id = models.CharField(max_length = 6, primary_key = True) #module code is used as primary. format COSXXX
    presentation_year = models.DateField(auto_now = True)
    module_name = models.CharField(max_length = 255) #i.e Artificial Intelligence
    
    def getModuleCode(self):
        return self.moduleCode
    def setModuleCode(self,value):
        self.moduleCode=value
        self.save()
        
    def setModuleName(self, value):
      self.module_name = value
      self.save()
    
    def getModuleName(self):
      return self.module_name
    
    def __unicode__(self):
        return u'%s %s' %(self.module_name, self.module_code)
      
#===============================Module Function================================
# [jacques] We need to know who makes insert for logging purposes (Possibly from web services)
def insertModule(code,name,year,assessments_):
    module = Module(moduleCode=code,moduleName=name,presentationYear=year,assessments=assessments_)
    module.save()
    return module

def getAllModules():
    modules = Module.objects.all()
    return modules

def deleteModule(self):
    Module.delete(self)
    
#===============================End of Module Function================================
#Inherits from Assessment using django-polymorphism
class AggregateAssessment(Assessment):
    aggregator_name = models.CharField(max_length = 65)
    session = models.ForeignKey('Sessions')
    isroot = models.BooleanField()
   
    def add_child(self, child_id):
      childAssess = Assessment.objects.filter(Q(Assessment_id=child_id))
      childAssess.set_parent(self.id)
      return true
    
    def get_current_assessment():
      assess = Assessment.objects.filter(Q(Assessment__id=self.id))
      return assess
    
    def get_subassessment(self, sub_id):
      # This traverses through the tree and tries find the object
      sub = Assessment.objects.filter(Q(Assessment__id=sub_id))
      if sub != null:
        return sub
      else:
        #We can change this to throw an exception if that is what we decide on 
        return 'Assessment does not exist'
      
    def get_children(self):
      #make a list of all the children of this assessment and returns that list
      list_ = Assessment.objects.filter(Q(Assessment_parent=self.id))
      return list_
      
    def get_aggregator_name(self):
      #get the name from the database
      return self.aggregator_name
    
    def is_root(self):
      return self.isroot #find a way to determine the root 
    
    def getaggregator(self):
      return self.aggregator
    
    def choose_aggregator(self, agg_key):
      statement = 'Aggregator changed to: '
      if agg_key == 1:
        self.aggregator = SimpleSumAggregator()
        self.aggregator_name = 'S' #fetch name from database... exact format
        statement += 'Simple Sum Aggregator'
        
      elif agg_key == 2:
        self.aggregator = BestOfAggregator()
        self.aggregator_name = 'B' #fetch name from database... exact format
        statement += 'Best of Aggrgator'
        
      elif agg_key == 3:
        self.aggregator = WeightedSumAggregator()
        self.aggregator_name = 'W' #fetch name from database... exact format
        statement += 'Weighted Sum Aggregator'
        
      else:
        statement = 'Throw Exception'
       
      self.save() 
      return statement
    
    def __unicode__(self):
      return self.aggregator_name

#================================AggregateAssessment Function============================
def createAggregateAssessment(name_, published_,aggregator_):
    a = AggregateAssessment(name = name_, published = published_,aggregator=aggregator_)
    a.save()

def getAggregateAssessment(): #gets all aggregate assessments
    aggregate_assessments = AggregateAssessment.objects.all()
    return aggregate_assessments

def deleteAggregateAssessment(self):
    AggregateAssessment.delete(self)

#================================End of AggregateAssessment Function============================

class LeafAssessment(Assessment):
    full_marks = models.IntegerField()
    
    def get_full_marks(self):
      return self.full_marks
    def set_full_marks(self,value):
      self.full_marks=value
      self.save()
    
    def __unicode__(self):
      return 'Mark'

#=================================LeafAssessment Function==============================
def insertLeafAssessment(name_,fullMarks_, parent=None):
    if parent is None:
      a = LeafAssessment(name = name_,full_marks=fullMarks_) 
    else:
      a = LeafAssessment(name = name_,full_marks=fullMarks_ )
      a.set_parent(parent)
    a.save()
    return a

def deleteLeafAssessment(self):
    LeafAssessment.delete(self)

def getLeafAssessment():
    leaf = LeafAssessment.objects.all()
    return leaf
#=================================End of LeafAssessment Function==============================

class Person(models.Model):
    firstName = models.CharField(max_length = 20, null = False)
    upId = models.CharField(max_length = 9, null = False, unique=True)
    surname = models.CharField(max_length = 30, null = False)
    studentOf_module  = models.ManyToManyField(Module, related_name = 'studentOf_module', blank = True)
    tutorOf_module  = models.ManyToManyField(Module, related_name = 'tutorOf_module', blank = True)
    teachingAssistantOf_module  = models.ManyToManyField(Module, related_name = 'teachingAssistantOf_module', blank = True)
    lectureOf_module = models.ManyToManyField(Module, related_name = 'lectureOf_module', blank = True)
    
    def _init_(self,fn, sn, uid):
            self.firstName = fn
            self.upId = uid
            self.surname = sn
    def getFirstName(self):
            return self.firstName
    def getupId(self):
            return self.upId
    def getSurname(self):
            return self.surname
          
    def setFirstName(self,value):
            self.firstName=value
            self.save()
    def setupId(self,value):
            self.upId=value
            self.save()
    def setSurname(self,value):
            self.surname=value
            self.save()
            
    def lectureOfInsert(self,value):
            self.lectureOf_module.append(value)
    def lectureOfDelete(self,value):
            self.lectureOf_module.remove(value)
            
    def studentOfInsert(self,value):
            self.studentOf_module.append(value)
    def studentOfDelete(self,value):
            self.studentOf_module.remove(value)
            
    def tutorOfInsert(self,value):
            self.tutorOf_module.append(value)
    def tutorOfDelete(self,value):
            self.tutorOf_module.remove(value)
            
    def teachingAssistantOfInsert(self,value):
            self.teachingAssistantOf_module.append(value)
    def teachingAssistantOfDelete(self,value):
            self.teachingAssistantOf_module.remove(value)
    
    def isEnrolled(self, mod_code):
            is_true = studentOf_module.objects.filter(module_id=mod_code)
            if is_true is None:
              return False
            return True
            
    def __unicode__(self):
            return u'%s %s %s' % (self.firstName, self.surname, self.upId)


class Person_data(models.Model):
    uid = models.CharField(max_length = 9,unique = True)
    data = models.TextField()
    
    def setuid(self, value):
      self.uid = value
    def getuid(self):
      return self.uid
    def setData(self, value):
      data = value
      self.save()
    def getData(self):
      return self.data
    
    def __unicode__(self):
      return self.uid
    

#==========================Person_data===============================
def insertPerson_data(upId_,data_):
    session = Person_data(uid=upId_,data=data_)
    session.save()
    return session

def getAllPerson_data():
    person = Person_data.objects.all()
    return person

def deletePerson_data(self):
    Person.delete(self)

#==========================Person_data===============================

class MarkAllocation(models.Model):
    comment =models.TextField()
    student = models.ForeignKey('Person')
    assessment =models.ForeignKey('LeafAssessment') 
    marker = models.CharField(max_length=100)
    timeStamp = models.DateTimeField()
    mark = models.IntegerField(max_length=3)
    
    def setMark(self,value):
      self.mark = value
      self.save()
    def getMark(self):
      return self.mark
    
    def setcomment(self,value):
        self.comment=value
        self.save()
    def setLAssessment(self,value):
        self.assessment = value
        self.save()
    def setmarker(self,value):
        self.marker=value
        self.save()
    def setstudent(self,value):
        self.student=value
        self.save()
    def getLAssessment(self):
        return self.assessment
    def getstudent(self):
        return self.student
    def settimeStamp(self,value):
        self.timeStamp=value
        self.save()
    def getcomment(self):
        return self.comment
    def getmarker(self):
        return self.marker
    def gettimeStamp(self):
        return self.timeStamp
      
    def __unicode__(self):
      return self.marker

#===============================MarkAllocation Function================================
def insertMarkAllocation(comment_,marker_,timeStamp_,student_,L_assessment):
    markAlloc = MarkAllocation(comment=comment_,marker=marker_,timeStamp=timeStamp_,student=student_,assessment = L_assessment)
    markAlloc.save()

def getMarkAllocation():
    mark_allocation = MarkAllocation.objects.all()
    return mark_allocation
    
def getMarkAllocation(id):
	return MarkAllocation.object.get(assessment = id)

def deleteMarkAllocation(self):
    MarkAllocation.delete(self)

#===============================End of MarkAllocation Function================================

class Sessions(models.Model):
    assessmentname = models.CharField(max_length=100, null=False)
    session_name = models.CharField(max_length=100, null=False)
    assessment_id = models.ForeignKey('Assessment')
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()
    status = models.IntegerField(default = 0)
    
    def checkStatus(self):
        if open_time < datetime.now() & close_time >= datetime.now():
                status = 1
                return status
        else:
                return status

    def setAssessmentName(self, name):
      self.assessmentname = name
      self.save()

    def setAssessmentID(self,id):
        self.assessment_id = id
        self.save()

    def setOpenedDate(self, date):
        self.open_time = date
        self.save()
    
    def setClosedDate(self, date):
        self.close_time = date
        self.save()
       
    def setOpen(self):
        self.status = 1
        self.save()
    
    def setClose(self):
        self.status = 2
        self.save()
    
    def setName(self,name):
        self.session_name = name
        self.save()
    
    #getters
    def getID(self):
        return self.id
    def getClosedDate(self):
        return self.close_time
    def getOpenedDate(self):
        return self.open_time
    def getAssessmentID(self):
        return self.assessment_id
    def getClosedDate(self):
        return self.closed
    def getStatus(self):
        return self.status
    def getOpenedDate(self):
        return self.opened
    def getName(self):
        return self.session_name
    
    def addStudent(self,studentID):
        insertPersonToSession(studentID,self.ID,1,0)
    
    def deleteStudent(self,value):
        deleteAllocatedPerson(value)
    
    def addMarker(self,markerID):
        insertPersonToSession(markerID,self.ID,0,1)
        
    def deleteMarker(self,vaule):
        deleteAllocatedPerson(value)
        
    def getAssessmentname(self):
        return self.assessmentname
    def setAssessmentname(self,value):
        self.assessmentname=value
        self.save()
    def getsessionStatus(self):
        return self.status
    def setsessionStatus(self,value):
        self.status=value
        self.save()
    """
    def awardMark(self,value):
        if datetime.datetime.now() >= self.getsessionStatus().getClosed(self):
            self.markallocation.setmark(self,0)
            self.markallocation.setcomment(self,"Assessment session is closed")
            self.markallocation.settimeStamp(self,datetime.datetime.now())
        else:
            self.markallocation=value
     """
     
    def __unicode__(self):
          return u'%s' % (self.assessmentname)

def deleteSessions(self):
	Sessions.delete(self)

def insertSessions(session_name_, assessment_id_,opened_,closed_):
	temp = Sessions(session_name=session_name_,assessment_id=assessment_id_,opened=opened_,closed=closed_,status=0)
	temp.save()
	return temp

def getSessions():
	temp=Sessions.objects.all()
	return temp

def getSessions(Id):
	return Sessions.object.get(id= Id)




class AllocatePerson(models.Model):
	person_id = models.ForeignKey('Person')
	session_id = models.ForeignKey('Sessions')
	isStudent = models.BooleanField(default=0)
	isMarker = models.BooleanField(default=0)
	
	def is_Student(self):
		return isStudent
		
	def is_Marker(self):
		return isMarker
		
	def getID(self):
		return self.ID
		
	def getSessionID(self):
		return session_id
		
	def getPersonID(self):
		return person_id
		
	def set_isStudent(self,bool):
		isStudent = bool
		self.save()
		
	def set_isMarker(self, bool):
		isMarker = bool
		self.save()
		
	def set_personID(self, id):
		person_id = id
		self.save()
		
	def set_sessionID(self, id):
		session_id = id
		self.save()

	def __unicode__(self):
		return 'Allocated person'

#==============================AllocatePerson Function==============================
def insertPersonToSession(personID,sessionID,student,Marker):
	temp = AllocatePerson(person_id = personID, session_id = sessionID,isStudent = student, isMarker = Marker)
	temp.save()
	
def getAllocatedPerson():
	return AllocatePerson.object.all()
	
def getAllocatedPerson(sessionID):
	return AllocatePerson.object.filter(session_id = id)
	
def deleteAllocatedPerson(self):
	AllocatePerson.delete(self)
#==============================End of AllocatePerson Function==============================

#----------------------------------------------------------
#-------------------- Audit tables ------------------------
#----------------------------------------------------------

class AuditAction(models.Model):
    auditAction = models.IntegerField()
    auditDesc = models.CharField(max_length=15)
    
    def __unicode__(self):
      return self.auditDesc


class AuditTable(models.Model):
    tableId = models.IntegerField()
    tableName = models.CharField(max_length=50)

    def __unicode__(self):
      return self.tableName



class AuditTableColumn(models.Model):
    auditTableId = models.ForeignKey('AuditTable')
    columnId = models.IntegerField()
    columnName = models.CharField(max_length=30)

    def __unicode__(self):
      return self.columnName

class AuditLog(models.Model):
    person_id = models.ForeignKey('Person')
    description = models.CharField(max_length=50)
    action = models.ForeignKey('AuditAction')
    time = models.DateTimeField()
    audit_table_id = models.ForeignKey('AuditTable',null=True)
    audit_table_column_id = models.ForeignKey('AuditTableColumn',null=True)
    old_value = models.CharField(max_length=255,null=True)
    new_value = models.CharField(max_length=255,null=True)
    affected_table_id = models.IntegerField(null=True)
    
    def __unicode__(self):
      return self.person_id
    

#===================================AuditLog functions====================================

def logAudit(request,desc,act,table,column,old,new):
    p = Person.objects.get(id=request.REQUEST["upId"])
    t = AuditTable.objects.get(tableName=table)
    c = AuditTableColumn.objects.get(columnName=column)
    ti = time.strftime("%Y-%m-%d %H:%M:%S")
    if (column in {3,6,7,8,10,12,21,23,24,26}):     #[jacques] converts int fields to str for display purposes
        old = str(old)
        new = str(new)
    AuditLog(person_id=p,description=desc,action=act,time=ti,audit_table_id=t,audit_table_column_id=c,old_value=old,new_value=new).save()
    


def logAuditDetail(person,desc,act,table,column,old,new,table_id):
    p = Person.objects.get(id=request.REQUEST["id"])
    t = AuditTable.objects.get(tableName=table)
    c = AuditTableColumn.objects.get(columnName=column)
    aa = AuditAction.objects.get(auditDesc=act)
    ti = time.strftime("%Y-%m-%d %H:%M:%S")
    if (column in {3,6,7,8,10,12,21,23,24,26}):     #[jacques] converts int fields to str for display purposes
        old = str(old)
        new = str(new)
    AuditLog(person_id=p,description=desc,action=aa,time=ti,audit_table_id=t,
             audit_table_column_id=c,old_value=old,new_value=new,affected_table_id=table_id).save()

def getAuditlog():
    auditlog = AuditLog.objects.all()
    return auditlog


#===================================End of AuditLog functions====================================


#This is to create the table shown in the master specification giving a
#general idea of how their MySQL database table for courses looks like

class Course(models.Model):
    course_code = models.CharField(max_length = 20, null = False)
    name = models.CharField(max_length = 255, null = False)
    lecturer = models.CharField(max_length = 255, null = False, default = 0)
    description = models.TextField(null = True)
    semster = models.SmallIntegerField(max_length = 6, null = False, default = 0)
    has_webct = models.SmallIntegerField(max_length = 4, null = True)
    year_group = models.IntegerField(max_length = 11, null = True)
    hidden = models.SmallIntegerField(null = False, default = 0)
    last_updated = models.DateTimeField(auto_now_add = False, auto_now = True)
    discussion_board = models.SmallIntegerField(max_length = 4, null = True)
    tutors_allowed = models.SmallIntegerField(max_length = 2, null = True)
    
    def __unicode__(self):
        return self.course_code
    