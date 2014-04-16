from dbModels.models import *
from ldapView import *
import datetime

#general retrival functions

def getAllModules():
    return Module.objects.all()

#module specific retrival functions
def getPersonListFromArrayList(list):
    returnlist = []
    for item in list:
        returnlist.append(getPersonFromArr(constructPersonDetails(item)))
    return returnlist

def getAllLecturesOfModule(mod_code):
    list = getLecturorsOf(mod_code)
    return getPersonListFromArrayList(list)

def getAllStudentsOfModule(mod_code):
    list = getStudentsOf(mod_code)
    return getPersonListFromArrayList(list)

def getAllTAsOfModule(mod_code):
    list = getTAsOf(mod_code)
    return getPersonListFromArrayList(list)

def getAllNamesOf(listy):
    list = []
    for x in listy:
        list.append(x.getfirstName())
    return list

def getAllTutorsOfModule(mod_code):
    list = getTutorsOf(mod_code)
    return getPersonListFromArrayList(list)

def getAllMarkersOfModule(mod_code):
    temp = MarkerModule.objects.filter(module=mod_code)
    list =[]
    for x in temp:
        list.append(x.marker_id)
    return list

def createAssessment(request, assessment_name_,assessment_weight_,assessment_type_,module_code_):
    obj = insertAssessment(assessment_name_,assessment_weight_,assessment_type_,module_code_)
    logAudit(request,"Inserted new assessment","insert","dbModels_assessment","id",None,obj.id)

def createLeafAssessment(request, eaf_name_,assessment_id_,max_mark_):
    obj = insertLeafAssessment(leaf_name_,assessment_id_,max_mark_,False)
    logAudit(request,"Inserted new leaf assessment","insert","dbModels_leafassessment","id",None,obj.id)

def getAssessmentForModuleByName(mod_code, name):
    temp = Assessment.objects.filter(module_id=mod_code,assessment_name=name)
    return temp

def getLeafAssessmentOfAssessmentForModuleByName(mod_code, assess_name, leaf_name_):
    temp = getAssessmentForModuleByName(mod_code, assess_name)
    list = []
    if(temp):
        temp2 = LeafAssessment.objects.filter(assessment_id=temp[0], leaf_name=leaf_name_)
        if(temp2):
            list.append(temp2[0])
    return list

def getAllAssessmentsForModule(mod_code):
    temp= Assessment.objects.filter(module_id=mod_code)
    return temp

def getAllOpenAssessmentsForModule(mod_code):
    temp=Assessment.objects.filter(module_id=mod_code)
    list =[]
    for x in temp:
        temp2=Sessions.objects.filter(assessment_id=x.assessment_id,status=True)#implement
        if temp2:
            list.append(temp2)
    return list

def getAllModulesForStudent(uid):
    return sourceEnrollments(uid)

def getAllModulesForMarker(empl_no):
    temp = MarkerModule.objects.filter(marker_id=empl_no)
    list =[]
    for x in temp:
        temp2=Module.objects.filter(code=x.module)
        if temp2:
            list.append(temp2)
    return list

def getAllModulesForLecturer(uid):
    return sourceLecturerDesignations(uid)

#Assessment specific retrival functions
def getAllLeafAssessmentsForAssessment(assess_code):
  temp = LeafAssessment.objects.filter(assessment_id=assess_code)
  return temp

def getAllAssementsForStudent(empl_no,mod_code):
    temp = MarkAllocation.objects.filter(student=empl_no)
    list = []
    for x in temp:
        temp2 = LeafAssessment.objects.filter(leaf_id=x.leaf_id)
        temp3 = Assessment.objects.filter(assessment_id=temp2.assessment_id)
        if temp3.get() == mod_code:
            list.append(temp3)
    return list

def getAllSessionsForModule(mod_code):
    assessments = getAllAssessmentsForModule(mod_code)
    list = []
    for x in assessments:
        sessions = Sessions.objects.filter(assessment_id=x)
        for y in sessions:
            list.append(y)
    return list

