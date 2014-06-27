from django.shortcuts import render, render_to_response, RequestContext
from django.http import HttpResponse
from .ldap_api import *

# Create your views here.
# The intergartion team only needs to replace this file with one of their own
# to be able to integrate with ldap.


def ldap_view_test(request):
  return HttpResponse("Authenticate User Object" + str(sourceLecturerDesignations("BWingfield")))



def index(request):
  try:
    response = HttpResponse("<table border='1' style='width:1000px'>"+ 
                        "<tr>"+
                          "<td>Authenticate User Object</td>" +
                          "<td>"+ str(authenticateUser(request,"u89000447","Herbert"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Enrollments of user</td>" +
                          "<td>"+str(sourceEnrollments("u89000447"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td> Tutor Designations</td>" +
                          "<td>"+str(sourceTutorDesignations("u89000447"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>TeachAsst Designations</td>" +
                          "<td>"+str(sourceTeachingAssistantDesignations("u89000915"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Lecturer Designations</td>" +
                          "<td>"+str(sourceLecturerDesignations("BWingfield"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Demographics of User </td>" +
                          "<td>"+str(sourceDemographics("BWingfield"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Members of Module </td>" +
                          "<td>"+str(getMembers("stud_COS301"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Find a user by attribute</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Tries to look up a student</td>" +
                          "<td>"+str(findPerson("uid","u89000447"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Prints all module codes </td>" +
                          "<td>"+str(getAllModuleCodes())+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td> Prints Students of a module </td>" +
                          "<td>"+str(getStudentsOf("COS300"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Prints Tutors of a module</td>" +
                          "<td>"+str(getTutorsOf("COS344"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Prints TAs of a module</td>" +
                          "<td>"+str(getTAsOf("COS110"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Prints Lecturers of a module</td>" +
                          "<td>"+str(getLecturorsOf("COS301"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Test * character</td>" +
                          "<td>"+ str(authenticateUser(request,"u89000447","Herbert"))+"</td>" +
                        "</tr> "+
                        "<tr>"+
                          "<td> " +"</td>" +
                        "</tr>"+
                        "<tr>"+
                          "<td> " +"</td>" +
                        "</tr>"+
                        "<tr>"+
                          "<td>Authenticate User Object</td>" +
                          "<td>"+ str(authenticateUser(request,"u89000447","Herbert"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Enrollments of user test char * </td>" +
                          "<td>"+str(sourceEnrollments("u8*"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td> Tuter Designations test char + </td>" +
                          "<td>"+str(sourceTutorDesignations("u8900044+"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>TeachAsst Designations test char $ </td>" +
                          "<td>"+str(sourceTeachingAssistantDesignations("u8900091$"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Lecturer Designations test char # </td>" +
                          "<td>"+str(sourceLecturerDesignations("##########"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Demographics of User test char \ n </td>" +
                          "<td>"+str(sourceDemographics("BWingfie\n"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Members of Module </td>" +
                          "<td>"+str(getMembers("stud_COS301"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Find a user by attribute</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Tries to look up a student test char @</td>" +
                          "<td>"+str(findPerson("uid","u8900044@"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td> Prints Students of a module </td>" +
                          "<td>"+str(getStudentsOf("*"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Prints Tutors of a module</td>" +
                          "<td>"+str(getTutorsOf("COS344"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Prints TAs of a module test char _ </td>" +
                          "<td>"+str(getTAsOf("COS11_"))+"</td>" +
                        "</tr> "+ 
                        "<tr>"+
                          "<td>Prints Lecturers of a module test char - </td>" +
                          "<td>" + str(getLecturorsOf("COS30-")) +"</td>" +
                        "</tr> " +  
                        "</table>");

    
  
    #print "****************************"
    #print "*  TeachAsst Designations  *"
    #print "****************************"
    #print sourceTeachingAssistantDesignations("u89000915")
    #print "****************************"
    #print "*   Lecturer Designations  *"
    #print "****************************"
    #print sourceLecturerDesignations("BWingfield")
    #print "****************************"
    #print "*   Demographics of User   *"
    #print "****************************"
    #print sourceDemographics("BWingfield")
    #print "****************************"
    #print "*     Members of Module    *"
    #print "****************************"
    #print getMembers("stud_COS301")
    #print "****************************"
    #print "* Find a user by attribute *"
    #print "****************************"
    #print "****************************"
    #print "*Tries to look up a student*"
    #print "****************************"
    #print findPerson("uid","u89000447")
    #print "****************************"
    #print "*  Prints all module codes *"
    #print "****************************"
    #print getAllModuleCodes()
    #print "*******************************"
    #print "* Prints Students of a module *"
    #print "*******************************"
    #print getStudentsOf("COS300")
    #print "*****************************"
    #print "* Prints Tutors of a module *"
    #print "*****************************"
    #print getTutorsOf("COS344")
    #print "***************************"
    #print "*  Prints TAs of a module *"
    #print "***************************"
    #print getTAsOf("COS110")
    #print "*********************************"
    #print "*  Prints Lecturers of a module *"
    #print "*********************************"
    #print getLecturorsOf("COS301")
    
    
    
    print "========================================================================="
    print "========================================================================="
    print "========================================================================="
    print "========================================================================="
    print "========================================================================="
    print "========================================================================="
    print "========================================================================="
    print "========================================================================="
    print " 			Reserved character tests			    "
    print "****************************"
    print "* Test * character"           #allready tested and exeption is thrown
    print "****************************"
    print authenticateUser(request,"u89000447","Herbert")
    print "****************************"
    print "* Invalid enrollments search test '*' char "
    print "****************************"
    print sourceEnrollments("u89*")
    print "****************************"
    print "*    Tuter Designations test '+' char "
    print "****************************"
    print sourceTutorDesignations("u8900044*")
    print "****************************"
    print "*  TeachAsst Designations   test '?' char*"
    print "****************************"
    print sourceTeachingAssistantDesignations("u8900091?")
    print "****************************"
    print "*   Lecturer Designations  *"
    print "****************************"
    print sourceLecturerDesignations("BWingfield")
    print "****************************"
    print "*   Demographics of User   *"
    print "****************************"
    print sourceDemographics("BWingfield")
    print "****************************"
    print "*     Members of Module    *"
    print "****************************"
    print getMembers("stud_COS301")
    print "****************************"
    print "* Find a user by attribute *"
    print "****************************"
    print "****************************"
    print "*Tries to look up a student*"
    print "****************************"
    print findPerson("uid","u89000447")
    print "****************************"
    print "*  Prints all module codes *"
    print "****************************"
    print getAllModuleCodes()
    print "*******************************"
    print "* Prints Students of a module *"
    print "*******************************"
    print getStudentsOf("COS300")
    print "*****************************"
    print "* Prints Tutors of a module *"
    print "*****************************"
    print getTutorsOf("COS344")
    print "***************************"
    print "*  Prints TAs of a module *"
    print "***************************"
    print getTAsOf("COS110")
    print "*********************************"
    print "*  Prints Lecturers of a module *"
    print "*********************************"
    print getLecturorsOf("COS301")
    """
    need to use request.replace("*"); to remove all occurences of *
    in the search stream before integrating
    
    """
    return response;
    
    
  except Exception as e:
    #raise e
    print e
  return HttpResponse("Go away")