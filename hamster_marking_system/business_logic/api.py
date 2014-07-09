import datetime
from django.db.models import get_model
from .models import *
from ldap_interface.ldap_api import *

#general retrival functions
# Name: getAllModules()
# Description: Returns all the module objects
# Parameter: 
# Return: Module[]
def getAllModules():
    return Module.objects.all()

# Name: getPersonObjectListFromArrayList(list)
# Description: Returns a list of Person objects constructed from a list of Person id's
# Parameter: list: UP_ID[]
# Return: Person[]
def getPersonObjectListFromArrayList(list):
    returnlist = []
    for item in list:
        returnlist.append(getPersonFromArr(constructPersonDetails(item))) #ldap_function
    return returnlist 

# Name: getAllLecturesOfModule(mod_code)
# Description: Returns the lecturers of a module
# Parameter: mod_code : String
# Return: Person[]
def getAllLecturesOfModule(mod_code):
    list = getLecturersOf(mod_code) #ldap_function
    return getPersonObjectListFromArrayList(list)

# Name: getAllStudentsOfModule(mod_code
# Description: Returns all the students enrolled in a module
# Parameter: mod_code : String
# Return: Person[]
def getAllStudentsOfModule(mod_code):
    list = getStudentsOf(mod_code)
    return getPersonObjectListFromArrayList(list)

# Name: getAllTAsOfModule(mod_code)
# Description: Returns all the TA's assigned to a module
# Parameter: mod_code : String
# Return: Person[]
def getAllTAsOfModule(mod_code):
    list = getTAsOf(mod_code)
    return getPersonObjectListFromArrayList(list)

# Name: getAllTutorsOfModule(mod_code)
# Description: Returns all the Tutor's assigned to a module
# Parameter: mod_code : String
# Return: Person[]
def getAllTutorsOfModule(mod_code):
    list = getTutorsOf(mod_code)
    return getPersonObjectListFromArrayList(list)

# Name: getAllNamesOf(listy)
# Description: Returns a list of the first names of the Person objects 
# Parameter: listy : Person[]
# Return: String[]
def getAllNamesOf(listy):
    list = []
    for x in listy:
        list.append(x.getFirstName())
    return list

# Name: getAllSurnameOf(list)
# Description: Returns a list of the surname of the Person objects 
# Parameter: list : Person[]
# Return: String[]
def getAllSurnameOf(list):
	surname = []
	for x in list:
		surname.append(x.getSurname())
	return surname
	
# Name: getAllUidOf(list)
# Description: Returns a list of the surname of the Person objects 
# Parameter: list : Person[]
# Return: String[]
def getAllUidOf(list):
	uid = []
	for x in list:
		uid.append(x.getgetupId())
	return uid
# Name: getAllMarkersOfModule(mod_code)
# Description: Returns an array of marker id's that are markers for a specific module
# Parameter: mod_code : String
# Return: String[]
def getAllMarkersOfModule(mod_code):

    tut = getAllTutorsOfModule(mod_code)
    lec = getAllLecturersOfModule(mod_code)
    ta = getAllTAsOfModule(mod_code)
    markers = tut
    markers.append(lec)
    markers.append(ta)
    return markers

# Name: createAssessment(request, assessment_name_,assessment_weight_,assessment_type_,module_code_)
# Description: Creates an assessment object and saves it to the database
# Parameter: request : HTTPRequest
# Parameter: assessment_name_ : String
# Parameter: assessment_weight_ : Integer?
# Parameter: assessment_type_ : String
# Parameter: module_code_ : Object
# Return: Nothing
def createAssessment(request, assessment_name_,assessment_weight_,assessment_type_,module_code_):
    obj = insertAssessment(assessment_name_,assessment_weight_,assessment_type_,module_code_)
    logAudit(request,"Inserted new assessment","insert","dbModels_assessment","id",None,obj.id)

# Name: createLeafAssessment(request, leaf_name_,assessment_id_,max_mark_)
# Description: Creates a leaf assessment object and saves it to tge database
# Parameter: request : HTTPRequest
# Parameter: leaf_name_ : String
# Parameter: assessment_id_ : ?
# Parameter: max_mark_ : Integer
# Return: 
def createLeafAssessment(request, leaf_name_,assessment_id_,max_mark_):
    obj = insertLeafAssessment(leaf_name_,assessment_id_,max_mark_,False)
    logAudit(request,"Inserted new leaf assessment","insert","dbModels_leafassessment","id",None,obj.id)

