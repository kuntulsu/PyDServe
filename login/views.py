from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate as auth, login,logout

# Create your views here.
def index(request):

	if request.user.is_authenticated:
		return HttpResponseRedirect("../dashboard")
	else:
		return render(request,'login/login.html')
	
def authenticate(request):
	username = request.POST['username']
	password = request.POST['password']
	user = auth(request, username=username, password=password)
	if user is not None:
		login(request, user)
		# setting the session expiration time in seconds
		request.session.set_expiry(300) # 5 minutes
		return HttpResponseRedirect("../dashboard/")
	else:
		return HttpResponseRedirect("../login?from=authenticator")
def test(request):
	return HttpResponse(request.user.is_authenticated)