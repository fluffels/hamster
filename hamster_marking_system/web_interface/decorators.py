from django.http import *
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
import json
    
def isLecture(function):
    def wrapper(request,*args,**kwargs):
        return function(request,*args,**kwargs)
        mod = request.POST['module']
        print "++++++++++++++++++++++========================"
        mod =  request.POST['module']
        print "++++++++++++++++++++++========================"
        userModules = request.session['user']['lecturerOf']
        done = False
        for module in userModules:
            if module == mod:
                done = True
        if done == True:
            return function(request,*args,**kwargs)
        else:
            raise Http404()
    return wrapper
    

def isAuthenticated(function):
    def wrapper(request,*args,**kwargs):
        print "is authenticated"
        try:
            if request.session['user']:
                return function(request,*args,**kwargs)
        except:
            return render_to_response("web_interface/login.htm",locals(),context_instance = RequestContext(request))
    return wrapper

def isMarker(function):
    def wrapper(request,*args,**kwargs):
        mod = request.POST['module']
        userModuleLT = request.session['user']['lecturerOf']
        userModuleTA = request.session['user']['teachingAssistantOf']
        userModuleTT = request.session['user']['tutorFor']
        done = False
        
        for module in userModuleLT:
            if module == mod:
                done = True
        
        for module in userModuleTA:
            if moduele == mod:
                done = True
        
        for module in userModuleTT:
            if module == mod:
                done = True

        if done == True:
            return function(request,*args,**kwargs)
        else:
            raise Http404()
    return wrapper

def isStudent(function):
    def wrapper(request,*args,**kwargs):
        print "Student is authenticated"
        mod = request.POST['module']
        userModuleST = request.session['user']['studentOf']
        done = False
    
        for module in userModuleST:
            if module == mod:
                done=True
        
        if done == True:
            return function(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("web_interface/login.htm",locals(),context_instance = RequestContext(request))
    return wrapper