# Name: getAssessmentForModuleByName(mod_code, name)
# Description: Returns all Assessments according to their name and the module that they belong to
# Parameter: mod_code : Module
# Parameter: name : String
# Return: Assessment[] (This list either contains one element or none if it doesnt exist)
def getAssessmentForModuleByName(mod_code, name):
    temp = Assessment.objects.filter(mod_id=mod_code,assess_name=name) #assuming AND function
    return temp

# Name: getLeafAssessmentOfAssessmentForModuleByName(mod_code, assess_name, leaf_name_)
# Description: Returns all the LeafAssessments according to their name, and the assessments and module they belong to 
# Parameter: mod_code : String
# Parameter: assess_name : String
# Return: LeafAssessment[] (This list either contains one element or none if it doesnt exist)
def getLeafAssessmentOfAssessmentForModuleByName(mod_code, assess_name, leafName): #assess_name must be direct parent of leaf
    temp = getAssessmentForModuleByName(mod_code, assess_name)
    
    if(temp):
        temp2 = LeafAssessment.objects.filter(assessment_id=temp.getId(), leaf_name=leafName)
        if(temp2):
            return temp2
        else:
            return "Will throw an exception"

# Name: getAllAssessmentsForModule(mod_code):
# Description: Returns all Assessments of a module
# Parameter: mod_code : String
# Return: Assessments[]
def getAllAssessmentsForModule(mod_code):
    temp= getAssessments(mod_code) 
    return temp

def getAssessmentDetails(assess):
	list = []
	list.append(assess.id)
	list.append(assess.getname())
	return list
# Name: getAllOpenSessionsForModule(mod_code)
# Description: Returns all the Assessments that have an open session
# Parameter: mod_code : String
# Return: Sessions[]
def getAllOpenSessionsForModule(mod_code):
    temp=Assessment.objects.filter(module_id=mod_code)
    list =[]
    for x in temp:
        openSessions=getOpenSessions(x.id)
        for item in openSessions:
            list.append(item)
    return list

# Name: getAllModulesForStudent(uid)
# Description: Returns all the modules that a student is enrolled for
# Parameter: uid : String
# Return: Array of Modules
def getAllModulesForStudent(uid):
    return sourceEnrollments(uid)

# Name: getAllModulesForMarker(empl_no)
# Description: Returns all the modules that a marker is assigned to
# Parameter: empl_no : String
# Return: 
def getAllModulesForMarker(empl_no):
    temp = sourceTutorDesignations(empl_no)
    temp2 = sourceLecturerDesignations(empl_no)
    modules = sourceTeachingAssistantDesignations(empl_no)
    for i in temp:
        modules.append(i)
    for x in temp2:
        modules.append(x)
    return modules

# Name: getAllModulesForLecturer(uid)
# Description: Returns all the modules that the person is a lecturer of
# Parameter: uid : String
# Return: Array of Modules #empty if not lecturer
def getAllModulesForLecturer(uid):
    return sourceLecturerDesignations(uid)

# Name: getAllLeafAssessmentsForAssessment(assess_code)
# Description: Returns all the LeafAssessments that belong to a specific Assessment
# Parameter: assess_code
# Return: LeafAssessment[]
def getAllLeafAssessmentsForAssessment(assess_code):
  temp = LeafAssessment.objects.filter(assessment_id=assess_code)
  return temp

# Name: getAllAssementsForStudent(empl_no,mod_code)
# Description: Returns all Assessments that a student has been marked for
# Parameter: empl_no : String
# Parameter: mod_code : String
# Return: Assessments[]
def getAllAssementsForStudent(empl_no,mod_code):
    studentMod = getAllModulesForStudent(mod_code)
    for mod in studentMod:
        marked = Assessment.objects.filter(mod_id_id=mod_code, published=True)
    return marked

# Name: getAllSessionsForModule(mod_code)
# Description: Returns all the sessions for a module
# Parameter: mod_code : String
# Return: Sessions[]
def getAllSessionsForModule(mod_code):
    assessments = getAllAssessmentsForModule(mod_code)
    list = []
    for x in assessments:
        sessions = Sessions.objects.filter(assessment_id=x.getId())
        for y in sessions:
            list.append(y)
    return list

