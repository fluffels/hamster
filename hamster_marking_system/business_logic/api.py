import datetime
from django.db.models import get_model
from polymorphic import PolymorphicModel
from .models import *
from ldap_interface.ldap_api import *

#general retrival functions
# Name: getAllModules()
# Description: Returns all the module objects
# Parameter: 
# Return: Module[]
def getAllModules():
    return Module.objects.all()

def getPersonDetails(username):
    return getPersonFromArr(username)

# Name: getPersonObjectListFromArrayList(list)
# Description: Returns a list of Person objects constructed from a list of Person id's
# Parameter: list: UP_ID[]
# Return: Person[]
def getPersonObjectListFromArrayList(list):
    returnlist = []
    for item in list:
        print "lololololololololololololololololololololo"
        print sourceDemographics(item)
        returnlist.append(getPersonFromArr(constructPersonDetails(item))) #ldap_function
    return returnlist 

#def getPersonObjectListFromArrayList(list):
    

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
# Return: Person[],their uid,cn and sn
def getAllStudentsOfModule(mod_code):
    #For testing purposes ITS NOT ACCESSING LDAP
    print "Mod code is : " + str(mod_code)
    list = Person.objects.all()
    print "Size of list : " + str(len(list))
    module_list = []
    module_needed = None
    modObj = Module.objects.get(id=mod_code)
    print "ModObj : " + str(modObj)
    for per in list:
        print "OKAY!!!" + str(per)
#        print "if " + str(per.studentOf_module) + "==" + str(modObj)
        try:
            module_needed = per.studentOf_module.get(module_code=mod_code)
        except Exception as e:
            print e
        if module_needed:
            module_list.append(getPersonInformation(per))
            print "Added " + str(per)
        else:
            pass
            
    print "Module list :"
    print module_list
    return module_list
    '''
    list = getStudentsOf(mod_code)
    #return getPersonObjectListFromArrayList(list)
    returnList = []
    for item in list:
        person = []
        array = sourceDemographics(item)
        person.append(array['uid'])
        person.append(array['cn'])
        person.append(array['sn'])
        returnList.append(person)
    return returnList
    '''
 
# Name: getAllTAsOfModule(mod_code)
# Description: Returns all the TA's assigned to a module
# Parameter: mod_code : String
# Return: Person[],their uid,cn and sn
def getAllTAsOfModule(mod_code):
    list = getTAsOf(mod_code)
   # return getPersonObjectListFromArrayList(list)
    returnList = []
    for item in list:
        person = []
        array = sourceDemographics(item)
        person.append(array['uid'])
        person.append(array['cn'])
        person.append(array['sn'])
        returnList.append(person)
    return returnList

# Name: getAllTutorsOfModule(mod_code)
# Description: Returns all the Tutor's assigned to a module
# Parameter: mod_code : String
# Return: Person[],their uid,cn and sn
def getAllTutorsOfModule(mod_code):
    list = getTutorsOf(mod_code)
    #return getPersonObjectListFromArrayList(list)
    returnList = []
    for item in list:
        person = []
        array = sourceDemographics(item)
        person.append(array['uid'])
        person.append(array['cn'])
        person.append(array['sn'])
        returnList.append(person)
    
    return returnList

def getPersonsInformation(uid):
    per = Person.objects.get(upId=uid)
    X = getPersonInformation(per)
    return X

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

def getPersonInformation(person):
    students = []
    students.append(person.getupId())
    students.append(person.getFirstName())
    students.append(person.getSurname())
    return students
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

def getAssessmentName(assess_id):
    assess = Assessment.objects.all()
    for ass in assess:
        if str(ass.id) == str(assess_id):
            result = ass.assess_name
    print "********************"
    print result
    print "********************"
    return result

def getModuleNameForAssessment(assess_id):
    assess = Assessment.objects.all()
#    print "------------------------------"
    for ass in assess:
        if(str(ass.id) == str(assess_id)):
            result = ass.mod_id
#            print result.getModuleCode()
#    print "------------------------------"
    return result.getModuleCode()
	
# Name: checkIfAssessmentIsLeaf(asssess_id)
# Description: Checks if the assessment is a leaf assessment
# Parameter: assess_id: String
# Return: Boolean

def checkIfAssessmentIsLeaf(assess_id):
	print "++++++++++++++++++++"
	print assess_id
	assess_objs = Assessment.objects.all()
	for ass in assess_objs:
		if str(ass.id) == str(assess_id):
			print "I do mamelo"
			types = ass.assessment_type
			if str(types) == 'Leaf':
				print "I came, and I...became a leaf"
				return True
	
	return False

