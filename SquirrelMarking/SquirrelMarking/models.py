from django.db import models
import time                     # [jacques] For audit logging
import datetime
#from ldapView import *
class Person:
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

def login(request, username, password):
  personInfo = authenticateUser(username, password)

def getSessionPerson(request):
  information = request.session["user"]
  return getPersonFromArr(information)

def getPersonFromArr(data):

  objPerson = Person(data["cn"],data["sn"],data["uid"])

  for x in data["studentOf"]:
    objPerson.studentOfInsert(x)

  for x in data["tutorFor"]:
    objPerson.tutorOfInsert(x)

  for x in data["teachingAssistantOf"]:
    objPerson.teachingAssistantOfInsert(x)

  for x in data["lecturerOf"]:
    objPerson.lectureOfInsert(x)
  
  return objPerson

class Module(models.Model):
    moduleCode = models.CharField(max_length=6)
    moduleName = models.CharField(max_length=10)
    presentationYear = models.IntegerField()
    def getmoduleCode(self):
        return self.moduleCode
    def setmoduleCode(self,value):
        self.moduleCode=value
        self.save()
    def getmoduleName(self):
        return self.moduleName
    def setmoduleName(self,value):
        self.moduleName=value
        self.save()
    def getpresentationYear(self):
        return self.presentationYear
    def setpresentationYear(self,value):
        self.presentationYear=value
        self.save()
    # Use this to get readable output from shell
    def __unicode__(self):
        return self.moduleName
#Module Function===============================================================
# [jacques] We need to know who makes insert for logging purposes (Possibly from web services)
def insertModule(code,name,year):
    module = Module(moduleCode=code,moduleName=name,presentationYear=year)
    module.save()
    logAuditDetail(1,'Added module','INSERT',1,1,'',code,module.id)
    return module

def getModule():
    module = Module.objects.all()
    return module

def deleteModule(self):
    logAuditDetail(1,'Delete module','Delete',1,1,'',self.getmoduleCode(),self.id)
    Module.delete(self)

def modifyModule(self,code,name,year):
    logAuditDetail(1,'Modify module','Modify',1,1,'',self.getmoduleCode(),self.id)
    self.setmoduleCode(code)
    self.setmoduleName(name)
    self.setpresentationYear(year)

#Module Function===============================================================

class Assessment(models.Model):
    name = models.CharField(max_length=20)
    published = models.BooleanField()
    module = models.ForeignKey(Module)
    head = False

    def setHead(self):
        self.head = True

    def getname(self):
        return self.name
    def setname(self,value):
        self.name=value
    def getpublished(self):
        return self.published
    def setpublished(self,value):
        self.published=value
    def getmodule(self):
        return self.module
    def setmodule(self,value):
        self.module=value

#Assessment Function===============================================================
def insertAssessment(name_,published_,module_):
    asses = Assessment(name=name_,published=published_,module=module_)
    asses.save()
    return asses

def getAssessment():
    asses = Assessment.objects.all()
    return asses

def deleteAssessment(self):
    Assessment.delete(self)

#def modifyAssessment(self,name_,published_,module_):
#    deleteAssessment(self)
#    asses = Assessment(name=name_,published=published_,module=module_)
#    asses.save()
#Assessment Function===============================================================

class AggregateAssessment(Assessment):
    assessList =[]
    def insertassessList(self,value):
        self.assessList.append(value)
    def deleteassessList(self,value):
        self.assessList.remove(value)
    def getAggregateAssessment(self):
        return self.assessList



#AggregateAssessment Function===============================================================
def createAggregateAssessment(name_, published_, module_):#----------------------------------------------------------------------------
    a = AggregateAssessment(name = name_, published = published_, module = module_)
    a.save()
    return a

def modifyAggregateAssessment(self,name_,published_,module_):#------------------------------------------------------------
    deleteAssessment(self)
    asses = AggregateAssessment(name=name_,published=published_,module=module_)
    asses.save()


class LeafAssessment(Assessment):
    assesssessionlist =[]#assessmentsession
    fullMarks = models.IntegerField()
    def getfullMarks(self):
        return self.fullMarks
    def setfullMarks(self,value):
        self.fullMarks=value
    def assesssessionlistinsert(self,value):
        self.assesssessionlist.append(value)
    def assesssessionlistdelete(self,value):
        self.assesssessionlist.remove(value)


#LeafAssessment Function===============================================================
def createLeafAssessment(name_, published_, module_,fullMarks_):
    a = LeafAssessment(name = name_, published = published_, module = module_,fullMarks=fullMarks_ )
    a.save()
    return a