def getAllSessionsForAssessment(assess_id):
	assess = getAssessmentFromID(assess_id)
	sessions = Sessions.objects.filter(assessment_id_id=assess)
	return sessions

# Name: createSession(mod_code,assess_id, opentime, closetime )
# Description: Creates a Session object and saves it to the database
# Parameter: session_name : String
# Parameter: assess_id : Assessment
# Parameter: opentime : DateTime
# Parameter: closetime : DateTime
# Return: Boolean
def createSession(request,session_name,assess_id, opentime, closetime ):
    obj = insertSessions(session_name,assess_id,opentime,closetime)
    logAudit(request,"Inserted new session","insert","dbModels_sessions","id",None,obj.id)
    return True
    
def getSessionIdFromObject(session):
	return session.getID()

def getSessionNameFromObject(session)
	return session.getName()

# Name: closeSession(request, sess_id)
# Description: Closes a session therefore no more marking can be done
# Parameter: request : HTTPRequest
# Parameter:  sess_id : Integer
# Return: Boolean
def closeSession(request, sess_id):
    sess = Sessions.objects.get(id=sess_id)
    old = sess.getStatus()
    if old == 1:
        sess.setClose()
        logAuditDetail(request,"Closed session","update","dbModels_sessions","status",old,sess.status,sess.id)
    else:
        return False
    return True

# Name: openSession(request, sess_id)
# Description: Opens a session for marking
# Parameter: request : HTTPRequest
# Parameter: sess_id : Integer
# Return: Boolean
def openSession(request, sess_id):
    sess = Sessions.objects.get(id=sess_id)
    old = sess.getStatus()
    if old == 2:
        sess.setOpen()
        logAuditDetail(request,"Opened session","update","dbModels_sessions","status",old,sess.status,sess.id)
        return True
    else:
        return False

# Name: removeSession(request,sess_id)
# Description: Deletes a marker Session from the database
# Parameter: request : HTTPRequest
# Parameter: sess_id : Integer
# Return: Boolean
def removeSession(request,sess_id):
    try:
        sess =  Sessions.objects.filter(id=sess_id)
        if sess:
            sess.deleteSessions() #exception may be thrown here
            logAuditDetail(request,"Deleted session","delete","business_logic_sessions","id",str(oldid1) + "," + str(oldid2),None,sess.id)
            return True
    except Exception as e:
        raise e
        print 'The session to be deleted does not exist'

# Name: removeMarkerFromSession(request, sess_id, uid)
# Description: Removes a marker from a specific marking Session
# Parameter: request : HTTPRequest
# Parameter: sess_id : Integer
# Parameter: uid : String
# Return: Boolean
def removeMarkerFromSession(request, sess_id, uid):
    try:
        MarkSess = AllocatePerson.objects.get(session_id_id=sess_id, person_id_id=uid)
        marker_id = MarkSess.getId()
        MarkSess.deleteAllocatedPerson()
        logAuditDetail(request,"Deleted marker session","delete","business_logic_allocateperson","id",uid + "," + sess_id,None,marker_id)
    except Exception as e:
        print "Cannot remove marker from session, person or session does not exist."
        raise e

    return True

# Name: removeMarkerFromModule(request, mod_code, uid)
# Description: Removes a marker completely from a module
# Parameter: request : HTTPRequest
# Parameter: mod_code : Integer
# Parameter: uid : String
# Return: Boolean
def removeMarkerFromModule(request, mod_code, uid):
    try:
        sessions = getAllSessionsForModule(mod_code)
        for x in sessions:
            MarkSess = AllocatePerson.objects.filter(session_id_id=x.getId(), person_id_id=uid)
            for m in MarkSess:
                oldid0 = m.id
                oldid1 = uid
                oldid2 = m.session_id_id
                m.delete()
                logAuditDetail(request,"Deleted marker session","delete","dbModels_markersessions","id",str(oldid1) + "," + str(oldid2),None,oldid0)
        markerTa = teachingAssistantOf_module.objects.filter(module_id=mod_code,person_id=uid)
        markerTut = teachingAssistantOf_module.objects.filter(module_id=mod_code,person_id=uid)
        for x in markerTa:
            oldid0 = x.id
            oldid1 = uid
            oldid2 = x.module_id
            x.delete()
            logAuditDetail(request,"Deleted marker module","delete","dbModels_markermodule","id",str(oldid1) + "," + str(oldid2),None,oldid0)

        for y in markerTut:
            oldid0 = y.id
            oldid1 = uid
            oldid2 = y.module_id
            y.delete()
            logAuditDetail(request,"Deleted marker module","delete","dbModels_markermodule","id",str(oldid1) + "," + str(oldid2),None,oldid0)
    except Exception as e:
        print 'Error removing marker from sessions or module, marker/module/session does not exist.'
        raise e
    return True

