from dbModels.models import *
from ldapView import *
import datetime

#general retrival functions

# Name: getAllModules()
# Description: Returns all the module objects
# Parameter: 
# Return: Module[]
def getAllModules():
    return Module.objects.all()

# Name: getPersonListFromArrayList(list)
# Description: Returns a list of Person objects constructed from a list of Person id's
# Parameter: list: UP_ID[]
# Return: Person[]
def getPersonListFromArrayList(list):
    returnlist = []
    for item in list:
        returnlist.append(getPersonFromArr(constructPersonDetails(item)))
    return returnlist

# Name: getAllLecturesOfModule(mod_code)
# Description: Returns the lecturers of a module
# Parameter: mod_code : String
# Return: Person[]
def getAllLecturesOfModule(mod_code):
    list = getLecturorsOf(mod_code)
    return getPersonListFromArrayList(list)

# Name: getAllStudentsOfModule(mod_code
# Description: Returns all the students enrolled in a module
# Parameter: mod_code : String
# Return: Person[]
def getAllStudentsOfModule(mod_code):
    list = getStudentsOf(mod_code)
    return getPersonListFromArrayList(list)

# Name: getAllTAsOfModule(mod_code)
# Description: Returns all the TA's assigned to a module
# Parameter: mod_code : String
# Return: 
def getAllTAsOfModule(mod_code):
    list = getTAsOf(mod_code)
    return getPersonListFromArrayList(list)

# Name:
# Description:
# Parameter: 
# Return: 
def getAllNamesOf(listy):
    list = []
    for x in listy:
        list.append(x.getfirstName())
    return list

# Name:
# Description:
# Parameter: 
# Return: 
def getAllTutorsOfModule(mod_code):
    list = getTutorsOf(mod_code)
    return getPersonListFromArrayList(list)

# Name:
# Description:
# Parameter: 
# Return: 
def getAllMarkersOfModule(mod_code):
    temp = MarkerModule.objects.filter(module=mod_code)
    list =[]
    for x in temp:
        list.append(x.marker_id)
    return list

# Name:
# Description:
# Parameter: 
# Return: 
def createAssessment(request, assessment_name_,assessment_weight_,assessment_type_,module_code_):
    obj = insertAssessment(assessment_name_,assessment_weight_,assessment_type_,module_code_)
    logAudit(request,"Inserted new assessment","insert","dbModels_assessment","id",None,obj.id)

# Name:
# Description:
# Parameter: 
# Return: 
def createLeafAssessment(request, eaf_name_,assessment_id_,max_mark_):
    obj = insertLeafAssessment(leaf_name_,assessment_id_,max_mark_,False)
    logAudit(request,"Inserted new leaf assessment","insert","dbModels_leafassessment","id",None,obj.id)

# Name:
# Description:
# Parameter: 
# Return: 
def getAssessmentForModuleByName(mod_code, name):
    temp = Assessment.objects.filter(module_id=mod_code,assessment_name=name)
    return temp

# Name:
# Description:
# Parameter: 
# Return: 
def getLeafAssessmentOfAssessmentForModuleByName(mod_code, assess_name, leaf_name_):
    temp = getAssessmentForModuleByName(mod_code, assess_name)
    list = []
    if(temp):
        temp2 = LeafAssessment.objects.filter(assessment_id=temp[0], leaf_name=leaf_name_)
        if(temp2):
            list.append(temp2[0])
    return list

# Name:
# Description:
# Parameter: 
# Return: 
def getAllAssessmentsForModule(mod_code):
    temp= Assessment.objects.filter(module_id=mod_code)
    return temp

# Name:
# Description:
# Parameter: 
# Return: 
def getAllOpenAssessmentsForModule(mod_code):
    temp=Assessment.objects.filter(module_id=mod_code)
    list =[]
    for x in temp:
        temp2=getOpenSessions(x.id)
        for item in temp2:
            list.append(item)
    return list

# Name:
# Description:
# Parameter: 
# Return: 
def getAllModulesForStudent(uid):
    return sourceEnrollments(uid)

