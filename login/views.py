from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect,Http404, HttpResponse
from django.contrib.auth import authenticate, login
from .models import User
import hashlib
import django.utils
# Create your views here.
def index(request):
	try:
		context = {
			"login_status" : request.GET['login'],
			"post_username" : request.GET['username']
		}
		return render(request,'login/login.html',context)
	except:
		return render(request,'login/login.html')
	
def authenticate(request):
	post_username = request.POST['username']
	post_password = hashlib.md5(request.POST['password'].encode()).hexdigest()
	auth = User.objects.filter(username=post_username).filter(password=post_password).values()
	if len(auth) > 0 and len(auth) < 2:
		#we're ready, setup the session
		request.session['userdata'] = auth[0]
		request.session['login_status'] = True
		return HttpResponseRedirect("/dashboard")
	else:
		return HttpResponseRedirect("/login?login=failure&username="+post_username)
def test(request):
	get = []
	value = []
	try:
		for x in request.GET:
			get.append(x)
		for y in get:
			value.append(request.GET[y])
		value = ', '.join(str(y) for y in value)
		get = ', '.join(str(x) for x in get)
		return HttpResponse(value)
	except:
		raise Http404("Opps, Something bad Happen, Seems like 404 for me.")