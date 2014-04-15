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

def createAssessment(assessment_name_,assessment_weight_,assessment_type_,module_code_):
    insertAssessment(assessment_name_,assessment_weight_,assessment_type_,module_code_)

def createLeafAssessment(eaf_name_,assessment_id_,max_mark_):
    insertLeafAssessment(leaf_name_,assessment_id_,max_mark_,False)

def getAssessmentForModuleByName(mod_code, name):
    temp = Assessment.objects.filter(module_id=mod_code,assessment_name=name)
    return temp

def getLeafAssessmentOfAssessmentForModuleByName(mod_code, assess_name, leaf_name_):
    temp = getAssessmentForModuleByName(mod_code, assess_name)
    list = []
    if(temp):
        temp2 = LeafAssessment.objects.filter(assessment_id=temp[0], leaf_name=leaf_name_)
        if(temp2)
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
	insertSessions(mod_code,assess_id,opentime,closetime)

def closeSession(sess_id):
	try:
		sess = Sessions.objects.get(id=sess_id)
		sess.setClose()
	except Exception, e:
		raise e

def openSession(sess_id):
	try:
		sess = Sessions.objects.get(id=sess_id)
		sess.setOpen()
	except Exception, e:
		raise e

def removeSession(sess_id):
    try:
        MarkSess = MarkerSessions.objects.filter(id=sess_id)

        for x in MarkSess:
            deleteMarkerSessions(x)
        sess = Sessions.objects.get(id=sess_id)
        MarkAlloc = MarkAllocation.objects.filter(session_id=sess)

        for x in MarkAlloc:
            deleteMarkAllocation(x)


        deleteSessions(sess)

    except Exception, e:
        raise e

def removeMarkerFromSession(sess_id, uid):
	try:
		MarkSess = MarkerSessions.objects.get(id=sess_id, marker_id=uid)
		deleteMarkerSessions(MarkSess)
	except Exception, e:
		raise e	

def removeMarkerFromModule(mod_code, uid):
    try:
        sessions = getAllSessionsForModule(mod_code)
        for x in sessions:
            MarkSess = MarkerSessions.objects.filter(id=x.getID(), marker_id=uid)
            for m in MarkSess:
               deleteMarkerSessions(m)
        marker = MarkerModule.objects.filter(marker_id=uid,module=mod_code)
        for x in marker:
            deleteMarkerModule(x)
    except Exception, e:
	   raise e	

def getAllAggregatedResultsForStudentOfModule(empl_no, mod_code, level):
  
  return

def login(request, username, password):
  authenticateUser(request,username, password)

def getSessionPerson(request):
  information = request.session["user"]
  return getPersonFromArr(information)


def setMarkerForModule(uid, mod_code):
    insertMarkerModule(uid, mod_code)

def setMarkerForSession(uid, session_id):
    insertMarkSession(uid, session_id)

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
        
        marks = MarkAllocation.objects().filter(leaf_id=x,student=uid)
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