def modifyLeafAssessment(self,name_,published_,module_):#---------------------------------------------------------------
    deleteAssessment(self)
    asses = LeafAssessment(name=name_,published=published_,module=module_)
    asses.save()
#LeafAssessment Function===============================================================


class SessionStatus(models.Model):
    open = models.DateTimeField()
    closed = models.DateTimeField()
    def getopen(self):
        return self.open
    def setopen(self,value):
        self.open=value
    def getclosed(self):
        return self.closed
    def setclosed(self,value):
        self.closed=value

#SessionStatus Function===============================================================
def insertSessionStatus(open_,close_,):
    session = SessionStatus(open=open_,close=close_)
    session.save()

def getSessionStatus(name_):
    session = AssessmentSession.objects.all(name=name_).object.all()
    return session

def deleteSessionStatus(self):
    SessionStatus.delete(self)

def modifySessionStatus(self,open_,close_,):
    deleteSessionStatus(self)
    asses = Assessment(open=open_,close=close_)
    asses.save()

#SessionStatus Function===============================================================

class Person(models.Model):
    firstName = models.CharField(max_length=10)
    upId = models.CharField(max_length=10)
    surname = models.CharField(max_length=10)
    studentOf  = [] #module
    tutorOf  = [] #module
    teachingAssistantOf  = [] #module
    lectureOf = [] #module

    def getfirstName(self):
        return self.firstName
    def getupId(self):
        return self.upId
    def getsurname(self):
        return self.surname
    def setfirstName(self,value):
        self.firstName=value
    def setupId(self,value):
        self.upId=value
    def setsurname(self,value):
        self.surname=value
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
#Person Function===============================================================
def insertPerson(firstName_,upId_,surname_):
    session = Person(firstName=firstName_,upId=upId_,surname=surname_)
    session.save()
    return session

def getPerson():
    person = Person.objects.all()
    return person

def deletePerson(self):
    Person.delete(self)

def modifyPerson(self,firstName_,upId_,surname_):
    deletePerson(self)
    person = Person(firstName=firstName_,upId=upId_,surname=surname_)
    person.save()
#Person Function===============================================================

class MarkAllocation(models.Model):
    mark =models.IntegerField()
    comment =models.CharField(max_length=100)
    marker = models.ForeignKey(Person)
    timeStamp = models.DateTimeField()
    student  = [] #person
    def setmark(self,value):
        self.mark=value
    def setcomment(self,value):
        self.comment=value
    def setmarker(self,value):
        self.marker=value
    def settimeStamp(self,value):
        self.timeStamp=value
    def getmark(self):
        return self.mark
    def getcomment(self):
        return self.comment
    def getmarker(self):
        return self.marker
    def gettimeStamp(self):
        return self.timeStamp
    def studentInsert(self,value):
        self.student.append(self,value)
    def studentDelete(self,value):
        self.student.remove(self,value)

#MarkAllocation Function===============================================================

def insertMarkAllocation(mark_,comment_,marker_,timeStamp_):
    markAlloc = MarkAllocation(mark=mark_,comment=comment_,marker=marker_,timeStamp=timeStamp_)
    markAlloc.save()

def getMarkAllocation():
    markAlloc = MarkAllocation.objects.all()
    return markAlloc

def deleteMarkAllocation(self):
    MarkAllocation.delete(self)

def modifyMarkAllocation(self,mark_,comment_,marker_,timeStamp_):
    deleteMarkAllocation(self)
    markAlloc = MarkAllocation(mark=mark_,comment=comment_,marker=marker_,timeStamp=timeStamp_)
    markAlloc.save()
#MarkAllocation Function===============================================================

class AssessmentSession(models.Model):
    Assessmentname = models.CharField(max_length=10)
    sessionStatus = models.ForeignKey(SessionStatus)
    studentList =[] #person
    leafassessment = models.ForeignKey(LeafAssessment)
    markerLists=[] #person
    markallocation= models.ForeignKey(MarkAllocation)
    def leafassessmentinsert(self,value):
        self.leafassessment.append(self,value)
    def leafassessmentdelete(self,value):
        self.leafassessment.remove(self,value)
    def studentListinsert(self,value):
        self.studentList.append(self,value)
    def studentListdelete(self,value):
        self.studentList.remove(self,value)
    def getAssessmentname(self):
        return self.Assessmentname
    def setAssessmentname(self,value):
        self.Assessmentname=value
    def getsessionStatus(self):
        return self.sessionStatus
    def setsessionStatus(self,value):
        self.sessionStatus=value
    def getleafassessment(self):
        return self.leafassessment
    def setleafassessment(self,value):
        self.leafassessment=value
    def awardMark(self,value):
        if datetime.datetime.now() >= self.getsessionStatus().getClosed(self):
            self.markallocation.setmark(self,0)
            self.markallocation.setcomment(self,"Assessment session is closed")
            self.markallocation.settimeStamp(self,datetime.datetime.now())
        else:
            self.markallocation=value
    def getmarkallocation(self):
        return self.markallocation
    #AssessmentSession Function===============================================================