def isMarked(leaf_id):
    leaf_obj = Assessment.objects.get(id=leaf_id)
    allLeafsMarks = MarkAllocation.objects.filter(assessment = leaf_id)
    
    for leaf in allLeafsMarks:
        if leaf.mark > -1:
            return True
    return False
# Name: makeLeafAssessmentAnAggregate(old_leaf_id, new_leaf_id)
# Description: Makes the old leaf an aggregate assessment and makes the new leaf its child (assumes that new leaf already exists)
# Parameter: old_leaf_id: String
# Parameter: new_leaf_id: String
# Return: Boolean
def manageSessions(objFrom, objTo):
    objFromSessions = Sessions.objects.filter(assessment_id=objFrom)
    for sess in objFromSessions:
        sess.assessment_id = objTo
        sess.save()
    return True
# Name: makeLeafAssessmentAnAggregate(old_leaf_id, new_leaf_id)
# Description: Makes the old leaf an aggregate assessment and makes the new leaf its child (assumes that new leaf already exists)
# Parameter: old_leaf_id: String
# Parameter: new_leaf_id: String
# Return: Boolean			
def makeLeafAssessmentAnAggregate(old_leaf_id, new_leaf_id):
	all_assessments = Assessment.objects.all()
	old_leaf_obj = None
	new_leaf_obj = None
	for assess in all_assessments:
		if str(assess.id) == str(old_leaf_id):
			old_leaf_obj = assess
			
		if assess.id == new_leaf_id:
			new_leaf_obj = assess
	
	    
	if isMarked(old_leaf_id): #We cannot continue with this function because the assessment cannot become an aggregate because it has marks
	    new_leaf_obj.delete()
	    return None	  # assigned to people
	else:
	    all_marks = MarkAllocation.objects.filter(assessment=old_leaf_id)
	    for mark in all_marks:
	        deleteMarkAllocation(mark)
	    
	if str(old_leaf_obj.assessment_type) == 'Leaf':
	    if str(new_leaf_obj.assessment_type)=='Leaf':
	        #can perform change
	        agg_name = old_leaf_obj.assess_name
	        agg_type = 'Aggregate'
	        agg_mod_code = old_leaf_obj.mod_id
	        agg_published = old_leaf_obj.published
	        agg_aggregator = 'SimpleSum'
	        agg_weight = None
	        agg_parent = old_leaf_obj.parent
	        
	        new_agg_obj = insertAggregateAssessment(agg_name, agg_type, agg_mod_code, agg_published, agg_aggregator, agg_weight, agg_parent) 
	        if new_agg_obj.parent:
	            new_agg_obj.isroot = False
	        new_leaf_obj.parent = new_agg_obj.id
	        new_leaf_obj.save()
	        print new_leaf_obj.parent
	        new_leaf_obj.isroot = False
	        new_leaf_obj.save()
	        new_agg_obj.save()
	        
	        manageSessions(old_leaf_obj, new_leaf_obj)
	        old_leaf_obj.delete()
	        return new_leaf_obj
	else:
		return None

def getParent(leaf_obj):
    print "eeeeee chale am here"
    print leaf_obj
    if leaf_obj == None:
        print "leaf_Obj"
        print leaf_obj
        return None
    else:
        print "parent"
        print leaf_obj.parent
        return leaf_obj.get_parent()

def changeLeafAssessmentFullMark(request,assess_id,mark):
    try:
        assess = Assessment.objects.get(id=assess_id)
        assess.full_marks = mark
        assess.save()
        return True
    except Exception as e:
        raise e


# Name: createLeafAssessment(request, leaf_name_,assessment_type, module_code,published_, full_marks, parent_id)
# Description: Creates a leaf assessment object by calling the function in models
# Parameter: request : HTTPRequest
# Parameter: leaf_name_ : String
# Parameter: assessment_type : String
# Parameter: module_code: String
#Parameter: published_: Boolean
# Parameter: full_marks : Integer
# Parameter: parent_id: Integer
# Return: Boolean
def createLeafAssessment(request, leaf_name_,assessment_type, module_code,published_, full_marks, parent_id ):
	modObj = Module.objects.get(module_code=module_code)
	print "==============="
	print modObj
	print "==============="
	if parent_id is None:
		print "I am None"
		obj = insertLeafAssessment(leaf_name_, assessment_type, modObj, published_, full_marks, parent_id)
