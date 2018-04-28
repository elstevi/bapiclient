#!/usr/local/bin/python
import ConfigParser
import requests

config = Config = ConfigParser.ConfigParser()
config.read('/persist/bapiclient.conf')
HOSTS = config.get('global', 'hosts').replace(' ', '').split(',')

def new_host(host, vmdata):
    """ Create a new host """
    if host not in HOSTS:
        raise IOError('target host %s does not exist' % host)

    url = '%s/vm/' % host
    r = requests.post(url, json=vmdata)
    return r

def get_hosts():
    """ Return a list of hosts that bapiclient knows about """
    return HOSTS

def edit_host(host, newvm):
    """ Edit an existing host """
    if host not in HOSTS:
        raise IOError('target host %s does not exist' % host)
    url = "%s/vm/%s" % (host, newvm['name'])
    r = requests.patch(url, json=newvm)

def get_all_vms():
    """ Returns a list of VM's that we can see """
    vms = []
    for host in HOSTS:
        url = "%s/vm/" % host
        r = requests.get(url)
        vml = r.json()['vms']
        for vm in vml:
            vms.append(vm)
    return vms

def find_vm_host(vm_name):
    """ Find the host that a vm resides on """
    for host in HOSTS:
        url = "%s/vm/" % host
        r = requests.get(url)
        vml = r.json()['vms']
        if vm_name in vml:
            return host
    else:
        raise IOError("VM %s doesn't exist" % vm_name)

def get_vm_details(vm_name):
    """ Return a json dump of everything we know about a VM """
    host = find_vm_host(vm_name)
    url = "%s/vm/%s/dump" % (host, vm_name)
    r = requests.get(url)
    rtrn = r.json()
    rtrn['host'] = host
    return rtrn

def vm_action(vm_name, action):
    """ Run a particular action on a VM """
    host = find_vm_host(vm_name)
    url = "%s/vm/%s" %(host, vm_name)

    # GET - status
    if action == 'status':
        r = requests.get(url)

    elif action == 'delete':
        r = requests.delete(url)
        if r.status_code != 202:
            raise
        else:
            return

    # POST - start stop restart
    elif action == 'start' or action == 'stop' or action == 'restart':
        r = requests.post(url, json={'action': action})
    else:
        raise
    
    return r.json()

