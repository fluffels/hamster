import json
from django.shortcuts import render, render_to_response, RequestContext
from web_services import views
from django.views.decorators.csrf import csrf_exempt

def home(request):
    
    return render_to_response("web_interface/base.htm",
                              locals(),
                              context_instance = RequestContext(request))
@csrf_exempt
def login(request):
	user = request.POST['username']
	passw = request.POST['password']
	data = {
		'username':user,
		'password':passw
	}
	user_info = views.login(request,json.dumps(data))
	user = json.loads(user_info.content)
	if user[0]['type'] == 1:
		 return render_to_response("web_interface/success.htm",locals(),context_instance = RequestContext(request))
	else:
		return render_to_response("web_interface/base.htm",locals(),context_instance = RequestContext(request))