#		logAudit(request,"Inserted new leaf assessment","insert","business_logic_leafassessment","id",None,obj.id)
	else:
		print "I am something"
		obj = insertLeafAssessment(leaf_name_, assessment_type, modObj, published_, full_marks, parent_id)
		is_parent_leaf = checkIfAssessmentIsLeaf(parent_id)
		if is_parent_leaf: #means its a leaf and must be changed
			changed = makeLeafAssessmentAnAggregate(parent_id, obj.id)
			if changed == None:
			    return None
			else: return changed
		else:
		    obj.parent = parent_id
		    obj.save()
	if obj:
	    print "bubububububu"
	    print obj
	    return obj
	else: return None

# Name: createAggregateAssessment(request,assessment_name, assessment_type, module_code,published_, aggregator, assessment_weight, parent_id)
# Description: Creates an aggregate assessment object by calling the function in models.
# Parameter: request : HTTPRequest
# Parameter: assessment_name : String
# Parameter: assessment_type : String
# Parameter: module_code: String
# Parameter: published_: Boolean
# Parameter: aggregator : String
# Parameter: assessment_weight: Integer
# Parameter: parent_id: Integer
# Return: Boolean
def createAggregateAssessment(request, assessment_name, assessment_type, module_code, published_, aggregator, assessment_weight, parent_id = None):
	obj = insertAggregateAssessment(assessment_name, assessment_type, module_code, published_, aggregator, assessment_weight, parent_id)
#	logAudit(request, "Inserted new aggregate assessment", "insert", "business_logic_aggregateassessment", "id", None, obj.id)
	return True
	
# Name: getAssessmentForModuleByName(mod_code, name)
# Description: Returns all Assessments according to their name and the module that they belong to
# Parameter: mod_code : Module
# Parameter: name : String
# Return: Assessment[] (This list either contains one element or none if it doesnt exist)
def getAssessmentForModuleByName(mod_code, name):
    temp = Assessment.objects.filter(mod_id=mod_code,assess_name=name) #assuming AND function
    return temp

def getPublishedChildrenAssessmentsForAssessment(assess_id):
    assessments = Assessment.objects.all()
    children = []
    for ass in assessments:
        if str(ass.parent) == str(assess_id):
            if ass.published == True:
                children.append(ass)
    array = []
    for child in children:
        array.append(getAssessmentDetails(child))
    return array


def getChildrenAssessmentsForAssessmemnt(assess_id):
    print "am in heree"
    assessments = Assessment.objects.all()
    children = []
    for ass in assessments:
        print ass
        if str(ass.parent) == str(assess_id):
            print ass
            children.append(ass)
    array = []
    for child in children:
        array.append(getAssessmentDetails(child))
    return array
        

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
    #temp= getAssessments(mod_code)
    print "am in"
    temp = Assessment.objects.filter(mod_id = mod_code)
    print temp
    assessment = []
    for x in temp:
        if x.parent is None:
            assessment.append(x)
    print assessment
    return assessment

def getAssessmentDetails(assess):
	list = []
	list.append(assess.id)
	list.append(assess.getname())
	list.append(assess.getpublished())
	return list

def getAssessmentPublishStatus(assess):
    ass_obj = Assessment.objects.get(id=assess.id)
    status = ass_obj.getpublished()
    return status

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
def getAllAssessmentsForStudent(mod_code):
    print "==========================================="
    print 'GETTING ALL THE ASSESSMENTS'
    print mod_code
   
    mod_obj = Module.objects.get(id=str(mod_code))
    print "mod_obj: " + str(mod_obj)
    print '==================================='
    assessments = Assessment.objects.filter(mod_id=mod_obj)
    print 'Assessments: ' + str(assessments)
    return assessments
    '''  for mod in studentMod:
        marked = Assessment.objects.filter(mod_id=mod_code, published=True)
    return marked'''
    
def getChildAssessmentOfAssessmentForStudent(assess_id,stud):
    assess = Assessment.objects.get(id = assess_id)
    done = []
    person = Person.objects.get(upId=stud)
    if assess.assessment_type == 'Leaf':
        mark = MarkAllocation.objects.get(assessment=assess,student=person)
        done.append('leaf')
        done.append(mark.mark)
        done.append(assess.full_mark)
        return done
    else:
        children = Assessment.objects.filter(parent=assess_id)
        done.append('Aggregate')
        done.append(children)


# Name: getAllSessionsForModule(mod_code)
# Description: Returns all the sessions for a module
# Parameter: mod_code : String
# Return: Sessions[]
def getAllSessionsForModule(mod_code):
    module = Module.objects.get(id=mod_code)
    assessments = Assessment.objects.filter(mod_id=module)
    print "we are the assessments"
    print assessments
    list = []
    for x in assessments:
        sessions = Sessions.objects.filter(assessment_id=x.id)
        for y in sessions:
            list.append(y)
    return list

