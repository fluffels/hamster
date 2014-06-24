import time                     # [jacques] For audit logging
import datetime
import json

from django.db import models
from django.http import HttpResponse

from polymorphic import polymorphic_model

#from ldap.ldap import *

def login(request, username, password) :
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

class Aggregator(models.Model):
    def aggregateMarks(self,assessment=[]):
        total = 0.0
        for x in range(len(assessment)):
            total += assessment[x]
        return total/len(assessment)
    def __unicode__(self):
        return "Aggregator"

class BestOfAggregator(Aggregator):
    numContributors = models.IntegerField()
    def aggregateMarks(self,assessment=[]):
        assessment.sort(reversed)
        total = 0.0
        for x in range(0,self.numContributors ):
            total += assessment[x]
        return (total/self.numContributors)
    def getnumContributors(self):
        return self.numContributors
    def setnumContributors(self,value):
        self.numContributors=value
        self.save()
    def __unicode__(self):
        return "BestOfAggregator"
def createBestOfAggregator(numContributors_):
    coA= BestOfAggregator(numContributors=numContributors_)
    coA.save()
    return coA

class WeightedSumAggregator(Aggregator):
    weights = []
    def weightsInsert(self,value):
        self.weights.append(value)
        self.save()
    def weightsDelete(self,value):
        self.weights.remove(value)
    def aggregateMarks(self,assessment=[]):
        total = 0.0
        for x in assessment:
            total += assessment[x] * self.weights[x]
        return total/len(assessment)
    def __unicode__(self):
        return "WeightedSumAggregator"

class SimpleSumAggregator(Aggregator):
    def aggregateMarks(self,assessment=[]):
        total = 0.0
        for x in range(len(assessment)):
            total += assessment[x]
        return total/len(assessment)
    def __unicode__(self):
        return "SimpleSumAggregator"

class Assessment(models.Model):
    name = models.CharField(max_length=65)
    published = models.BooleanField()
    mod_id = models.ForeignKey('Module')
    
    def getname(self):
        return self.name
    def setname(self,value):
        self.name=value
        self.save()
    def getpublished(self):
        return self.published
    def setpublished(self,value):
        self.published=value
        self.save()
        
    def __unicode__(self):
        return self.name
#Assessment Function===============================================================
def insertAssessment(name_,published_):
    asses = Assessment(name=name_,published=published_)
    asses.save()
    return asses

def getAssessment():
    asses = Assessment.objects.all()
    return asses

def deleteAssessment(self):
    Assessment.delete(self)

#Assessment Function===============================================================

class Module(models.Model):
    module_code = models.CharField(max_length=6)
    id = models.CharField(max_length = 6, primary_key = True) #module code is used as primary. format COSXXX
    presentation_year = models.DateField()
    module_name = models.CharField(max_length = 255) #i.e Artificial Intelligence
    
    def getmoduleCode(self):
        return self.moduleCode
    def setmoduleCode(self,value):
        self.moduleCode=value
        self.save()
    def getMarkers(self):
        markersArr = json.loads(self.markerArr)
        return markersArr
    def insertMarkers(self,value):
        markersArr = json.loads(self.markerArr)
        self.markersArr.append(value)
        markers = json.dumps(markersArr)
        self.save()
    def removeMarkers(self,value):
        markersArr = json.loads(self.markerArr)
        self.markersArr.remove(value)
        markers = json.dumps(markersArr)
        self.save()
        
    def getModuleCode(self):
      return self.module_name
    
    def __unicode__(self):
        return u's% s%' %(self.module_name, self.module_code)
      
#Module Function===============================================================
# [jacques] We need to know who makes insert for logging purposes (Possibly from web services)
def insertModule(code,name,year,assessments_):
    module = Module(moduleCode=code,moduleName=name,presentationYear=year,assessments=assessments_)
    module.save()
    return module

def getModule():
    module = Module.objects.all()
    return module

def deleteModule(self):
    Module.delete(self)

class AggregateAssessment(Assessment):
    aggregator = models.ForeignKey(Aggregator)
    aggregator_name = models.CharField(max_length = 65)
    session = models.ForeignKey('AssessmentSession')
    
    def setname(self, value):
      self.aggregator_name = value
      self.save()
    def getname(self):
      return self.aggregator_name
    
    def getaggregator(self):
        return self.aggregator
    def setaggregator(self,value):
        self.aggregator=value
        self.save()

    def __unicode__(self):
        return self.aggregator_name



#AggregateAssessment Function===============================================================
def createAggregateAssessment(name_, published_,aggregator_):#----------------------------------------------------------------------------
    a = AggregateAssessment(name = name_, published = published_,aggregator=aggregator_)
    a.save()
    return a

def getAggregateAssessment():
    agassess = AggregateAssessment.objects.all()
    return agassess

