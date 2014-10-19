from django.http import *
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
import json
    
def isLecture(function):
    def wrapper(request,*args,**kwargs):
        #mod = request.POST['module']
        #print "++++++++++++++++++++++========================"
        #print "++++++++++++++++++++++========================"
        #userModules = request.session['user']['lecturerOf']
        #done = False
        #for module in userModules:
        #    if module == mod:
        #        done = True
        #if done == True:
            return function(request,*args,**kwargs)
        #else:
        #    del request.session['user']
        #    return HttpResponseRedirect(reverse('home'))
    return wrapper
    

def isAuthenticated(function):
    def wrapper(request,*args,**kwargs):
        #print "is authenticated"
        #try:
        #    if request.session['user']:
                return function(request,*args,**kwargs)
        #    else:
        #        return HttpResponseRedirect(reverse('home'))
        #except:
        #    return HttpResponseRedirect(reverse('home'))
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
            del request.session['user']
            return HttpResponseRedirect(reverse('home'))
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
            del request.session['user']
            return HttpResponseRedirect(reverse('home'))
    return wrapper

def isPartOfmodule(function):
    def wrapper(request,*args,**kwargs):
        print "is he part of the module"
        if request.POST.get('studB'):
            mod = request.POST['studB']
            usermodules = request.session['user']['studentOf']
            done = False
            for module in usermodules:
                if mod == module:
                    done = True
            if done:
                return function(request,*args,**kwargs)
            else:
                del request.session['user']
                return HttpResponseRedirect(reverse('home'))
        elif request.POST.get('tutB'):
            mod = request.POST['tutB']
            usermodules = request.session['user']['tutorFor']
            done = False
            for module in usermodules:
                if mod == module:
                    done = True
            if done:
                return function(request,*args,**kwargs)
            else:
                del request.session['user']
                return HttpResponseRedirect(reverse('home'))
        elif request.POST.get('lectB'):
            mod = request.POST['lectB']
            usermodules = request.session['user']['lecturerOf']
            done = False
            for module in usermodules:
                if mod == module:
                    done = True
            if done:
                return function(request,*args,**kwargs)
            else:
                del request.session['user']
                return HttpResponseRedirect(reverse('home'))
        elif request.POST.get('taB'):
            mod = request.POST['taB']
            usermodules = request.session['user']['teachingAssistantOf']
            done = False
            for module in usermodules:
                if mod == module:
                    done = True
            if done:
                return function(request,*args,**kwargs)
            else:
                del request.session['user']
                return render_to_response("web_interface/login.htm",locals(),context_instance = RequestContext(request))
        else:
            del request.session['user']
            return HttpResponseRedirect(reverse('home'))
    return wrapper