def createSession(mod_code,assess_id, opentime, closetime ):
    obj = insertSessions(mod_code,assess_id,opentime,closetime)
    logAudit(request,"Inserted new session","insert","dbModels_sessions","id",None,obj.id)

def closeSession(request, sess_id):
    try:
        sess = Sessions.objects.get(id=sess_id)
        old = sess.status
        sess.setClose()
        logAuditDetail(request,"Closed session","update","dbModels_sessions","status",old,sess.status,sess.id)
    except Exception, e:
        raise e

def openSession(sess_id):
    try:
        sess = Sessions.objects.get(id=sess_id)
        old = sess.status
        sess.setOpen()
        logAuditDetail(request,"Opened session","update","dbModels_sessions","status",old,sess.status,sess.id)
    except Exception, e:
        raise e

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

def getAllAggregatedResultsForStudentOfModule(empl_no, mod_code, level):
  
  return

def login(request, username, password):
  authenticateUser(request,username, password)

def getSessionPerson(request):
  information = request.session["user"]
  return getPersonFromArr(information)


def setMarkerForModule(request, uid, mod_code):
    obj = insertMarkerModule(uid, mod_code)
    logAudit(request,"Inserted new marker for module","insert","dbModels_markermodule","id",None,obj.id)

def setMarkerForSession(request, uid, session_id):
    obj = insertMarkSession(uid, session_id)
    logAudit(request,"Inserted new marker for session","insert","dbModels_markersessions","id",None,obj.id)

def getOpenSessions(assessment_id_):
    temp = Sessions.objects.filter(assessment_id_id=assessment_id_,status=1)
    list = []
    for x in temp:
        list.append(x)
    temp = Sessions.objects.filter(assessment_id_id=assessment_id_,opened__lte=datetime.datetime.now(),closed__gte=datetime.datetime.now(),status=0)
    for x in temp:
        list.append(x)
    return list

def getLeafAssessmentMarksOfAsssessmentForStudent(uid, assess_id):
    leafs = getAllLeafAssessmentsForAssessment(assess_id)
    listMark = []
    for x in leafs:
        
        marks = MarkAllocation.objects.filter(leaf_id=x,student=uid)
        if(marks):
            listMark.append(x.getMax_mark())
            listMark.append(marks[0].getMark())
    
    return listMark

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

def populateModules():
    list = getAllModuleCodes()
    for module in list:
        insertModule(module)

def searchBySurname(surname):
    list = findPerson("sn",surname)
    newlist = []
    for uid in list:
        newlist.append(getPersonFromArr(list[uid]))
    return newlist

def searchByName(surname):
    list = findPerson("sn",surname)
    newlist = []
    for uid in list:
        newlist.append(getPersonFromArr(list[uid]))
    return newlist

def getSessionByName(mod_code, name):
    assessments = getAllAssessmentsForModule(mod_code)
    list = []
    for x in assessments:
        sessions = Sessions.objects.filter(assessment_id=x,session_name=name)
        for y in sessions:
            list.append(y)
    return list

def createMarkAllocation(request, leaf_id, session_id, marker, student, timestamp):
    leaf = LeafAssessment.objects.get(id=leaf_id)
    session = Sessions.objects.get(id=session_id)
    obj = insertMarkAllocation(leaf,0,session,marker,student,timestamp)
    logAudit(request,"Inserted new mark allocation","insert","dbModels_markallocation","id",None,obj.id)
    return obj.id

def updateMarkAllocation(request, markAlloc_id, mark):
    try:
        markAlloc = MarkAllocation.objects.get(id=markAlloc_id)
        old = markAlloc.mark
        markAlloc.setMark(mark)
        logAuditDetail(request,"Updated Mark Allocation","update","dbModels_markallocation","mark",old,markAlloc.mark,markAlloc.id)
    except Exception, e:
        raise e