def deleteAggregateAssessment(self):
    AggregateAssessment.delete(self)


class LeafAssessment(Assessment):
    assesssessionlist =[]#assessmentsession
    fullMarks = models.IntegerField()
    def getfullMarks(self):
        return self.fullMarks
    def setfullMarks(self,value):
        self.fullMarks=value
        self.save()
    def assesssessionlistinsert(self,value):
        self.assesssessionlist.append(value)
    def assesssessionlistdelete(self,value):
        self.assesssessionlist.remove(value)
    def __unicode__(self):
        return self.getname()

#LeafAssessment Function===============================================================
def createLeafAssessment(name_, published_,fullMarks_):
    a = LeafAssessment(name = name_, published = published_,fullMarks=fullMarks_ )
    a.save()
    return a

def deleteLeafAssessment(self):
    LeafAssessment.delete(self)

def getLeafAssessment():
    leaf = LeafAssessment.objects.all()
    return leaf
#LeafAssessment Function===============================================================


class SessionStatus(models.Model):
    open = models.DateTimeField()
    closed = models.DateTimeField()
    def getopen(self):
        return self.open
    def setopen(self,value):
        self.open=value
        self.save()
    def getclosed(self):
        return self.closed
    def setclosed(self,value):
        self.closed=value
        self.save()
    def __unicode__(self):
        return self.getopen()+":"+self.getclosed()

#SessionStatus Function===============================================================
def insertSessionStatus(open_,close_,):
    session = SessionStatus(open=open_,close=close_)
    session.save()
    return session

def getSessionStatus(name_):
    session = AssessmentSession.objects.all(name=name_).object.all()
    return session

def deleteSessionStatus(self):
    SessionStatus.delete(self)

#SessionStatus Function===============================================================

class Person(models.Model):
    firstName = ""
    upId = ""
    surname = ""
    studentOf  = [] #module
    tutorOf  = [] #module
    teachingAssistantOf  = [] #module
    lectureOf = [] #module
    
    def _init_(self,fn, sn, uid):
            self.firstName = fn
            self.upId = uid
            self.surname = sn
    def getfirstName(self):
            return self.firstName
    def getupId(self):
            return self.upId
    def getsurname(self):
            return self.surname
    def setfirstName(self,value):
            self.firstName=value
            self.save()
    def setupId(self,value):
            self.upId=value
            self.save()
    def setsurname(self,value):
            self.surname=value
            self.save()
    def lectureOfInsert(self,value):
            self.lectureOf.append(value)
    def lectureOfDelete(self,value):
            self.lectureOf.remove(value)
    def studentOfInsert(self,value):
            self.studentOf.append(value)
    def studentOfDelete(self,value):
            self.studentOf.remove(value)
    def tutorOfInsert(self,value):
            self.tutorOf.append(value)
    def tutorOfDelete(self,value):
            self.tutorOf.remove(value)
    def teachingAssistantOfInsert(self,value):
            self.teachingAssistantOf.append(value)
    def teachingAssistantOfDelete(self,value):
            self.teachingAssistantOf.remove(value)
    def __unicode__(self):
            return self.getfirstName()+" "+self.getsurname()+" "+self.getupId()
#Person Function===============================================================


class Person_data(models.Model):
    uid = models.CharField(max_length = 9)
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

def insertPerson_data(upId_,data_):
    session = Person_data(uid=upId_,data=data_)
    session.save()
    return session

def getPerson_data():
    person = Person_data.objects.all()
    return person

def deletePerson_data(self):
    Person.delete(self)

#Person Function===============================================================

class MarkAllocation(models.Model):
    mark =models.IntegerField()
    comment =models.CharField(max_length=100)
    student = models.ForeignKey(Person)
    marker=models.CharField(max_length=100)
    timeStamp = models.DateTimeField()
    def setmark(self,value):
        self.mark=value
        self.save()
    def setcomment(self,value):
        self.comment=value
        self.save()
    def setmarker(self,value):
        self.marker=value
        self.save()
    def setstudent(self,value):
        self.student=value
        self.save()
    def getstudent(self):
        return self.student
    def settimeStamp(self,value):
        self.timeStamp=value
        self.save()
    def getmark(self):
        return self.mark
    def getcomment(self):
        return self.comment
    def getmarker(self):
        return self.marker
    def gettimeStamp(self):
        return self.timeStamp

#MarkAllocation Function===============================================================

def insertMarkAllocation(mark_,comment_,marker_,timeStamp_,student_):
    markAlloc = MarkAllocation(mark=mark_,comment=comment_,marker=marker_,timeStamp=timeStamp_,student=student_)
    markAlloc.save()
    return markAlloc


def getMarkAllocation():
    markAlloc = MarkAllocation.objects.all()
    return markAlloc

