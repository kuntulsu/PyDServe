from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404, HttpResponse
import psutil
from django.http import JsonResponse
import cpuinfo
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout as dlogout,authenticate
import distro
from importlib.util import find_spec as find_modules
from .helper import Kcores
from .helper.Kdecorator import module_required, ajax_required
import subprocess

# Create your views here.


def login_redirector(request):
	return HttpResponseRedirect("../../login?from=dashboardredirector")
@login_required
def index(request):

	meminfo = psutil.virtual_memory()
	# getting / device
	diskpart = psutil.disk_partitions("/")
	rootDusage = psutil.disk_usage("/")
	for x in diskpart:
		if x.mountpoint == "/":
			mp = x.device
		else:
			pass
	context = {
		'uptime' : {
			"uptime_since" : subprocess.Popen("uptime -s".split(),stdout=subprocess.PIPE).communicate()[0].decode(),
			"uptime" : subprocess.Popen("uptime -p".split(),stdout=subprocess.PIPE).communicate()[0].decode(),
		},
		'distro' : distro.id(),
		'cpu_count' : psutil.cpu_count(),
		'cpuname' : cpuinfo.get_cpu_info()['brand'],
		'diskinfo' : {
			'mp' : mp,
			'disk_total' : round(rootDusage.total / 1024000000,1),
			'disk_free' : round(rootDusage.free / 1024000000,1)
		},
		'meminfo' : {
			'total_mem' : round(meminfo.total / 1024000000,2),
			'free_mem' : round(meminfo.available / 1024000000,2)
		},
	}
	return render(request,'dashboard/index.html',context)
@login_required
@ajax_required
def dashboard_raw(request):
	meminfo = psutil.virtual_memory()
	# getting / device
	diskpart = psutil.disk_partitions("/")
	rootDusage = psutil.disk_usage("/")
	for x in diskpart:
		if x.mountpoint == "/":
			mp = x.device
		else:
			pass
	context = {
		'distro' : distro.id(),
		'cpu_count' : psutil.cpu_count(),
		'cpuname' : cpuinfo.get_cpu_info()['brand'],
		'diskinfo' : {
			'mp' : mp,
			'disk_total' : round(rootDusage.total / 1024000000,1),
			'disk_free' : round(rootDusage.free / 1024000000,1)
		},
		'meminfo' : {
			'total_mem' : round(meminfo.total / 1024000000,2),
			'free_mem' : round(meminfo.available / 1024000000,2)
		},
	}
	return render(request,'dashboard/dashboard_raw.html',context)


@login_required
def logout(request):
	dlogout(request)
	return HttpResponseRedirect("../login?from=dlogout")

@login_required
@ajax_required
def modules(request):
	cM = open('callableModules.txt',"r")
	cU = open('callableUtilities.txt',"r")
	readcM = cM.readlines()
	readcU = cU.readlines()
	cU.close()
	cM.close()
	module_result = {}
	util_result = {}
	for x in readcM:
		x = x.replace("\n","")
		find = find_modules(x)
		try:
			path = find.submodule_search_locations[0]
		except TypeError:
			path = find.origin
		except AttributeError:
			path = None
		module_result[x] = {
			"installed" : find is not None,
			"path" : path
		}
	for x in readcU:
		x = x.replace("\n","")
		r = subprocess.Popen(f"which {x}".split(),stdout=subprocess.PIPE).communicate()[0].decode()
		if len(r) > 0:
			util_result[x] = {
				"executable" : r
			}
		else:
			util_result[x] = {
				"executable" : None
			}
	context = {
		"modules" : module_result,
		"utilities" : util_result,
	}
	return render(request,'dashboard/modules.html',context)
@ajax_required
def ping(request):
	if request.user.is_authenticated:
		return HttpResponse("ok",content_type="text/plain")
	elif not request.user.is_authenticated:
		return HttpResponse("login",content_type="text/plain")


@csrf_exempt
@ajax_required
def dashboard_login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		# setting the session expiration time in seconds
		request.session.set_expiry(300) # 5 minutes
		return HttpResponse("loginOk")
	else:
		return HttpResponse("loginFailure")


@login_required
@ajax_required
@module_required('subprocess')
def syslog(request):
	logs = subprocess.Popen("tail -n 500 /var/log/syslog".split(),stdout=subprocess.PIPE).communicate()[0].decode()
	context = {
	'logs' : logs,
	}
	return render(request,'dashboard/syslog.html',context)

@ajax_required

def sysload(request):

	resource = {
		"cpu" : psutil.cpu_percent(),
		"memory" : psutil.virtual_memory(),
		"disk" : psutil.disk_usage("/"),
		"swap" : psutil.swap_memory(),
	}
	try:
		if request.GET['show'] == 'cpu':
			data_json = {
			'cpu_load' : int(resource['cpu']),
			'cpu_load_all' : psutil.cpu_percent(percpu=True),
			}
		elif request.GET['show'] == 'memory':
			data_json = {
				'swap_load' : int(resource['swap'].percent),
				'memory_load' : int(resource['memory'].percent)}
		elif request.GET['show'] == 'disk':
			data_json = {'disk_load' : int(resource['disk'].used / resource['disk'].total * 100)}

	except KeyError:
		data_json = {
	


	'cpu_load' : int(resource['cpu']),
	'memory_load' : int(resource['memory'].percent),
	'disk_load' : int(resource['disk'].used / resource['disk'].total * 100)
	}
	return JsonResponse(data_json)
