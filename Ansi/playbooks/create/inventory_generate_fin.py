import proxmoxer
from proxmoxer.backends.https import AuthenticationError
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
#from API_INFO import host, user, password
import ipaddress
import time
import yaml

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

host = "10.222.201.201"
user = "ansible_collector@pam"
password = "qwerty12345"

proxmox = proxmoxer.ProxmoxAPI(host=host, user=user, password=password, verify_ssl=False)

def get_os_type(vmid):
    config = proxmox.nodes('pve').qemu(vmid).config
    config = config.get()
    os_type = config.get('ostype')
    if not os_type:
        return 'unknown'
    match os_type:
        case 'win10':
            return 'windows'
        case 'l26':
            return 'linux'
    return 'unknown'

def PrintIpsInfo(proxmox):
    inventory = {'windows': {'hosts': []}, 'linux': {'hosts': []}}

    for ips in proxmox.cluster.sdn.ipams('pve').status.get():
        if ips['vnet'] == 'cyberpol':
            vmid = ips.get('vmid') or ips.get('vmID')
            if vmid:
                os_type = get_os_type(vmid)
                host_info = f"{vmid} ansible_host={ips['ip']}"
                if os_type == 'windows':
                    inventory['windows']['hosts'].append(host_info)
                elif os_type == 'linux':
                    inventory['linux']['hosts'].append(host_info)
                print(vmid, ips['ip'], os_type)
            else:
                print("No vmid found for IP:", ips['ip'])
    
    with open('inventory.yml', 'w') as file:
        
        file.write("\n[linux:vars]\n")
        file.write("ansible_ssh_user=root\n")
        file.write("ansible_ssh_password=root\n")

        file.write("\n[windows:vars]\n")
        file.write("ansible_password=your_password\n")
        file.write("ansible_port=5985\n")
        file.write("ansible_connection=winrm\n")
        file.write("ansible_winrm_server_cert_validation=ignore\n")

        file.write("[windows]\n")
        for host in inventory['windows']['hosts']:
            file.write(f"{host}\n")
        
        file.write("\n[linux]\n")
        for host in inventory['linux']['hosts']:
            file.write(f"{host}\n")
        
        #Добавление логина/пароля для линуксоидных машин


PrintIpsInfo(proxmox)