# Name:
# Description:
# Parameter: 
# Return: 
def getAllAggregatedResultsForStudentOfModule(empl_no, mod_code, level):
  #TODO
  return

# Name: login(request, username, password)
# Description: Authenticates a user for login purposes
# Parameter: request : HTTPRequest
# Parameter: username : String
# Parameter: password : String
# Return: Associative array with Person details
def login(request, username, password):
  return authenticateUser(request,username, password)

# Name: getSessionPerson(request)
# Description: Creates a Person object from associative array
# Parameter: request : HTTPRequest
# Return: Person object
def getSessionPerson(request):
  information = request.session["user"]
  return getPersonFromArr(information)


# Name: setTeachingAssistantForModule(request, uid, mod_code)
# Description: Assigns a teaching assistant for a specific module
# Parameter: request : HTTPRequest
# Parameter: uid : String
# Parameter: mod_code : String
# Return: Boolean
def setTeachingAssistantForModule(request, uid, mod_code):
    try:
        ta = teachingAssistantOf_module(person_id=uid, module_id=mod_code)
        per = Person.objects.filter(Q(upId=uid))
        has_been_set =  per.teachingAssistantOfInsert.add(ta) #should return a boolean
        logAudit(request,"Inserted new marker for module","insert","dbModels_markermodule","id",None,per.id)
    except Exception as e:
        print 'Error, user could not be assigned as teaching assistant.'
        raise e
    return True

# Name: setTutorForModule(request, uid, mod_code)
# Description: Assigns a tutor for a specific module
# Parameter: request : HTTPRequest
# Parameter: uid : String
# Parameter: mod_code : String
# Return: Boolean
def setTutorForModule(request, uid, mod_code):
    try:
        tut = tutorOf_module(person_id=uid, module_id=mod_code)
        per = Person.objects.filter(Q(upId=uid))
        per.tutorOf_module.add(tut) #should return a boolean
        logAudit(request,"Inserted new marker for module","insert","dbModels_markermodule","id",None,per.id)
    except Exception as e:
        print 'Error, user could not be assigned as tutor.'
        raise e
    return True

# Name: setMarkerForSession(request, uid, session_id)
# Description: Assigns a marker for a specific Session
# Parameter: request : HTTPRequest
# Parameter: uid : String
# Parameter: session_id : Integer
# Return: Nothing
def setMarkerForSession(request, uid, session_id):
    obj = insertPersonToSession(uid, session_id,0,1)
    logAudit(request,"Inserted new marker for session","insert","dbModels_markersessions","id",None,obj.getId())

# Name: getOpenSessions(assessment_id_)
# Description: Returns all the sessions that are open for marking
# Parameter: assessment_id : Assessment
# Return: Sessions[]
def getOpenSessions(assessment_id_):
    temp = Sessions.objects.filter(assessment_id_id=assessment_id_)
    list = []
    for x in temp:
        if(x.getStatus() == 1):
            list.append(x)
    return list
    
# Name: getOpenSessions(assessment_id_)
# Description: Returns all the sessions that are open for marking
# Parameter: assessment_id : Assessment
# Return: Sessions[]
def getOpenSessionsForMarker(assessment_id_,marker_id_):
	list = getOpenSessions(assessment_id_)
	listy = []
	for x in list:
		markerS =AllocatePerson.objects.filter(person_id=marker_id_,isMarker=1,session_id =x)
		for m in markerS:
		        sess = m.getSessionID()
		        session = Sessions.object.get(id = sess)
		        listy.append(session)
	return listy

# Name:  getLeafAssessmentMarksOfAsssessmentForStudent(uid, assess_id)
# Description: Returns all marks of a student for a specific assessment
# Parameter: uid : String
# Parameter assess_id : Assessment
# Return: returns 2D list first indices indicate assessment number and second indices consist of [0..2]: [0 ]= Name; [1] = Total; [2]= mark obtained;
def getLeafAssessmentMarksOfAsssessmentForStudent(uid, assess_id):
    leafs = getAllLeafAssessmentsForAssessment(assess_id)
    listMark = []
    
    for x in leafs:
        list = []
        list.append(x.getName())
        list.append(x.getMax_mark())
        try:
            marks = MarkAllocation.objects.filter(leaf_id=x,student=uid)
            list.append(marks.getMark())
            list.append(marks.getID())
        except Exception as e:
            print e
            list.append(-2)
            list.append(-2)
        list.append(x.id)
        listMark.append(list)
    return listMark
    
