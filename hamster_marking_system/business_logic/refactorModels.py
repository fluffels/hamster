#==================Person model class=======================
class Person(models.Model):
    firstName = models.CharField(max_length = 255, null = False)
    upId = models.CharField(max_length = 255, null = False)
    surname = models.CharField(max_length = 255, null = False)
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
        
#==================Person_data model class =======================

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

#==================MarkAllocation model class =======================


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


#==================AssessmentSession model class =======================

class AssessmentSession(models.Model):
    Assessmentname = models.CharField(max_length=10)
    sessionStatus = models.ForeignKey(SessionStatus)
    markallocationList =[] #person

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


#==================AuditAction model class =======================

class AuditAction(models.Model):
    auditAction = models.IntegerField()
    auditDesc = models.CharField(max_length=15)

#==================AuditTable model class =======================

class AuditTable(models.Model):
    tableId = models.IntegerField()
    tableName = models.CharField(max_length=50)

#==================AssessmentSession model class =======================

class AuditTableColumn(models.Model):
    auditTableId = models.ForeignKey(AuditTable)
    columnId = models.IntegerField()
    columnName = models.CharField(max_length=30)
    
#==================AuditLog model class =======================

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

#==================Sessions model class =======================

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
    def __unicode__(self):
        return self.session_name
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


#==================AssessmentSession model class =======================

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

#==================AssessmentSession model class =======================