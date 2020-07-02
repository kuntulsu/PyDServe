import psutil
import subprocess
import random
import os
import time
import mimetypes
from psutil._common import bytes2human
# stable release at 1.0
VERSION = "0.1.6~alpha"



def swapinfo():
	fstab = open("/etc/fstab","r")
	swapline = []
	for x in fstab.readlines():
		if "swap" in x:
			swapline.append(x)

	procswaps = subprocess.Popen("cat /proc/swaps".split(),stdout=subprocess.PIPE).communicate()
	devices = []
	index = 5
	while True:
		try:
			devices.append(procswaps[0].split()[index].decode())
			index = index+5
		except IndexError:
			break
	
	confirmed = []
	count = 0
	for x in devices:
		for y in swapline:
			s = subprocess.Popen(f"swaplabel {x}".split(),stdout=subprocess.PIPE).communicate()[0].split()[1].decode()
			if s in y:
				confirmed.append(f"Swap ID : {count}<ul><li>Device : {x}</li><li>UUID : {s}</li></ul>")
				count = count+1
	return confirmed
def log_generator(unit):
	print(unit)
	if unit == 'kern':
		logs = subprocess.Popen(f"dmesg --time-format ctime --color=never".split(),stdout=subprocess.PIPE).communicate()[0].decode()
		logs = logs.split("\n")
	elif unit == 'syslog':
		log = open("/var/log/syslog")
		logs = log.readlines()
		log.close()
	elif unit == 'auth':
		log = open("/var/log/auth.log")
		logs = log.readlines()
		log.close()
	log_list = []
	
	try:
		for x in logs:
			each = x.split()

			if unit == 'syslog' or unit == 'auth':
				time = each[0:3]
				del each[0:3]
			elif unit == 'kern':
				time = each[0:5]
				del each[0:5]
			component = []
			is_component = False
			message = ""
			for i in each:
				
				if i.endswith(":"):
					component.append(i.replace(":",""))
					index = each.index(i)
					is_component = True
					break
				else:
					component.append(i)
			if is_component:
				component = " ".join(str(f) for f in component)
				if len(component) > 1:
					del each[0:index+1]
				else:
					del each[index]
				message = " ".join(str(f)for f in each)
			else:
				message = " ".join(str(f) for f in component)
				component = ""
			#now collecting the list to string
			time = " ".join(str(f) for f in time)
			time = str(time).replace("[","").replace("]","")
			log_list.append((time,component,message))
	except TypeError:
		pass
	return log_list
def dirlisting(path="/"):
	if not path.endswith("/"):
		path = path + "/"
	disk_usage = psutil.disk_usage(path)
	if disk_usage.percent >= 0 and disk_usage.percent <= 50:
		bs_status = "success"
	elif disk_usage.percent > 50 and disk_usage.percent < 80:
		bs_status = "warning"
	elif disk_usage.percent >= 80 :
		bs_status = "danger"
	print(bs_status)
	items = {
		"current_dir" : path,
		"disk_usage" : {
			"total" : bytes2human(disk_usage.total),
			"used" : bytes2human(disk_usage.used),
			"free" : bytes2human(disk_usage.free),
			"percent" : disk_usage.percent,
			"status" : bs_status
		},
		"direct" : {
			"folder" : [],
			"file" : [],
		},
	}
	try:
		for x in os.scandir(path):
			if x.name.startswith("."):
				attr = "hidden"
			else:
				attr = "show"
			if x.is_dir():
				types = "Directory"
			else:
				types = mimetypes.guess_type(x.path)[0]
				if types is None:
					types = "Unknown"
			itemname = x.name.replace("+","@plus")
			if x.is_dir():
				items['direct']['folder'].append({
					"name" : x.name,
					"size" : len(os.listdir(path+x.name)),
					"path" : path.replace("+","@plus") + itemname,
					"type" : types,
					"last_accessed" : time.ctime(x.stat().st_ctime),
					"attr" : attr,
				})
			else:
				items['direct']['file'].append({
					"name" : x.name,
					"size" : bytes2human(x.stat().st_size),
					"path" : path.replace("+","@plus") + itemname,
					"type" : types,
					"last_accessed" : time.ctime(x.stat().st_ctime),
					"attr" : attr,
				})
	except (NotADirectoryError,FileNotFoundError) as err:
		items['direct'] = {
			"error" : True,
			"message" : err,
		}
	return items