def deleteMarkAllocation(self):
    MarkAllocation.delete(self)


#MarkAllocation Function===============================================================

class AssessmentSession(models.Model):
    Assessmentname = models.CharField(max_length=10)
    sessionStatus = models.ForeignKey(SessionStatus)
    markallocationList =[] #person
    assessment_id = models.ForeignKey('AggregateAssessment')
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()
    session_name = models.CharField(max_length = 65)
    
    def setsessionName(self, value):
      self.session_name = value
      self.save()
    def getsessionName(self):
      return self.session_name
    
    def markallocationListinsert(self,value):
        self.markallocationList.append(value)
    def markallocationListdelete(self,value):
        self.markallocationList.remove(value)
    def getAssessmentname(self):
        return self.Assessmentname
    def setAssessmentname(self,value):
        self.Assessmentname=value
        self.save()
    def getsessionStatus(self):
        return self.sessionStatus
    def setsessionStatus(self,value):
        self.sessionStatus=value
        self.save()
    def awardMark(self,value):
        if datetime.datetime.now() >= self.getsessionStatus().getClosed(self):
            self.markallocation.setmark(self,0)
            self.markallocation.setcomment(self,"Assessment session is closed")
            self.markallocation.settimeStamp(self,datetime.datetime.now())
        else:
            self.markallocation=value
            
    def __unicode__(self):
      return self.session_name

    #AssessmentSession Function===============================================================

def insertAssessmentSession(Assessmentname_,sessionStatus_):
    assesssess = AssessmentSession(Assessmentname=Assessmentname_,sessionStatus=sessionStatus_,)
    assesssess.save()
    return assesssess

def getAssessmentSession():
    assesssess = AssessmentSession.objects.all()
    return assesssess

def deleteAssessmentSession(self):
    AssessmentSession.delete(self)

#AssessmentSession Function===============================================================

#----------------------------------------------------------
#---- Audit tables ----------------------------------------
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
    auditTableId = models.ForeignKey(AuditTable)
    columnId = models.IntegerField()
    columnName = models.CharField(max_length=30)
    
    def __unicode__(self):
      return self.columnName
    


class AuditLog(models.Model):
    person_id = models.ForeignKey(Person)
    description = models.CharField(max_length=50)
    action = models.ForeignKey(AuditAction)
    time = models.DateTimeField()
    audit_table_id = models.ForeignKey(AuditTable,null=True)
    audit_table_column_id = models.ForeignKey(AuditTableColumn,null=True)
    old_value = models.CharField(max_length=255,null=True)
    new_value = models.CharField(max_length=255,null=True)
    affected_table_id = models.IntegerField(null=True)
    
    def __unicode__(self):
      return self.person_id
    

#AuditLog functions=======================================================================

def logAudit(person,desc,act,table,column,old,new):
    p = Person.objects.get(id=person)
    t = AuditTable.objects.get(tableName=table)
    c = AuditTableColumn.objects.get(columnName=column)
    ti = time.strftime("%Y-%m-%d %H:%M:%S")
    if (column in {3,6,7,8,10,12,21,23,24,26}):     #[jacques] converts int fields to str for display purposes
        old = str(old)
        new = str(new)
    AuditLog(person_id=p,description=desc,action=act,time=ti,audit_table_id=t,audit_table_column_id=c,old_value=old,new_value=new).save()
    


def logAuditDetail(person,desc,act,table,column,old,new,table_id):
    p = Person.objects.get(id=person)
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


#AuditLog functions=======================================================================

def authenticateUser(username,passwords):
    if passwords=="123":
        logAudit(1,'Login Success','LOGIN')
        return True
    else:
        logAudit(1,'Login Failed','LOGIN')
        return False
    #LDAP
    
    
    
    
class Sessions(models.Model):
    session_name=models.CharField(max_length=100)
    assessment_id = models.ForeignKey(Assessment)
    opened = models.DateTimeField()
    closed = models.DateTimeField()
    status = models.IntegerField()
    
    def setAssessmentID(self,id):
        self.assessment_id = id
        self.save()

    def setOpenedDate(self, date):
        self.opened = date
        self.save()

    def setClosedDate(self, date):
        self.closed = date
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

    def deleteSessions(self):
          Sessions.delete(self)

    def insertSessions(session_name_, assessment_id_,opened_,closed_):
            temp = Sessions(session_name=session_name_,assessment_id=assessment_id_,opened=opened_,closed=closed_,status=0)
            temp.save()
            return temp

    def getSessions():
            temp=Sessions.objects.all()
            return temp
          
    def __unicode__(self):
        return self.session_name


#This is to create the table shown in the master specification giving a
#general idea of how their MySQL database table for courses looks like

class Course(models.Model):
    code = models.CharField(max_length = 20, null = False)
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
        return self.code
    