# Name:
# Description:
# Parameter: 
# Return: 
def getAllModulesForMarker(empl_no):
    temp = MarkerModule.objects.filter(marker_id=empl_no)
    list =[]
    for x in temp:
        temp2=Module.objects.filter(code=x.module)
        if temp2:
            list.append(temp2)
    return list

# Name:
# Description:
# Parameter: 
# Return: 
def getAllModulesForLecturer(uid):
    return sourceLecturerDesignations(uid)

#Assessment specific retrival functions
# Name:
# Description:
# Parameter: 
# Return: 
def getAllLeafAssessmentsForAssessment(assess_code):
  temp = LeafAssessment.objects.filter(assessment_id=assess_code)
  return temp

# Name:
# Description:
# Parameter: 
# Return: 
def getAllAssementsForStudent(empl_no,mod_code):
    temp = MarkAllocation.objects.filter(student=empl_no)
    list = []
    for x in temp:
        temp2 = LeafAssessment.objects.filter(leaf_id=x.leaf_id)
        temp3 = Assessment.objects.filter(assessment_id=temp2.assessment_id)
        if temp3.get() == mod_code:
            list.append(temp3)
    return list

# Name:
# Description:
# Parameter: 
# Return: 
def getAllSessionsForModule(mod_code):
    assessments = getAllAssessmentsForModule(mod_code)
    list = []
    for x in assessments:
        sessions = Sessions.objects.filter(assessment_id=x)
        for y in sessions:
            list.append(y)
    return list

# Name:
# Description:
# Parameter: 
# Return: 
def createSession(mod_code,assess_id, opentime, closetime ):
    obj = insertSessions(mod_code,assess_id,opentime,closetime)
    logAudit(request,"Inserted new session","insert","dbModels_sessions","id",None,obj.id)

# Name:
# Description:
# Parameter: 
# Return: 
def closeSession(request, sess_id):
    try:
        sess = Sessions.objects.get(id=sess_id)
        old = sess.status
        sess.setClose()
        logAuditDetail(request,"Closed session","update","dbModels_sessions","status",old,sess.status,sess.id)
    except Exception, e:
        raise e

# Name:
# Description:
# Parameter: 
# Return: 
def openSession(sess_id):
    try:
        sess = Sessions.objects.get(id=sess_id)
        old = sess.status
        sess.setOpen()
        logAuditDetail(request,"Opened session","update","dbModels_sessions","status",old,sess.status,sess.id)
    except Exception, e:
        raise e

# Name:
# Description:
# Parameter: 
# Return: 
def removeSession(request,sess_id):
    try:
        MarkSess = MarkerSessions.objects.filter(id=sess_id)

        for x in MarkSess:
            oldid0 = x.id
            oldid1 = x.marker_id
            oldid2 = x.session_id_id
            deleteMarkerSessions(x)
            logAuditDetail(request,"Deleted marker session","delete","dbModels_markersessions","id",str(oldid1) + "," + str(oldid2),None,oldid0)
        sess = Sessions.objects.get(id=sess_id)
        MarkAlloc = MarkAllocation.objects.filter(session_id=sess)

        for x in MarkAlloc:
            oldid = x.id
            oldmark = x.mark
            deleteMarkAllocation(x)
            logAuditDetail(request,"Deleted mark allocation","delete","dbModels_markallocation","id",oldmark,None,oldid)

        old = sess.session_name
        oldid = sess.id
        deleteSessions(sess)
        logAuditDetail(request,"Deleted session","delete","dbModels_sessions","id",old,None,sess.id)

    except Exception, e:
        raise e

# Name:
# Description:
# Parameter: 
# Return: 
def removeMarkerFromSession(request, sess_id, uid):
    try:
        MarkSess = MarkerSessions.objects.get(id=sess_id, marker_id=uid)

        oldid0 = MarkSess.id
        oldid1 = MarkSess.marker_id
        oldid2 = MarkSess.session_id_id
        deleteMarkerSessions(MarkSess)
        logAuditDetail(request,"Deleted marker session","delete","dbModels_markersessions","id",str(oldid1) + "," + str(oldid2),None,oldid0)
    except Exception, e:
        raise e	

