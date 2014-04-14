from models import *
from ldapView import *

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

def getAllTutorsOfModule(mod_code):
    list = getTutorsOf(mod_code)
    return getPersonListFromArrayList(list)

def getAllMarkersOfModule(mod_code):
    temp = MarkerModule.objects.filter(module=mod_code)
    list =[]
    #for x in temp:
    #    temp2=Module.objects.filter(code=x)
    #    if temp2:
    #        list.append(temp2) Ldap
    return list

def getAllAssessmentsForModule(mod_code):
    temp= Assessment.objects.filter(module_id=mod_code)
    return temp

def getAllOpenAssessmentsForModule(mod_code):
    temp=Assessment.objects.filter(module_id=mod_code)
    list =[]
    for x in temp:
        temp2=Sessions.objects.filter(assessment_id=x,status=True)#implement
        if temp2:
            list.append(temp2)
    return list

def getAllModulesForStudent(uid):
    return sourceEnrollments(uid)

def getAllModulesForMarker(empl_no):
    temp = MarkerModule.objects.filter(marker_id=empl_no)
    list =[]
    for x in temp:
        temp2=Module.objects.filter(code=x)
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
    temp= MarkAllocation.objects.filter(student=empl_no)
    list = []
    for x in temp:
        temp2 = LeafAssessment.objects.filter(leaf_id=x)
        temp3 = Assessment.objects.filter(assessment_id=temp2.ge)
        if temp3.get() == mod_code:
            list.append(temp3)
    return list

def getAllAggregatedResultsForStudentOfModule(empl_no, mod_code, level):
  
  return

