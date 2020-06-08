from django.urls import path
from . import views
urlpatterns = [
	path('login_redirector', views.login_redirector, name='authredirector'),
	path('dashboard_login',views.dashboard_login,name="dashboard_login"),
	path('modules',views.modules,name='modules'),
	path('', views.index, name='dashboard'),
	path('dashboard_raw',views.dashboard_raw,name='dashboard_raw'),
	path('ping',views.ping,name='ping'),
	path('logout',views.logout, name='logout'),
	path('syslog',views.syslog, name='syslog'),
	path('sysload',views.sysload, name='sysload'),
	path('sysinfo',views.sysinfo, name='sysinfo'),
	path('user_manager',views.userman, name='userman'),
	path('user_manager/permission',views.user_permission,name='user_permission'),
	path('servroom',views.servroom,name='servroom'),
	path('servroom/cpu',views.cpu_info,name='cpuinfo'),
	path('servroom/memory',views.meminfo,name='meminfo'),
	path('servroom/disk',views.diskinfo,name='diskinfo'),
	path('sysadmin/web_terminal',views.web_terminal, name='web_terminal'),
	path('sysadmin/networks',views.sysnet,name='sysnet'),
	path('sysadmin/filefinder',views.filefinder,name='filefinder'),
	path('sysadmin/filefinder_post',views.filefinder_post,name='filefinder_post')
]