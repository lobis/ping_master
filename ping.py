from subprocess import call
import re
import os

def hosts_get(filename):
    hosts = []
    with open(filename) as f:
        for line in f:
            hosts.append([x for x in line.split()])
    ip_addresses = []
    for host in hosts:
        aa = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", host[0])
        if aa:
            ip_addresses.append(aa.group())
    return ip_addresses

def ping_host(ip):
    FNULL = open(os.devnull, 'w')
    #careful when using venv
    response = call(["ping", "-c 1", "-W 1", ip], stdout=FNULL)
    #ping command returns 0 if host is up, returns error code >0 else
    return not response



#response = not call("ping -n 1 -w 500 " + ip + " >NUL 2>NUL", shell=True)

'''
i = 0
while 1:
	text = []
	text.append("-"*55)
	text.append("%-20s %-20s %-10s" % ("Hostname", "Address", "Alive"))
	text.append("-"*55)
	for host in hosts:
		#Because we used "shell = True" we need to check for possible code injections
		aa=re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", host[0])
		#Check if the first argument host[0] is an IP address
		if aa:
			ip = aa.group()
			response = not call("ping -n 1 -w 500 " + ip + " >NUL 2>NUL", shell = True)
			alive = "yes" if response else "no"
			hostname = "" if len(host) <= 1 else host[1]
			text.append("%-20s %-20s %-3s" % (hostname, ip, alive))

	text.append("-"*55)
	i = i + 1
	text.append("Iteration: %s" % i)
	call("cls", shell = True)
	for t in text: print t
time.sleep(1)
'''