def getAllSessionForMarker(mod_code,marker):
    sessions = getAllSessionsForModule(mod_code)
    person = Person.objects.get(upId=marker)
    session = []
    print "huh i dnt know wats happending"
    if sessions:
        print sessions
        for sess in sessions:
            marker = AllocatePerson.objects.filter(person_id=person,session_id=sess.id,isMarker=1)
            if marker:
                session.append(getSessionDetails(sess))
    return session

def getLeafAssessmentOfAssessmentBySession(session_id):
    session = Sessions.objects.get(id=session_id)
    assessment = session.assessment_id
    return getLeafAssessmentOfAssessment(assessment)

def getAllSessionsForAssessment(assess_id):
	assess = getAssessmentFromID(assess_id)
	sessions = Sessions.objects.filter(assessment_id_id=assess)
	return sessions

def getLeafAssessmentOfAssessment(assessment):
    assessments = []
    if assessment.assessment_type == 'Leaf':
        assessments.append(getAssessmentDetails(assessment))
        return assessments
    else:
        children = Assessment.objects.filter(parent=assessment.id)
        for child in children:
            if child.assessment_type == 'Leaf':
                assessments.append(getAssessmentDetails(child))
            else:
                assessments.append(getLeafAssessmentOfAssessment(child))
        return assessments
        
def getSessionDetails(session):
    list = []
    list.append(session.id)
    list.append(session.getName())
    return list

def getSessionObject(sess):
    return Sessions.objects.get(id=sess)

def getSessionName(sess_id):
    sess = Sessions.objects.get(id = sess_id)
    if sess:
        return sess.getName()
    else:
        return ''
    
def getSessionStatus(sessObj):
    return sessObj.checkStatus()
    
# Name: closeSession(request, sess_id)
# Description: Closes a session therefore no more marking can be done
# Parameter: request : HTTPRequest
# Parameter:  sess_id : Integer
# Return: Boolean
def closeSession(request, sess_id):
    print "closeSession::::::::::::::"
    sess = Sessions.objects.get(id=sess_id)
    old = sess.getStatus()
    if old == 1:
        print "IF iS MY MIDDLE NAME..."
        sess.setClose()
#        Detail(request,"Closed session","update","dbModels_sessions","status",old,sess.status,sess.id)
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
    if old == 0:
        sess.setOpen()
#        logAuditDetail(request,"Opened session","update","dbModels_sessions","status",old,sess.status,sess.id)
        return True
    else:
        return False

# Name: publishAssessment(request, sess_id)
# Description: Publishes an assessment
# Parameter: request : HTTPRequest
# Parameter: sess_id : Integer
# Return: Boolean
def publishAssessment(request, assess_id):
    ass = Assessment.objects.get(id=assess_id)
    old = ass.getpublished()
    if old == True:
        return old
        #Do nothing, assessment is already published
#        logAuditDetail(request,"Opened session","update","dbModels_sessions","status",old,sess.status,sess.id)
    else:
        ass.published = True
        ass.save()
        return old
    
# Name: unpublishAssessment(request, sess_id)
# Description: Un-publishes an assessment
# Parameter: request : HTTPRequest
# Parameter: sess_id : Integer
# Return: Boolean
def unpublishAssessment(request, assess_id):
    ass = Assessment.objects.get(id=assess_id)
    old = ass.getpublished()
    if old == True:
        ass.published = False
        ass.save()
        return old
        #Do nothing, assessment is already published
#        logAuditDetail(request,"Opened session","update","dbModels_sessions","status",old,sess.status,sess.id)
    else:
        return old

# Name: removeSession(request,sess_id)
# Description: Deletes a marker Session from the database
# Parameter: request : HTTPRequest
# Parameter: sess_id : Integer
# Return: Boolean
def removeSession(request,sess_id):
    try:
        print "how come i dnt delete bathond" + str(sess_id)
        sess =  Sessions.objects.get(id=sess_id)
        person = AllocatePerson.objects.filter(session_id=sess)
        if sess:
            if len(person)> 0:
                for per in person:
                    per.delete()
            sess.delete() #exception may be thrown here
#            logAuditDetail(request,"Deleted session","delete","business_logic_sessions","id",str(oldid1) + "," + str(oldid2),None,sess.id)
            return True
        else:
            return False
    except Exception as e:
        raise e

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
#        logAuditDetail(request,"Deleted marker session","delete","business_logic_allocateperson","id",uid + "," + sess_id,None,marker_id)
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
#                logAuditDetail(request,"Deleted marker session","delete","dbModels_markersessions","id",str(oldid1) + "," + str(oldid2),None,oldid0)
        markerTa = teachingAssistantOf_module.objects.filter(module_id=mod_code,person_id=uid)
        markerTut = teachingAssistantOf_module.objects.filter(module_id=mod_code,person_id=uid)
        for x in markerTa:
            oldid0 = x.id
            oldid1 = uid
            oldid2 = x.module_id
            x.delete()
