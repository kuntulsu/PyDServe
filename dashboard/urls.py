from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='dashboard'),
	path('logout', views.logout, name='logout'),
	path('syslog',views.syslog, name='syslog'),
	path('sysload',views.sysload, name='sysload'),
	path('sysinfo',views.sysinfo, name='sysinfo')

]