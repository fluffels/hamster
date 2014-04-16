from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from dbModels.models import *
from ldapView import *
from businessLogicAPI import *

def test(request):
	populateModules()
	x2 = insertModule("COS301")
	x3 = insertAssessment('test','asdas',"type",x2)
	x4 = insertSessions("test",x3,'2012-12-12 12:12','2015-12-12 12:12')
	xx = insertMarkSession("u89000999",x4)
	x5 = insertMarkerModule("u89000999",x2)
	x6 = insertLeafAssessment("name",x3,100,True)
	x7 = insertMarkAllocation(x6,20,x4,"asdsad","sadasd",'2012-12-12 12:12')
	x8 = insertMarkerModule("u89000999",x2)
	login(request,"u89000989","Flanigan")
	p = getSessionPerson(request)
	#print (p.studentOf)
	#print (p.firstName)
	#removeMarkerFromModule("COS301","asdasd")
	#removeSession(x4.getID())
	#print getAllSessionsForModule("COS301")
	createAssessment(request, "test",123,"asd",x2)
	#closeSession(request,1)
	#removeSession(request,1)
	#removeMarkerFromSession(request,2,"u89000999")
	createMarkAllocation(request, 1,1,"someperson","someotherperson",'2012-12-12 12:12')
	updateMarkAllocation(request, 1,0)
	removeMarkerFromModule(request,"COS301","u89000999")
	setMarkerForModule(request,"u89000999",x2)
	#print getSessionByName("COS301","test")
	#print getMarkAllocationFromID(2)
	getAuditLogFromTimeRange('2012-12-12 12:12','2015-12-12 12:12')
	return HttpResponse("<html><body><p>"+str(len(getOpenSessions(2)))+"</p><p>"+str(getSessions()[0].assessment_id_id)+"</p></body></html>")


def loginData(request):
	t = get_template('login.html')
	html = t.render(Context())
	return HttpResponse(html)

def student_home(request):
	t = get_template('student.html')
	html = t.render(Context())
	return HttpResponse(html)
	
def lecturer_home(request):
	t = get_template('lecturer.html')
	html = t.render(Context())
	return HttpResponse(html)
	
def marker_home(request):
	t = get_template('marker.html')
	html = t.render(Context())
	return HttpResponse(html)


def assessment_view(request):
	t = get_template('assessmentView.html')
	html = t.render(Context())
	return HttpResponse(html)

def assessment_manager(request):
	t = get_template('assessmentManager.html')
	html = t.render(Context())
	return HttpResponse(html)

def session_manager(request):
	t = get_template('sessionManager.html')
	html = t.render(Context())
	return HttpResponse(html)
	
	
	
def audit_report(request):
	t = get_template('auditReport.html')
	html = t.render(Context())
	return HttpResponse(html)
	
def reporting_main(request):
	t = get_template('Reporting_Main.html')
	html = t.render(Context())
	return HttpResponse(html)


def statistics(request):
	t = get_template('Statistics.html')
	html = t.render(Context())
	return HttpResponse(html)

def student_chosen(request):
	t = get_template('studentChosen.html')
	html = t.render(Context())
	return HttpResponse(html)

def student_report(request):
	t = get_template('studentReport.html')
	html = t.render(Context())
	return HttpResponse(html)
	
	
def unpublish(request):
	t = get_template('unpublish.html')
	html = t.render(Context())
	return HttpResponse(html)

def marks_management(request):
        t = get_template('marks-management.html')
	html = t.render(Context())
	return HttpResponse(html)	
	
def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    print >>sys.stderr, 'Goodbye, cruel world!'
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticateUser(username, password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('home.html')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Squirrel account is not active.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

        # The request is not a HTTP POST, so display the login form.
        # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)