# Name:
# Description:
# Parameter: 
# Return: 
def removeMarkerFromModule(request, mod_code, uid):
    try:
        sessions = getAllSessionsForModule(mod_code)
        for x in sessions:
            MarkSess = MarkerSessions.objects.filter(id=x.getID(), marker_id=uid)
            for m in MarkSess:
                oldid0 = m.id
                oldid1 = m.marker_id
                oldid2 = m.session_id_id
                deleteMarkerSessions(m)
                logAuditDetail(request,"Deleted marker session","delete","dbModels_markersessions","id",str(oldid1) + "," + str(oldid2),None,oldid0)
        marker = MarkerModule.objects.filter(marker_id=uid,module=mod_code)
        for x in marker:
            oldid0 = x.id
            oldid1 = x.marker_id
            oldid2 = x.module_id
            deleteMarkerModule(x)
            logAuditDetail(request,"Deleted marker module","delete","dbModels_markermodule","id",str(oldid1) + "," + str(oldid2),None,oldid0)
    except Exception, e:
	   raise e	

# Name:
# Description:
# Parameter: 
# Return: 
def getAllAggregatedResultsForStudentOfModule(empl_no, mod_code, level):
  
  return

# Name:
# Description:
# Parameter: 
# Return: 
def login(request, username, password):
  authenticateUser(request,username, password)

# Name:
# Description:
# Parameter: 
# Return: 
def getSessionPerson(request):
  information = request.session["user"]
  return getPersonFromArr(information)


# Name:
# Description:
# Parameter: 
# Return: 
def setMarkerForModule(request, uid, mod_code):
    obj = insertMarkerModule(uid, mod_code)
    logAudit(request,"Inserted new marker for module","insert","dbModels_markermodule","id",None,obj.id)

# Name:
# Description:
# Parameter: 
# Return: 
def setMarkerForSession(request, uid, session_id):
    obj = insertMarkSession(uid, session_id)
    logAudit(request,"Inserted new marker for session","insert","dbModels_markersessions","id",None,obj.id)

# Name:
# Description:
# Parameter: 
# Return: 
def getOpenSessions(assessment_id_):
    temp = Sessions.objects.filter(assessment_id_id=assessment_id_,status=1)
    list = []
    for x in temp:
        list.append(x)
    temp = Sessions.objects.filter(assessment_id_id=assessment_id_,opened__lte=datetime.datetime.now(),closed__gte=datetime.datetime.now(),status=0)
    for x in temp:
        list.append(x)
    return list

# Name:
# Description:
# Parameter: 
# Return: 
def getLeafAssessmentMarksOfAsssessmentForStudent(uid, assess_id):
    leafs = getAllLeafAssessmentsForAssessment(assess_id)
    listMark = []
    for x in leafs:
        
        marks = MarkAllocation.objects.filter(leaf_id=x,student=uid)
        if(marks):
            listMark.append(x.getMax_mark())
            listMark.append(marks[0].getMark())
    
    return listMark

# Name:
# Description:
# Parameter: 
# Return: 
def getAllAssessmentTotalsForStudent(uid, mod_code):
    assessments = getAllAssementsForStudent(uid,mod_code)
    totals = []
    for x in assessments:
        leafMarks = getLeafAssessmentMarksOfAsssessmentForStudent(uid, x)
        total = 0
        mark = 0
        counter = 0
        for m in leafMarks:
            counter = counter + 1
            if (counter % 2 == 0):
                totals = totals + m
            else:
                mark = mark + m 
        totals.append(totals)
        totals.append(marks)
    
    return totals

# Name:
# Description:
# Parameter: 
# Return: 
def populateModules():
    list = getAllModuleCodes()
    for module in list:
        insertModule(module)