#            logAuditDetail(request,"Deleted marker module","delete","dbModels_markermodule","id",str(oldid1) + "," + str(oldid2),None,oldid0)

        for y in markerTut:
            oldid0 = y.id
            oldid1 = uid
            oldid2 = y.module_id
            y.delete()
#            logAuditDetail(request,"Deleted marker module","delete","dbModels_markermodule","id",str(oldid1) + "," + str(oldid2),None,oldid0)
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
#        logAudit(request,"Inserted new marker for module","insert","dbModels_markermodule","id",None,per.id)
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
#        logAudit(request,"Inserted new marker for module","insert","dbModels_markermodule","id",None,per.id)
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
#    logAudit(request,"Inserted new marker for session","insert","dbModels_markersessions","id",None,obj.getId())

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
def createMarkAllocation(request, leaf_id, marker, student, timestamp,comment):
    objL = Assessment.objects.get(id=leaf_id)
    #per = Person.objects.get(upId = student)
    obj = insertMarkAllocation(objL,-1,marker,student,timestamp,comment)
#    logAudit(request,"Inserted new mark allocation","insert","dbModels_markallocation","id",None,obj.id)
    return obj

def getFullMark(assess_id):
    obj = Assessment.objects.get(id=assess_id)
    return obj.full_marks

# Name: updateMarkAllocation(request, markAlloc_id, mark)
# Description: Updates the mark of the MarkAllocation object
# Parameter: request : HTTPRequest
# Parameter: markAlloc_id : Integer
# Parameter: mark : Integer
# Return: Boolean
def updateMarkAllocation(request, student, leaf_id,mark):
    marker = request.session['user']['uid'][0]
    try:
        #markAlloc = MarkAllocation.objects.get(id=markAlloc_id)
       # assess = Assessment.objects.get(id=leaf_id)
        per = Person.objects.get(upId=student)
        leaf = Assessment.objects.get(id=leaf_id)
        if int(mark) <=leaf.full_marks:
            if int(mark) >= 0:
                print "if " + mark + " <= " + leaf.full_marks
                markAlloc = MarkAllocation.objects.get(assessment=leaf_id,student=per.id)
                old = markAlloc.getMark()
                markAlloc.setMark(int(mark))
                markAlloc.setmarker(marker)
                return True
        else:
            print "MaRK IS WRONG"
            return False
#        logAuditDetail(request,"Updated Mark Allocation","update","dbModels_markallocation","mark",old,markAlloc.getMark(),markAlloc_id)
    except Exception as e:
        print e.args
        raise e
    
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
#        logAuditDetail(request,"Deleted Mark Allocation","delete","dbModels_markallocation","id",old,None,oldid)
    except Exception as e:
        raise e
    return True

def removeLeafAssessment(request,leaf_id):    
    deleteLeafAssessment(leaf_id)
    
def makeAggregateAssessmentALeaf(assess_id): #assumes agg_obj has no children
    try:
        agg_obj = Assessment.objects.get(id=assess_id)
        children = Assessment.objects.filter(parent=assess_id)
        sessions = Sessions.objects.filter(assessment_id=assess_id)
        if agg_obj:
            print "AGG OBJ FOUND TO BE: "+ str(agg_obj)
            if len(children) == 0:
                print "HAS NO CHILDREN"
                try:
                    name_ = agg_obj.assess_name
                    assessment_type_ = 'Leaf'
                    module_code = agg_obj.mod_id
                    published_ = agg_obj.published
                    fullMarks_ =0
                    parent = agg_obj.parent
                    print "PARENT IS : " + str(parent)
                    newLeafObj = insertLeafAssessment(name_,assessment_type_, module_code, published_, fullMarks_, parent)
                    manageSessions(agg_obj, newLeafObj)
                    agg_obj.delete()
                except Exception as e:
                    raise e #there is still atleast one child

    except Exception as e:
        raise e  #object did not exist
    
    return newLeafObj
    
    
