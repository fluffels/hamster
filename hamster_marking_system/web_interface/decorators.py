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

def isAuthenticated():
    def wrapper(request,*args,**kwargs):
        print "is authemticated"

def isMarker(function):
    def wrapper(request,*args,**kwargs):
        