def insertAssessmentSession(Assessmentname_,sessionStatus_,leafassessment_,markallocation_):
    assesssess = AssessmentSession(Assessmentname=Assessmentname_,sessionStatus=sessionStatus_,markleafassessmenter=leafassessment_,markallocation=markallocation_)
    assesssess.save()

def getAssessmentSession():
    assesssess = AssessmentSession.objects.all()
    return assesssess

def deleteAssessmentSession(self):
    AssessmentSession.delete(self)

def modifyAssessmentSession(self,Assessmentname_,sessionStatus_,leafassessment_,markallocation_):
    deleteAssessmentSession(self)
    assesssess = AssessmentSession(Assessmentname=Assessmentname_,sessionStatus=sessionStatus_,markleafassessmenter=leafassessment_,markallocation=markallocation_)
    assesssess.save()
#AssessmentSession Function===============================================================


class Aggregator(models.Model):
    def aggregateMarks(self,assessment=[]):
        total = 0.0
        for x in range(len(assessment)):
            total += assessment[x]
        return total/len(assessment)


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


class WeightedSumAggregator(Aggregator):
    weights = []
    def weightsInsert(self,value):
        self.weights.append(self,value)
    def weightsDelete(self,value):
        self.weights.remove(self,value)
    def aggregateMarks(self,assessment=[]):
        total = 0.0
        for x in assessment:
            total += assessment[x] * self.weights[x]
        return total/len(assessment)


class SimpleSumAggregator(Aggregator):
    def aggregateMarks(self,assessment=[]):
        total = 0.0
        for x in range(len(assessment)):
            total += assessment[x]
        return total/len(assessment)


#----------------------------------------------------------
#---- Audit tables ----------------------------------------
#----------------------------------------------------------

class AuditAction(models.Model):
    auditAction = models.IntegerField()
    auditDesc = models.CharField(max_length=15)

class AuditTable(models.Model):
    tableId = models.IntegerField()
    tableName = models.CharField(max_length=50)


class AuditTableColumn(models.Model):
    auditTableId = models.ForeignKey(AuditTable)
    columnId = models.IntegerField()
    columnName = models.CharField(max_length=30)


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

#AuditLog functions=======================================================================

def logAudit(person,desc,act,table,column,old,new):
    p = Person.objects.get(id=person)
    t = AuditTable.objects.get(id=table)
    c = AuditTableColumn.objects.get(id=column)
    ti = time.strftime("%Y-%m-%d %H:%M:%S")
    if (column in {3,6,7,8,10,12,21,23,24,26}):     #[jacques] converts int fields to str for display purposes
        old = str(old)
        new = str(new)
    AuditLog(person_id=p,description=desc,action=act,time=ti,audit_table_id=t,audit_table_column_id=c,old_value=old,new_value=new).save()

def getAuditlog():
    auditlog = AuditLog.objects.all()
    return auditlog

def logAuditDetail(person,desc,act,table,column,old,new,table_id):
    p = Person.objects.get(id=person)
    t = AuditTable.objects.get(id=table)
    c = AuditTableColumn.objects.get(id=column)
    aa = AuditAction.objects.get(auditDesc=act)
    ti = time.strftime("%Y-%m-%d %H:%M:%S")
    if (column in {3,6,7,8,10,12,21,23,24,26}):     #[jacques] converts int fields to str for display purposes
        old = str(old)
        new = str(new)
    AuditLog(person_id=p,description=desc,action=aa,time=ti,audit_table_id=t,
             audit_table_column_id=c,old_value=old,new_value=new,affected_table_id=table_id).save()

def logAudit(person,desc,act):
    p = Person.objects.get(id=person)
    aa = AuditAction.objects.get(auditDesc=act)
    ti = time.strftime("%Y-%m-%d %H:%M:%S")
    AuditLog(person_id=p,description=desc,action=aa,time=ti).save()

#AuditLog functions=======================================================================

def authenticateUser(username,passwords):
    return True
    try:
        user = authenticateldapUser(username,password)
        return True
    except e:
        return False
        #LDAP