#Look at 212 book for tree traversals, make this function recursive, alternatively BFS,DFS
# Name: removeAssessment(request, assess_id)
# Description: Removes an assessment and all its children from the database
# Parameter: request : HttpRequest
# Parameter: assess_id : String
# Return: Boolean
def removeAssessment(request,assess_id):
    
    root_ = Assessment.objects.get(id=assess_id)
    print "root_ = " + str(root_)
    print "root_.parent = " + str(root_.parent)
    if root_.parent is None:
        print "CANT GO IN HERE MARA"
        par = None
        if isAggregate(root_.id):
            print "isAggregate == " + str("True")
            children_ = Assessment.objects.filter(parent=assess_id)
            print "HERE ARE MY YOUNG ONES : " + str(children_)
            deleteAssessmentSessions(root_)
            deleteAllChildren(children_)
            print "THEY SHOULD BE GONE TO COLLEGE"
        else:
            print "isAggregate == " + str("False")
            deleteAssessmentSessions(root_)
        root_.delete()
          
    else:
        print "MUST BE HERE"
        par = root_.parent
        childrenOfParent = Assessment.objects.filter(parent = par)
        print "LENGTH OF CHILDREN OF PARENT:" + str(len(childrenOfParent))
        if isAggregate(root_.id):        
            children_ = Assessment.objects.filter(parent=assess_id)
            deleteAssessmentSessions(root_)
            deleteAllChildren(children_)
        else:
            deleteAssessmentSessions(root_)    
        root_.delete()
 
        if len(childrenOfParent) == 1: #means the aggregate is the only child
           print "Making agg a leaf..."
           part= makeAggregateAssessmentALeaf(par)
           par = part.id
           print "Made agg a leaf..." + str(part.id)

    return par

# Name: deleteAssessmentSessions(assessObj)
# Description: Deletes all the sessions of that particular assessment 
# Parameter: assessObj : Asssessment object
# Return: Boolean
def deleteAssessmentSessions(assessObj):
    sessions = Sessions.objects.filter(assessment_id=assessObj)
    if sessions: #assessment has sessions created
        for sess in sessions:
            sess.delete()

    return True

# Name: isAggregate(assessmentObj)
# Description: Checks if the assessment is an aggregate 
# Parameter: assessmentObj : Asssessment object
# Return: Boolean
def isAggregate(assessmentObj):
    #check if assessment exists
    try:
        possible_children = Assessment.objects.filter(parent=assessmentObj)
        print "possible_children = " + str(possible_children)
        
        if len(possible_children) == 0:
            return False #not an aggregate
        return True
    except Exception as e:
        raise e #assessment does not exist
    
# Name: deleteAllChildren(childrenArray)
# Description: Recursive DFS that deletes all assessments, leafs and aggregates
# Parameter: childrenArray : Asssessment[]
# Return: Boolean
def deleteAllChildren(childrenArray):
    try:
        for child in childrenArray:
            print "Deleting : " + str(child.assess_name)
            deleteAssessmentSessions(child)
            if (isAggregate(child.id)):
                print str(child.assess_name) + " is Aggregate...so"
                child_children = Assessment.objects.filter(parent=child.id)
                print "CHILD CHILDREN : " + str(child_children)
                if len(child_children) > 0:
                    deleteAllChildren(child_children) #recursion
                    child.delete()

            else:
                print "Adios amigo!"
                child.delete()
    except Exception as e:
        raise e #no children to delete
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


def getMarkerForSession(sess_id_):
    temp = AllocatePerson.objects.filter(session_id=sess_id_,isMarker = 1)
    list = []
    for x in temp:
        person = Person.objects.get(id=x.getPersonID().id)
        uid = getPersonInformation(person)
        list.append(uid)
    return list
    


def getUserInformation(lists):
   
    user = []
    for x in lists:
        per = []
        person = Person.objects.get(upId=x)
        per.append(x)
        per.append(person.getFirstName())
        per.append(person.getSurname())
        user.append(per)
    return user
        
def getStudentMarks(request,student,assess):
    assessments = Assessment.objects.get(id = assess)
    students = []
    for n in student:
        array = []
        per = Person.objects.get(upId=n)
        mark = MarkAllocation.objects.get(student=per,assessment=assessments)
        if mark:
            array.append(n)
            array.append(per.getFirstName())
            array.append(per.getSurname())
            array.append(mark.mark)
            students.append(array)
        else:
            createMarkAllocation(request,assess,"no marker",n,datetime.datetime.now(),"no mark awarded")
            array.append(n)
            array.append(per.getFirstName())
            array.append(per.getSurname())
            array.append(-1)
            students.append(array)
    return students

def getAssessmentFullMark(assess_id):
    assess = Assessment.objects.get(id=assess_id)
    return assess.full_marks

# Name: addStudentToSession
# Description: Adds a student to the session
# Parameter: uid:string, sess_id_:session Object
# Return: None
def addStudentToSession(uid, sess_id):
    try:
        sessObj = Sessions.objects.get(id=sess_id)
        person = Person.objects.get(upId = uid)
        insertPersonToSession(person,sessObj,1,0)
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