@login_required
@ajax_required
@module_required('distro')
def sysinfo(request):
	headers = ['CONTENT_LENGTH','CONTENT_TYPE','HTTP_ACCEPT','HTTP_ACCEPT_ENCODING','HTTP_ACCEPT_LANGUAGE','HTTP_HOST','HTTP_REFERER','HTTP_USER_AGENT','QUERY_STRING','REMOTE_ADDR','REMOTE_HOST','REMOTE_USER','REQUEST_METHOD','SERVER_NAME','SERVER_PORT']
	http_headers = {}
	for x in headers:
		try:
			http_headers[x] = request.META[x]
		except KeyError:
			http_headers[x] = ""
	context = {
		'dist' : distro.os_release_info(),
		'headers' : http_headers,
	}
	return render(request,'dashboard/sysinfo.html',context)


@login_required
@ajax_required
def userman(request):
	context = {}
	return render(request,'dashboard/userman.html',context)

@login_required
@ajax_required
def user_permission(request):
	context = {}
	return render(request,'dashboard/userman.user_permission.html',context)

@login_required
@ajax_required
def servroom(request):
	context={

	}
	return render(request,'dashboard/servroom.html',context)


#need improvements (critical level)

@login_required
@module_required(['cpuinfo','psutil','distro'])
@ajax_required
def cpu_info(request):
	f = open("/proc/cpuinfo","r")
	file_content = []
	for x in f.readlines():
		file_content.append(x)
	f.close()
	context = {
		"cpuinfo" : cpuinfo.get_cpu_info(),
		"psutil" : psutil,
		"distro" : distro,
		"cpu_raw": file_content,
		"cpuhelper":Kcores.cpuhelper(),
		"cpuiter" : Kcores.cpuiter(),
		"cpuiter_raw" : Kcores.cpuiter_raw(),
	}
	return render(request,'dashboard/servroom.cpuinfo.html',context)


@login_required
@ajax_required
def meminfo(request):
	context = {
		"swap" : Kcores.swapinfo(),
	}
	return render(request,'dashboard/servroom.meminfo.html',context)

@login_required
@ajax_required
@module_required(['subprocess','psutil'])
def diskinfo(request):
	context = {
		"disklist" : Kcores.disklist(),
		"raw_disk" : subprocess.Popen("lsblk --fs".split(),stdout=subprocess.PIPE).communicate()[0].decode()
	}
	return render(request,'dashboard/servroom.diskinfo.html',context)


@login_required
@ajax_required
def web_terminal(request):
	context = {

	}
	return render(request,'dashboard/sysadmin.web_terminal.html',context)


@login_required()
@module_required("psutil")
@ajax_required
def sysnet(request):
	devhelper = psutil.net_if_addrs()
	try:
		if request.GET['device']:
			try:
				devhelper = devhelper[request.GET['device']]
				device_dict = {
					"IPv4" : "None",
					"Subnet Mask" : "None",
					"Broadcast" : "None",
					"IPv6" : "None",
					"MAC Address" : "None",

				}
				for x in devhelper:
					if str(x.family) == "AddressFamily.AF_INET":
						device_dict['IPv4'] = x.address
						device_dict['Subnet Mask'] = x.netmask
						device_dict['Broadcast'] = x.broadcast
					elif str(x.family) == 'AddressFamily.AF_INET6':
						device_dict['IPv6'] = x.address.replace(f"%{request.GET['device']}","")
					elif str(x.family) == "AddressFamily.AF_PACKET":
						device_dict['MAC Address'] = x.address
				context = {
					'device' : device_dict,
					'status' : psutil.net_if_stats()[request.GET['device']],
				}
				return render(request,'dashboard/sysadmin.networks.manager.html',context)
			except KeyError:
				return render(request,'dashboard/sysadmin.networks.manager.html')
	except:
		device_dict = {}
		for x,y in devhelper.items():
			device_dict[x] = {
				"ipv4" : "None",
				"netmask" : "None",
				"broadcast" : "None",
				"ipv6" : "None",
				"mac" : "None",
			}
			for z in y:
				if str(z.family) == "AddressFamily.AF_INET":
					device_dict[x]['ipv4'] = z.address
					device_dict[x]['netmask'] = z.netmask
					device_dict[x]['broadcast'] = z.broadcast
				elif str(z.family) == 'AddressFamily.AF_INET6':
					device_dict[x]['ipv6'] = z.address.replace(f"%{x}","")
				elif str(z.family) == "AddressFamily.AF_PACKET":
					device_dict[x]['mac'] = z.address

		context = {
			'addr' : device_dict,
		}
		return render(request,'dashboard/sysadmin.networks.html',context)
@login_required
@ajax_required
def filefinder(request):
	context = {

	}
	return render(request,'dashboard/sysadmin.filefinder.html',context)

@csrf_exempt
@ajax_required
@login_required
def filefinder_post(request):
	query = request.POST['QueryInput']
	is_sensitive = request.POST['QueryCaseSens']
	if is_sensitive == 'false':
		find =  subprocess.Popen(f"locate -i -b -n 100 {query}".split(),stdout=subprocess.PIPE).communicate()[0].decode()
	else:
		find =  subprocess.Popen(f"locate -b -n 100 {query}".split(),stdout=subprocess.PIPE).communicate()[0].decode()

	result = {
		"result" : find,
		"result_count" : find.count("\n")
	}
	return JsonResponse(result)