# Name: getAllAssessmentTotalsForStudent(uid, mod_code)
# Description: Returns all the totals for a specific Assessment?
# Parameter: uid : String
# Parameter: mod_code : String
# Return: returns 2D list first indices indicate assessment number and second indices consist of [0..2]: [0 ]= Name; [1] = Total; [2]= mark obtained;
def getAllAssessmentTotalsForStudent(uid, mod_code):
    assessments = getAllAssementsForStudent(uid,mod_code)
    print assessments
    totals = []
    for x in assessments:
        leafMarks = getLeafAssessmentMarksOfAsssessmentForStudent(uid, x)
        total = 0
        mark = 0
        name = x.assessment_name
        counter = 0
        for m in leafMarks:
            counter = counter + 1
            if (counter % 2 == 0):
                total = total + m[3]
            else:
                mark = mark + m[3]
        list = []
        list.append(name)
        list.append(total)
        list.append(mark)
        totals.append(list)
    
    return totals

# Name: getAssessmentTotalsForStudent(uid, mod_code, assess_id)
# Description: Returns all the totals for a specific Assessment?
# Parameter: uid : String
# Parameter: mod_code : String
# Parameter: assess_id : Integer
# Return: returns 2D list first indices indicate assessment number and second indices consist of [0..2]: [0 ]= Name; [1] = Total; [2]= mark obtained;
def getAssessmentTotalForStudent(uid, mod_code, assess_id):
    assessments = Assessment.objects.filter(id=assess_id)
    totals = []
    for x in assessments:
        leafMarks = getLeafAssessmentMarksOfAsssessmentForStudent(uid, x)        
        total = 0
        mark = 0
        name = x.assessment_name
        counter = 0
        
        for m in leafMarks:
            total = total + m[1]
            mark = mark + m[2]
        list = []
        list.append(name)
        list.append(total)
        list.append(mark)
        totals.append(list)
    
    return totals

# Name: populateModules()
# Description: Populates the database with the modules found in the ldap database
# Parameter: 
# Return: Nothing
def populateModules():
    list = getAllModuleCodes()
    for module in list:
        insertModule(module,"",datetime.date.today().year)#Module name not given initially

# Name: searchBySurname(surname)
# Description: Returns all Persons that have the specific surname
# Parameter: surname : Stirng
# Return: Person[]
def searchBySurname(surname):
    list = findPerson("sn",surname)
    newlist = []
    for uid in list:
        newlist.append(getPersonFromArr(list[uid]))
    return newlist

#?????????
# Name: searchByName(surname)
# Description: Returns all Persons that have the specific name
# Parameter: name : String
# Return: Person[]
def searchByName(name):
    list = findPerson("cn",name)
    newlist = []
    for uid in list:
        newlist.append(getPersonFromArr(list[uid]))
    return newlist

# Name: getSessionByName(mod_code, name)
# Description: Returns all Sessions with a specific name belonging to a specific module
# Parameter: mod_code : String
# Parameter: name : String
# Return: Sessions[]
def getSessionByName(mod_code, name):
    assessments = getAllAssessmentsForModule(mod_code)
    list = []
    for x in assessments:
        sessions = Sessions.objects.filter(assessment_id=x,session_name=name)
        for y in sessions:
            list.append(y)
    return list

# Name: createMarkAllocation(request, leaf_id, session_id, marker, student, timestamp)
# Description: Creates a MarkAllocation object and saves it to the database
# Parameter: request : HTTPRequest
# Parameter: leaf_id : Integer
# Parameter: session_id : Integer
# Parameter: marker : String
# Parameter: student : String
# Parameter: timestamp : DateTime
# Return: Integer (The created objects id)
def createMarkAllocation(request, leaf_id, session_id, marker, student, timestamp):
    
    obj = insertMarkAllocation(leaf_id,0,session_id,marker,student,timestamp)
    logAudit(request,"Inserted new mark allocation","insert","dbModels_markallocation","id",None,obj.id)
    return obj.id