def getMarkForStudents(request, studentsArray, leaf_id):
    finalArray = []
    print 'NAAAAAAAZZZZZZZZZZZOOOOOOOOO'
    print studentsArray
    leafObj = Assessment.objects.get(id=leaf_id)
    print leafObj
    comment = "No comment"
    for student in studentsArray:
        per = Person.objects.get(upId=student[0])
        has = isMarkGiven(per, leaf_id)
        if has == False:
            mark_created = createMarkAllocation(request, leaf_id,"No marker", per, datetime.datetime.now(),comment)
            mark = mark_created.getMark()
        else:
            markAlloc = getMarkAllocationForLeafOfStudent(per, leafObj)
            mark = markAlloc.getMark()
        studentArray =[]
        studentArray.append(student[0])
        studentArray.append(student[1])
        studentArray.append(student[2])
        studentArray.append(mark)
        finalArray.append(studentArray)
    return finalArray

def isMarkGiven(student,leaf_id):
    all_marks = MarkAllocation.objects.all()
    leafObj = Assessment.objects.get(id=leaf_id)
    print "Get all together" +str(leafObj)
    for mark in all_marks:
        print "Get all together"
      #  if (mark.assessment == leafObj) & (mark.student==student):
            #return True
        print "Get all together"
    return False

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


# Name: createSession(mod_code,assess_id, opentime, closetime )
# Description: Creates a Session object and saves it to the database
# Parameter: session_name : String
# Parameter: assess_id : Assessment
# Parameter: opentime : 
def createSession(request,session_name,assess_id, opentime, closetime ):
    sessionObj = Assessment.objects.get(id=assess_id)
    obj = insertSessions(session_name,sessionObj,opentime,closetime)
#    logAudit(request,"Inserted new session","insert","dbModels_sessions","id",None,obj.id)
    return True

######################### MARKER VIEW FUNCTIONS ################################

def getSessionForMarker(mod,marker_id):
    module = Module.objects.get(id=mod)
    assess = Assessment.objects.get(assess_name="Final Mark", mod_id=module)
    assessSession = checkAssessmentSession(assess)
    finalarray = []
    if assessSession == None:
        return None
    else:
        session = Sessions.objects.filter(assessment=assessSession)
        for n in session:
            array = []
            status = n.checkStatus()
            if status == 1:
                bool = validateIfMarkerCanViewSession(marker_id,n.id)
                if bool == True:
                    Studentarray = getStudentsForASession(n)
                    array.append(assessSession)
                    array.append(n)
                    array.append(Studentarray)
                finalarray.append(array)
        return finalarray

def getLeaf(assessment):
    pass
    
def getModuleLeafAssessment(mod,marker_id):
    final = getSessionForMarker(mod,marker_id)
    for n in final:
        leaf=getLeaf(n[0])

#checks if passed assessment has a session	
def checkAssessmentSession(assess):
    if assess.hasSession ==0:
        return None
    elif assess.hasSession ==1:
        return assess
    else:
        children = Assessment.objects.filter(parent=assess_id)	
        for child in children:
            return checkAssessmentSession(child)
    
# Name: getStudentsForASession
# Description:
# Parameter: sess_id_:session Object
# Return:  list of uids e.g ["u1200000", "u12233423"]   
def getStudentsForASession(sess_id_):
	temp = AllocatePerson.objects.filter(session_id=sess_id_,isStudent = 1)
	list = []
	for x in temp:
	        person = Person.objects.get(id=x.getPersonID().id)
	        uid = person.getupId()
	        list.append(uid)
	return list

def validateIfMarkerCanViewSession(marker_id, sess_id):
    marker = Person.objects.get(upId=marker_id)
    session = Session.objects.get(id=sess_id)
    
    personAllocated = AllocatePerson.objects.get(person_id=marker, isMarker = 1)
    if personAllocated:
        return True
    return False

def retrieveAllLeafAssessmentOfAggregate(assess_id,array):
    leaf = Assessment.objects.filter(parent=assess_id)
    for n in leaf:
        if n.assessment_type == "Leaf":
            array.append(n)
        else:
            retrieveAllLeafAssessmentOfAggregate(n.id,array)
    return array

def makeOnlySessionInLineage(assess_id):
    assess = Assessment.objects.get(id=assess_id)
    children = Assessment.objects.filter(parent=assess_id)
    parent = Assessment.objects.get(id=assess.parent)
    
    for child in children:
        child.hasSession = 2
        if child.assessment_type == 'Aggregate':
            makeOnlySessionInLineageChildren(child.id)
    
    makeOnlySessionInLineageAncestors(parent)
    return True   
        
