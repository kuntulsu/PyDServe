from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404, HttpResponse
import os, stat, subprocess, shlex, re, sys
import psutil
import shutil
from django.http import JsonResponse
import cpuinfo
import distro

# Create your views here.
def index(request):
	try:request.session['login_status']
	except:return HttpResponseRedirect("logout")
	try:
		meminfo = psutil.virtual_memory()
		# getting / device
		try:
			out = subprocess.Popen(shlex.split("df /"),stdout=subprocess.PIPE).communicate()

			m=re.search(r'(/[^\s]+)\s',str(out))

			mp= m.group(1)

		except:
			mp = "An Error Occured"	

		# end
		context = {
			'distro' : distro.linux_distribution()[0].split()[0].lower(),
			'cpuname' : cpuinfo.get_cpu_info()['brand'],
			'diskinfo' : {
				'mp' : mp,
				'disk_total' : round(shutil.disk_usage("/").total / 1000000000,1),
				'disk_free' : round(shutil.disk_usage("/").free / 1000000000,1)
			},
			'meminfo' : {
				'total_mem' : round(meminfo.total / 1000000000,2),
				'free_mem' : round(meminfo.available / 1000000000,2)
			},
			'uptime' : os.system('uptime'),
			'sysname' : os.uname().sysname +' '+ os.uname().nodename +' '+ os.uname().release +' '+ os.uname().version +' '+ os.uname().machine,
			'userdata' : request.session['userdata']
		}
		return render(request,'dashboard/index.html',context)
	except KeyError:
		return HttpResponseRedirect("logout")
def logout(request):
	try:
		del request.session['userdata']['username']
		del request.session['login_status']
	except:
		pass
	return HttpResponseRedirect("../login/")
def syslog(request):
	try:request.session['login_status']
	except:return HttpResponseRedirect("logout")
	try:
		f = open(os.path.dirname("/var/log/")+"/syslog")

		file_arrays = f.readlines()
		f.close()
		try:
			if request.GET['expand'] == 'True':
				log = open(os.path.dirname("/var/log/")+"/syslog")
				context = {
					'logs' : log.read(),
					'lenlogs' : len(file_arrays),
					'userdata' : request.session['userdata']
				}
				log.close()
				return render(request,'dashboard/syslog.html',context)
			else:
				return HttpResponseRedirect("syslog?expand=True")
		except:
			
			count_to_print = len(file_arrays) - 15
			counter = 0
			logs = []
			for x in file_arrays:
				if counter < count_to_print:
					counter +=1
				else:
					counter +=1
					logs.append(x)
			context = {
				'logs' : logs,
				'lenlogs' : len(file_arrays),
				'userdata' : request.session['userdata']
			}
			return render(request,'dashboard/syslog.html',context)
	except:
		context = {
				'logs' : "Unable to locate syslog",
				'userdata' : request.session['userdata']
			}
		return render(request,'dashboard/syslog.html',context)
def sysload(request):
	try:request.session['login_status']
	except:return HttpResponseRedirect("logout")
	data_json = {
	'cpu_load' : int(psutil.cpu_percent()),
	'memory_load' : int(psutil.virtual_memory().used / psutil.virtual_memory().total * 100),
	'disk_load' : int(shutil.disk_usage("/").used / shutil.disk_usage("/").total * 100)
	}
	return JsonResponse(data_json)
def sysinfo(request):
	try:request.session['login_status']
	except:return HttpResponseRedirect("logout")
	return HttpResponse(os.uname().sysname +' '+ os.uname().nodename +' '+ os.uname().release +' '+ os.uname().version +' '+ os.uname().machine)