# Name: updateMarkAllocation(request, markAlloc_id, mark)
# Description: Updates the mark of the MarkAllocation object
# Parameter: request : HTTPRequest
# Parameter: markAlloc_id : Integer
# Parameter: mark : Integer
# Return: Boolean
def updateMarkAllocation(request, markAlloc_id, mark):
    try:
        markAlloc = MarkAllocation.objects.get(id=markAlloc_id)
        old = markAlloc.getMark()
        markAlloc.setMark(int(mark))
       
        logAuditDetail(request,"Updated Mark Allocation","update","dbModels_markallocation","mark",old,markAlloc.getMark(),markAlloc_id)
    except Exception as e:
        print e.args
        raise e
    return True
    
# Name: removeMarkAlloccation(markAlloc_id)
# Description: Removes the mark of the MarkAllocation object for a student
# Parameter: markAlloc_id : Integer
# Return: Boolean
def removeMarkAlloccation(markAlloc_id):
    try:
        markAlloc = MarkAllocation.objects.get(id=markAlloc_id)
        old = markAlloc.getMark()
        oldid = markAlloc_id
        markAlloc.delete()
        logAuditDetail(request,"Deleted Mark Allocation","delete","dbModels_markallocation","id",old,None,oldid)
    except Exception as e:
        raise e
    return True

def removeLeafAssessment(request,leaf_id):    
    deleteLeafAssessment(leaf_id)

#Look at 212 book for tree traversals, make this function recursive, alternatively BFS,DFS      
def removeAssessment(request,assess_id):
    try:
        #obtain all the children
	root_ = Assessment.filter.objects(polymorphic_ctype_id=assess_id)
	children_ = Assessment.filter.objects(parent=assess_id)
	for child in children: #check if they are aggregates and if so call recursively
	    pass
	
        assess = getAssessmentFromID(assess_id)
        sessions = Sessions.objects.filter(assessment_id_id = assess)
        for x in sessions:
            removeSession(request,x.id)
        leafs = getAllLeafAssessmentsForAssessment(assess)
        for x in leafs:
            removeLeafAssessment(request,x)
        deleteAssessment(assess)
    except Exception as e:
        raise e
    return True

# Name: getAssessmentFromID(row_id)
# Description: Returns an Assessment object from a specific ID
# Parameter: row_id = Integer
# Return: Assessment object of specific ID
def getAssessmentFromID(assess_id):
        return Assessment.objects.get(id=assess_id)

# Name: getLeafAssessmentFromID(row_id)
# Description: Returns a LeafAssessment object from a specific ID
# Parameter: row_id = Integer
# Return: LeafAssessment object of specific ID
def getLeafAssessmentFromID(assess_id):
        return LeafAssessment.objects.get(id=assess_id)

# Name: getMarkAllocationFromID(row_id)
# Description: Returns a MarkAllocation object from a specific ID
# Parameter: row_id = Integer
# Return: MarkAllocation object of specific ID
def getMarkAllocationFromID(markAlloc_id):
        return MarkAllocation.objects.get(id=markAlloc_id)

# Name: getModuleFromID(row_id)
# Description: Returns a Module object from a specific ID
# Parameter: row_id = Integer
# Return: Module object of specific ID
def getModuleFromID(code_name):
        return Module.objects.get(id=code_name)

# Name: getSessionsFromID(row_id)
# Description: Returns a Sessions object from a specific ID
# Parameter: row_id = Integer
# Return: Sessions object of specific ID
def getSessionsFromID(sess_id):
        return Sessions.objects.get(id=sess_id)

# Name:
# Description:
# Parameter: 
# Return: 
def getAuditLogFromID(audit_id):
    return AuditLog.objects.get(id=audit_id)


# Name:
# Description:
# Parameter: 
# Return: 
def getAuditLogFromAction(action):
    actionObj = AuditAction.objects.get(auditDesc=action)
    return AuditLog.objects.filter(action=actionObj.id)

# Name:
# Description:
# Parameter: 
# Return: 
def getAuditLogFromUsername(username):
    person = Person.objects.filter(upId=username)
    return AuditLog.objects.filter(person_id_id=person.id)

# Name:
# Description:
# Parameter: 
# Return: 
def getAuditLogFromTimeRange(fromTime, toTime):
    return AuditLog.objects.filter(time__lte=toTime,time__gte=fromTime)
    