def makeOnlySessionInLineageChildren(assess_id):
    children = Assessment.objects.filter(parent = assess_id)
    
    for n in child:
        n.hasSession = 2
        if child.assessment_type == 'Aggregate':
            makeOnlySessionInLineageChildren(n.id)
    return True

def makeOnlySessionInLineageAncestors(parent):
    parent.hasSession = 2
    if parent.parent == None:
        return True
    else:
        parents = Assessment.objects.get(id=parent.parent)
        makeOnlySessionInLineageAncestors(parents)

    
########################## END MARKER VIEW FUNCTIONS ###############################
'''

##################### STUDENT VIEW FUNCTIONS #######################################

'''
# Name: getAllPublishedAssessmentsForStudent(mod_code)
# Description: Returns all the published assessments for the module
# Parameter: mod_code : String
# Returns: Assessments[]
def getAllPublishedAssessmentsForStudent(mod_code):
    mod_obj = Module.objects.get(id=str(mod_code))
    assessments = Assessment.objects.filter(mod_id=mod_obj, published = True)
    return assessments

# Name: getMarkForStudent(student_id, assess_id)
# Description: Retrieves the student's mark for the assessment specified. (Whether aggregate or leaf)
# Parameter: student_id : String
# Parameter: assess_id : String
# Returns: Float
def getMarkForStudent(student_id, assess_id):
    stud = student_id[0]
    print '=================================================\n'
    print "Assessment aaaaaaa: " + str(student_id) + '\n'
    print '================================================='
    stu_obj = Person.objects.get(upId=student_id)
    
    assess_obj = Assessment.objects.get(id=assess_id)
   
    if assess_obj.assessment_type == 'Leaf':
        markAlloc = MarkAllocation.objects.get(assessment=assess_obj, student=stu_obj)
        mark = markAlloc.getMark()
        full = assess_obj.full_marks
        percentage = (mark/full) * 100
        list =[]
        list.append(mark)
        list.append(full)
        list.append(percentage)
    else:

        agg = SimpleSumAggregator()
        print '*********************'
        print "Bout to aggregate"
        print '********************'
        list = agg.aggregateMarksStudent(assess_id, student_id)
        print '*********************'
        print "THE LIST---" + str(list)
        print '********************'

    mark = list[0]
    perc = list[2]

    list[0] = "{0:.2f}".format(mark)
    list[2] = "{0:.2f}".format(perc)

    return list

# Name: getMarksOfChildrenAssessments(assess_id)
# Description: Returns name, marks obtained and full marks for all children of assess
# Parameter: parent_id : String
# Return: String[] (because the marks should not be editable)
def getMarksOfChildrenAssessments(parent_id, student_id):
    children = Assessment.objects.filter(parent = parent_id)
    #Array that will contain lists with name, aggregated_mark, full_mark for each child of parent
    marksOfChildren = []
    for child in children:
        name = child.assess_name
        student_obj = Person.objects.get(upId=student_id)
        list = []

        list.append(child.id)
        list.append(name)
        list.append(child.published)
        marks = getMarkForStudent(student_id,child.id)
        print "am hereeeeee"
        list.append(marks[0])
        list.append(marks[1])
        list.append(marks[2])
        print '============================================='
        print "My LIST MAAAAAN: "+str(list)
        print '============================================='
        marksOfChildren.append(list)
        #Array of arrays containing {Assess_id, Assess_name,published, mark_obtained, full_mark, percentage}
        print '============================================='
        print "MY CHILDREN MARKS: "+str(marksOfChildren)
        print '============================================='
    return marksOfChildren 

def getPublishedChildrenAssessmentsForAssessmentForStudent(assess_id, student_id):
    assessments = Assessment.objects.all()
    children = []
    
    for ass in assessments:
        if str(ass.parent) == str(assess_id):
            if ass.published == True:
                children.append(ass)
    
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%"
    print "MY CHILDREN" + str(children)
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%"
    #published is not taken into account
    childrenMarks = getMarksOfChildrenAssessments(assess_id, student_id)
    publishedChildrenMarks = []
    #getAllthe marks that are published
    for markedChild in childrenMarks:
        if markedChild[2] == True: #published value is true
            publishedChildrenMarks.append(markedChild)
        
           #Array of arrays containing {Assess_id, Assess_name,published, mark_obtained, full_mark}
    return publishedChildrenMarks

'''

#################### END STUDENT VIEW FUNCTIONS ###################################

'''