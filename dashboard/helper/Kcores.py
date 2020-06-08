import distro
import psutil
import cpuinfo
import subprocess
import random
def parsedistro():
	stuff = []
	stuff.append(f"<tr><td>Disro Name</td><td>{distro.name()}</td></tr>")
	distroinfo = distro.info()
	distroinfo['version_parts'] = ".".join(str(distroinfo['version_parts'][x]) for x in distroinfo['version_parts'])
	for x in distroinfo:
		if len(distroinfo[x]) < 1:
			distroinfo[x] = f"<i>Could not get '{x}' Information</i>"
		stuff.append(f"<tr><td>{x}</td><td>{distroinfo[x]}</td></tr>")
	return stuff

def disklist():
	#checking the disk that are mounted at system boot (/etc/fstab)
	f = open("/etc/fstab","r")
	fstab = []
	for x in f.readlines():
		if x.split()[0].startswith("UUID"):
			r = subprocess.Popen(f"blkid --uuid {x.split()[0][5:]}".split(),stdout=subprocess.PIPE).communicate()[0].decode().replace("\n","")
			fstab.append(r)

	stuff = []
	
	for x in psutil.disk_partitions():
		disk = psutil.disk_usage(x.mountpoint)
		disktotal = round(disk.total / 1024000000,1)
		diskfree = round(disk.free/ 1024000000,1)
		diskused = round(disk.used/ 1024000000,1)
		if "" in x.device:
			noreturn = "<i>None</i>"
		if x.device in fstab:
			boot = f"<span title='{x.device} is mounted automatically at system boot' class='fa fa-star'></span>"
		else:
			boot = ""
		if x.mountpoint == "/":
			star = f"<span title='{x.device} is mounted in root Filesystem' class='fa fa-linux'></span>"
		else:
			star = ""
		if x.opts[0:2] == 'ro':
			readonly = "(Read Only)"
		else:
			readonly = ""

		
		try:
			stuff.append(f"""
					<div class="pre card text-white" style="column-break-inside: avoid;border-radius:0;background-color:#343d46;border: 2px solid #273c75">
                <div class="card-body">
                	<h6 class="text-center">{x.device or noreturn} {star} {boot}<sup>{readonly}</sup></h6>
                	<ul>
                		<li>Size in Total : {disktotal}G ({int(disk.percent)}% used)</li>
	                	<li>Free		  : {diskfree}G</li>
	                	<li>Used 		  : {diskused}G</li>
	                	<li>Mounted In    : {x.mountpoint}</li>
	                	<li>Filesystem    : {x.fstype}</li>
	                	<li>Mount Options : {x.opts}</li>
                	</ul>
                </div>
            </div>
				""")

		except KeyError:
			pass
		del readonly
	return stuff
def genhexcolor():
	hexcolor = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
	color = ["#"]
	for x in range(6):
		color.append(random.choice(hexcolor))
	color = "".join(str(x)for x in color)
	return color

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
def cpuhelper():
	# create random hex color

	stuff = []
	cpu = 1
	for x in range(len(psutil.cpu_percent(percpu=True))):

		stuff.append(f"""
						data: datarray{x},
				        label: "CPU {cpu}",
				        borderColor: "{genhexcolor()}",
				        fill: true
				        
			""")
		cpu = cpu+1
	return stuff
def cpuiter():
	stuff = []
	for x in range(len(psutil.cpu_percent(percpu=True))):
		stuff.append(f"""
					datarray{x}.push(data.cpu_load_all[{x}])
			""")
	return stuff
def cpuiter_raw():
	stuff = []
	for x in range(len(psutil.cpu_percent(percpu=True))):
		stuff.append(f"""
				datarray{x}
			""")
	return stuff
def netstat():
	addrs = psutil.net_if_addrs()
	stuff = []
	for x in addrs:
		ipv4 = "<i>None</i>"
		ipv6 = "<i>None</i>"
		netmask = "<i>None</i>"
		broadcast = "<i>None</i>"
		mac = "<i>None</i>"
		managed = "enabled Manage"
		if x == 'lo':
			managed = "disabled Unmanagable"
		for i in addrs.get(x):
			family = str(i.family)

			if family == "AddressFamily.AF_INET":
				ipv4 = i.address
				netmask = i.netmask
				broadcast = i.broadcast
			elif family == "AddressFamily.AF_INET6":
					ipv6 = i.address.replace(f"%{x}","")
			elif family == "AddressFamily.AF_PACKET":
					mac = i.address

		stuff.append(f"""
					<td>{x}</td>
					<td>{mac}</td>
					<td>{ipv4}</td>
					<td>{ipv6}</td>
					<td>{netmask}</td>
					<td><a href="#" onclick="loader('sysadmin/networks?device={x}')" class="btn btn-primary btn-raised w-100 btn-sm {managed.split()[0]}">{managed.split()[1]}</a></td>
				""")
	return stuff
