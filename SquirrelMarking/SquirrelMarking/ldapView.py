from django.shortcuts import render
import ldap
import re
from django.http import HttpResponse

global ldapURI
ldapURI = "ldap://localhost"
global basedn
basedn = "ou=Computer Science,o=University of Pretoria,c=ZA"
# Create your views here.
def initialize_ldap():
    try:
        ldapConnection
    except NameError:
        try:
            global ldapConnection
            ldapConnection = ldap.initialize(ldapURI)
            ldapConnection.simple_bind_s()
            return ldapConnection
        except Exception, e:
            raise e
    else:
        return ldapConnection

def authenticateUser(request, username, password):
    try:
        ldapConnectionLocal = initialize_ldap()
        results = ldapConnectionLocal.search_s(basedn,ldap.SCOPE_SUBTREE,"uid="+username)
        for dn,entry in results:
            dn = dn
        try:
            dn
        except NameError:
            raise Exception(ldap.INVALID_CREDENTIALS)
        else:
            newUsername = dn
            ldapConnectionTemp = ldap.initialize(ldapURI)
            ldapConnectionTemp.simple_bind_s(newUsername,password)
            request.session['user'] = constructPersonDetails(username)
            return request.session['user']

    except ldap.INVALID_CREDENTIALS, e:
        raise e

def getGroups(username, filterv):
    ldapConnectionLocal = initialize_ldap()
    results = ldapConnectionLocal.search_s(basedn,ldap.SCOPE_SUBTREE,"(&(memberuid="+username+")(cn=" + filterv + "*))",["cn"])
    resultArray = []
    for dn,cn in results:
        tmp = str(cn['cn'])[2:-2]
        try:
            pos = tmp.index('_')
        except:
            resultArray.append(tmp)
        else:
            resultArray.append(tmp[pos+1:])
    return resultArray

def sourceEnrollments(username):
    return getGroups(username,"stud_")

def sourceTutorDesignations(username):
    return getGroups(username,"tuts_")

def sourceTeachingAssistantDesignations(username):
    return getGroups(username,"teachasst_")

def sourceLecturerDesignations(username):
    return getGroups(username,"lect_")

def sourceDemographics(username):
    ldapConnectionLocal = initialize_ldap()
    results = ldapConnectionLocal.search_s(basedn,ldap.SCOPE_SUBTREE,"uid="+username,["uid","title","initials","cn","sn","mail"])
    for dn,attributes in results:
        return attributes

def constructPersonDetails(username):
    Person = {}
    attributes = sourceDemographics(username)
    for key,value in attributes.items():
        Person[key] = value
    Person["lecturerOf"] = sourceLecturerDesignations(username)
    Person["studentOf"] = sourceEnrollments(username)
    Person["teachingAssistantOf"] = sourceTeachingAssistantDesignations(username)
    Person["tutorFor"] = sourceTutorDesignations(username)
    return Person

def getMembers(groupName):
    ldapConnectionLocal = initialize_ldap()
    results = ldapConnectionLocal.search_s(basedn,ldap.SCOPE_SUBTREE,"cn=" + groupName,["memberUid"])
    resultArray = []
    for dn,memberUid in results:
        resultArray += memberUid['memberUid']
    return resultArray

def findPerson(filterName, filterValue):
    try:
        filterValue.index('*')
    except:
        ldapConnectionLocal = initialize_ldap()
        results = ldapConnectionLocal.search_s(basedn,ldap.SCOPE_SUBTREE,filterName + "=" + filterValue,["uid"])
        resultArray = {}
        for dn,uid in results:
            resultArray[str(uid['uid'])[2:-2]] = constructPersonDetails(str(uid['uid'])[2:-2])
        return resultArray
    else:
        raise Exception("Search filter may only contain alphanumeric characters.")