# Name:
# Description:
# Parameter: 
# Return: 
def searchBySurname(surname):
    list = findPerson("sn",surname)
    newlist = []
    for uid in list:
        newlist.append(getPersonFromArr(list[uid]))
    return newlist

# Name:
# Description:
# Parameter: 
# Return: 
def searchByName(surname):
    list = findPerson("sn",surname)
    newlist = []
    for uid in list:
        newlist.append(getPersonFromArr(list[uid]))
    return newlist

# Name:
# Description:
# Parameter: 
# Return: 
def getSessionByName(mod_code, name):
    assessments = getAllAssessmentsForModule(mod_code)
    list = []
    for x in assessments:
        sessions = Sessions.objects.filter(assessment_id=x,session_name=name)
        for y in sessions:
            list.append(y)
    return list

# Name:
# Description:
# Parameter: 
# Return: 
def createMarkAllocation(request, leaf_id, session_id, marker, student, timestamp):
    leaf = LeafAssessment.objects.get(id=leaf_id)
    session = Sessions.objects.get(id=session_id)
    obj = insertMarkAllocation(leaf,0,session,marker,student,timestamp)
    logAudit(request,"Inserted new mark allocation","insert","dbModels_markallocation","id",None,obj.id)
    return obj.id

# Name:
# Description:
# Parameter: 
# Return: 
def updateMarkAllocation(request, markAlloc_id, mark):
    try:
        markAlloc = MarkAllocation.objects.get(id=markAlloc_id)
        old = markAlloc.mark
        markAlloc.setMark(mark)
        logAuditDetail(request,"Updated Mark Allocation","update","dbModels_markallocation","mark",old,markAlloc.mark,markAlloc.id)
    except Exception, e:
        raise e

# Name:
# Description:
# Parameter: 
# Return: 
def removeMarkAlloccation(markAlloc_id):
    try:
        markAlloc = MarkAllocation.objects.get(id=markAlloc_id)
        old = markAlloc.mark
        oldid = markAlloc.id
        markAlloc.delete()
        logAuditDetail(request,"Deleted Mark Allocation","delete","dbModels_markallocation","id",old,None,oldid)
    except Exception, e:
        raise e

# Name:
# Description:
# Parameter: 
# Return: 
def getAssessmentFromID(row_id):
        return Assessment.objects.get(id=row_id)

# Name:
# Description:
# Parameter: 
# Return: 
def getLeafAssessmentFromID(row_id):
        return LeafAssessment.objects.get(id=row_id)

# Name:
# Description:
# Parameter: 
# Return: 
def getMarkAllocationFromID(row_id):
        return MarkAllocation.objects.get(id=row_id)

# Name:
# Description:
# Parameter: 
# Return: 
def getMarkerModuleFromID(row_id):
        return Markermodule.objects.get(id=row_id)

# Name:
# Description:
# Parameter: 
# Return: 
def getMarkerSessionsFromID(row_id):
        return Markersessions.objects.get(id=row_id)

# Name:
# Description:
# Parameter: 
# Return: 
def getModuleFromID(row_id):
        return Module.objects.get(id=row_id)

# Name:
# Description:
# Parameter: 
# Return: 
def getSessionsFromID(row_id):
        return Sessions.objects.get(id=row_id)

# Name:
# Description:
# Parameter: 
# Return: 
def getAuditLogFromID(row_id):
    return AuditLog.objects.get(id=row_id)


# Name:
# Description:
# Parameter: 
# Return: 
def getAuditLogFromAction(action):
    actionObj = AuditAction.objects.get(auditDesc=action)
    return AuditLog.objects.filter(action=actionObj)

# Name:
# Description:
# Parameter: 
# Return: 
def getAuditLogFromUsername(username):
    return AuditLog.objects.filter(user_id=username)

# Name:
# Description:
# Parameter: 
# Return: 
def getAuditLogFromTimeRange(fromTime, toTime):
    return AuditLog.objects.filter(time__lte=toTime,time__gte=fromTime)