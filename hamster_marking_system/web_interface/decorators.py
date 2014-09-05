from django.http import *
import json

def isLecture(function):
    def wrapper(request,*args,**kwargs):
        #mod = request.POST['module']
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
        print "is authemticated"
        if request.session['user']:
            return function(request,*args,**kwargs)
        else:
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
