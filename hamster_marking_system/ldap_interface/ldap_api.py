import ldap, sys
import re
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django_auth_ldap.backend import LDAPBackend
from hamster.settings import *
import logging

logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# Create your views here.
def initialize_ldap():
    try:
        ldapConnection
    except NameError:
        try:
            global ldapConnection
            ldapConnection = ldap.initialize(AUTH_LDAP_SERVER_URI)
            ldapConnection.simple_bind_s()
            return ldapConnection
        except Exception, e:
            raise e
    else:
        return ldapConnection

def authenticateUser(request, username, password):
    try:
        ldapConnectionLocal = initialize_ldap()
        print 'LDAP initialized...'

        results = ldapConnectionLocal.search_s(AUTH_LDAP_BIND_DN,ldap.SCOPE_SUBTREE,"uid="+username)
        if results is None:
            print "results is None"
            #Do nothing authentication failed, something else takes care of this.
            print "Authentication failed!"
            pass
        else :
            print "Valid credentials"
            first_name = results[0][1]['cn'][0]
            last_name = results[0][1]['sn'][0]
            try:
                user = User.objects.get(username = username, first_name = first_name, last_name = last_name)
            except User.DoesNotExist:
                user = None
            if user is None:
                user = User.objects.create_user(username, '', password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
        print results
#        Testing if pre-population of user works...Feel free to delete this code
        #user = LDAPBackend().populate_user(username)
        #if user is None:
        #    raise Exception('No user named ' + username)
#        Done testing
        
        for dn,entry in results:
            dn = dn
        try:
            dn
            print dn
        except NameError:
            raise Exception(ldap.INVALID_CREDENTIALS)
            print "Incorrect information used in authenticating user."
        else:
            newUsername = dn
            ldapConnectionTemp = ldap.initialize(AUTH_LDAP_SERVER_URI)
            ldapConnectionTemp.simple_bind_s(newUsername,password)
            if 'user' in request.session:
                del request.session['user']
            request.session['user'] = constructPersonDetails(username)
            return request.session['user']

    except NameError:
        raise Exception(ldap.INVALID_CREDENTIALS)
        #print "Incorrect information used in authenticating user."

def getGroups(username, filterv):
    ldapConnectionLocal = initialize_ldap()
    results = ldapConnectionLocal.search_s(AUTH_LDAP_BIND_DN,ldap.SCOPE_SUBTREE,"(&(memberuid="+username+")(cn=" + filterv + "*))",["cn"])
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
    results = ldapConnectionLocal.search_s(AUTH_LDAP_BIND_DN,ldap.SCOPE_SUBTREE,"uid="+username,["uid","title","initials","cn","sn","mail"])
    for dn,attributes in results:
        return attributes

def constructPersonDetails(username):
    mPerson = {}
    attributes = sourceDemographics(username)
    for key,value in attributes.items():
        mPerson[key] = value
    mPerson["lecturerOf"] = sourceLecturerDesignations(username)
    mPerson["studentOf"] = sourceEnrollments(username)
    mPerson["teachingAssistantOf"] = sourceTeachingAssistantDesignations(username)
    mPerson["tutorFor"] = sourceTutorDesignations(username)
    mPerson["admin"] = getAdminPermission(username)
    return mPerson

def getAllModuleCodes():
    ldapConnectionLocal = initialize_ldap()
    results = ldapConnectionLocal.search_s(AUTH_LDAP_BIND_DN,ldap.SCOPE_SUBTREE,"cn=stud_*",["cn"])
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

def getAdminPermission(username):
    ldapConnectionLocal = initialize_ldap()
    results = ldapConnectionLocal.search_s(AUTH_LDAP_TECHTEAM_BIND_DN, ldap.SCOPE_SUBTREE, "(uid=*)")
    member_list = []
    for dn, entry in results:
        if username in entry['uid']:
            return ['admin']
    return ""

def getMembers(groupName):
    ldapConnectionLocal = initialize_ldap()
    results = ldapConnectionLocal.search_s(AUTH_LDAP_BIND_DN,ldap.SCOPE_SUBTREE,"cn=" + groupName,["memberUid"])
    resultArray = []
    for dn,memberUid in results:
        if "memberUid" in memberUid:
            resultArray += memberUid['memberUid']
    return resultArray

def getStudentsOf(module):
  try:
      return getMembers("stud_" + module)
  except:
      raise Exception("Module code does not exist")

def getTutorsOf(module):
  try:
      return getMembers("tuts_" + module)
  except:
      raise Exception("Module code does not exist")
    
def getTAsOf(module):
  try:
      return getMembers("teachasst_" + module)
  except:
      raise Exception("Module code does not exist")

def getLecturorsOf(module):
  try:
      return getMembers("lect_" + module)
  except:
      raise Exception("Module code does not exist")

def findPerson(filterName, filterValue):
    try:
        filterValue.index('*')
    except:
        ldapConnectionLocal = initialize_ldap()
        results = ldapConnectionLocal.search_s(AUTH_LDAP_BIND_DN,ldap.SCOPE_SUBTREE,filterName + "=" + filterValue,["uid"])
        resultArray = {}
        for dn,uid in results:
            resultArray[str(uid['uid'])[2:-2]] = constructPersonDetails(str(uid['uid'])[2:-2])
        return resultArray
    else:
        raise Exception("Search filter may only contain alphanumeric characters.")