def getAuditLogFromTimeRangeAndUser(username, fromTime, toTime):
	auditObjects = AuditLog.objects.filter(time__lte=toTime,time__gte=fromTime)
	person = Person.objects.filter(upId=username)
	return auditObjects.objects.filter(person_id_id=person.id)

# Name: getStudentsForASession
# Description:
# Parameter: sess_id_:session Object
# Return:  list of uids e.g ["u1200000", "u12233423"]   
def getStudentsForASession(sess_id_):
	temp = AllocatePerson.objects.filter(sess_id=sess_id_,isStudent = 1)
	list = []
	for x in temp:
	        person = Person.objects.get(id=x.getPersonID())
	        uid = person.getupId()
	        list.append(uid)
	return list

# Name: addStudentToSession
# Description: Adds a student to the session
# Parameter: uid:string, sess_id_:session Object
# Return: None
def addStudentToSession(uid, sess_id):
    try:
        person = Person.objects.filter(upId = uid)
        insertPersonToSession(person.id,sess_id,1,0)
    except Exception as e:
        raise e
    return True

# Name:removeStudentFromSession
# Description: removes the student from the session
# Parameter: uid:string, sess_id_:session Object
# Return:  None
def removeStudentFromSession(uid, sess_id_):
	try:
	        person = Person.objects.filter(upId = uid)
	        stsess = AllocatePerson.objects.get(session_id=sess_id_, student_id=person.id)
	        stsess.deleteAllocatedPerson()
	except Exception as e:
		raise e
	return True

def getMarkAllocationForLeafOfStudent(student_id_, leaf_id_):
    try:
        return MarkAllocation.objects.get(student_id = student_id_, assessment_id = leaf_id_)
    except Exception as e:
        print e.args
        raise e
    return True

def getSessionForStudentForAssessmentOfModule(student_id_, leaf_id):
    try:
        
        leaf = getLeafAssessmentFromID(leaf_id)
        sess = Sessions.objects.filter(assessment_id_id = leaf.parent)
        
        for x in sess:
            j = AllocatePerson.objects.filter(session_id_id = x, person_id = student_id_)
            if (j):
                return x
        return []
    except Exception as e:
        print e.args
        raise e

# Name:
# Description:
# Parameter: 
# Return: 

def getAuditLogFromTableName(tableName_):
    mymodel = get_model('business_logic', tableName_)
    if (mymodel):
        table = AuditTable.objects.get(tableName=mymodel._meta.db_table)
        if (table):
            return AuditLog.objects.filter(audit_table_id=table)
        else:
            raise Exception("Table " + mymodel._meta.db_table + " is not being tracked by the audit log")
    else:
        raise Exception("Table " + tableName_ + " does not exist")

def getTableAudit(alteredTable,dateFrom,dateTo):
	list = getAuditLogFromTableName(alteredTable)
	return list.filter(time__lte=dateTo,time__gte=dateFrom)

def getUserTableAudit(userID,alteredTable,dateFrom,dateTo):
	list = getTableAudit(alteredTable,dateFrom,dateTo)
	return list.filter(person_id=userID)

def logout(request):
    try:
        del request.session['user']
    except Exception as e:
        print 'Error, key used is not already in the session.'
        raise e
    
def checkLeafAssessmentExists(leafAssessmentID):
	a = LeafAssessment.objects.filter(id = leafAssessmentID)
	if (a):
		return True
	else:
		return False
		
def checkSessionExists(sessionId):
	a = Sessions.objects.filter(id = sessionId)
	if (a):
		return True
	else:
		return False

def checkSessionBelongsToAssessment(sessionId, assessmentID):
	a = Sessions.objects.filter(id=sessionId,assessment_id_id=assessmentID)
	if (a):
		return True
	else:
		return False

def isStudentInSession(sessionId, student):
	a = AllocatePerson.objects.filter(session_id = sessionId, person_id = student)
	if (a.isStudent):
		return True
	else:
		return False

def isMarkerInSession(sessionId, pers_id):
	a = AllocatePerson.objects.filter(session_id_id = sessionId, person_id_id= pers_id)
	if (a.isMarker):
		return True
	else:
		return False

def checkMarkAllocationExists(uid, ass_id):
	a = MarkAllocation.objects.filter(student_id= uid, assessment_id=ass_id)
	if (a):
		return True
	else:
		return False
