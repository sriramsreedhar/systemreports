#!/usr/bin/python3.6
import os
import shutil
import datetime
import sysconfig
import platform
import getpass
import socket
#import psutil
#import commands
osn=list(os.uname())

def get_ipaddress():
    try:
        ipaddress=socket.gethostbyname(socket.getfqdn())
        return ipaddress
    except:
        print("Unable to get hostname")

def check_internet_connection():
    try:
        return (socket.gethostbyname('google.com'))
    except:
        print("Unable to connect to Internet!!")

def network_devices():
    try:
       return os.listdir('/sys/class/net/')
    except:
        print("Not able to list devices, Please check if this is CENTOS or Ubuntu")

def date_time():
    dt = datetime.datetime.now()
    return (dt.strftime("%c"))

def sys_name():
    return osn[0]

def load_avg():
    return os.getloadavg()

def arch_name():
    return osn[4]


def home_env():
    return os.environ["HOME"]

def current_uid():
    return os.getuid() 

def clear_screen():
    return os.system("clear")

def user_name():
    return getpass.getuser()

def host_name():
    return os.uname()[1]

def cpu_logical_core():
    return os.cpu_count()


def current_platform():
    return sysconfig.get_platform()

def total_disk_size():
    BytesPerGB = 1024 * 1024 * 1024
    (total, used, free) = shutil.disk_usage("/")
    return (" %.2fGB " % (float(total)/BytesPerGB))
    #return ("Total Disk Size         :-  %.2fGB " % (float(total)/BytesPerGB))
    #return ("Used                    :-  %.2fGB" % (float(used)/BytesPerGB))
    #return ("Free                    :-  %.2fGB" % (float(free)/BytesPerGB))


def disk_usage():
    BytesPerGB = 1024 * 1024 * 1024
    (total, used, free) = shutil.disk_usage("/")
    #return ("Disk Used               :-  %.2fGB" % (float(used)/BytesPerGB))
    return (" %.2fGB" % (float(used)/BytesPerGB))



def disk_free():
    BytesPerGB = 1024 * 1024 * 1024
    (total, used, free) = shutil.disk_usage("/")
    #return ("Free                    :-  %.2fGB" % (float(free)/BytesPerGB))
    return (" %.2fGB" % (float(free)/BytesPerGB))


def processor_name():
    return platform.processor()

#def users_logged_in():
    a=psutil.users()
    return  [i[0] for i in a]


#def cpu_usage_system():
#    return psutil.cpu_percent()

def memory_usage_resource():
    import resource
    import sys
    rusage_denom = 1024.
    if sys.platform == 'darwin':
        # ... it seems that in OSX the output is different units ...
        rusage_denom = rusage_denom * rusage_denom
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / rusage_denom
    return mem


def physical_memory():
    try:
        import os 
        mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
        mem_gib = mem_bytes/(1024.**3)
        return mem_gib
    except:
        print("Unable to get Physical Memory... Runs on Ubuntu and Centos though")


clear_screen()
print ("This System Report is Generated on :-", date_time())
print ("=========================================================")
print ("Name of Operating System is      :- ", sys_name())
print ("Host Name                        :- ", host_name())
print ("Load Average                     :- ", load_avg())
print ("System Architecture              :- ", arch_name())
print ("Home environment is set to       :- ", home_env())
print ("Current UID                      :- ", current_uid())
print ("Current User Name                :- ", user_name())
print ("Actual root Disk Size            :-", total_disk_size())
print ("root (/) Disk Used               :-", disk_usage())
print ("root (/) Free Space Available    :-", disk_free())
print ("Number of Logical Cores          :- ",  cpu_logical_core())
print ("Current System Platform          :- ",  current_platform())
print ("Processor in use                 :- ",  processor_name())
#print ("Current Logged in Users          :- ",  users_logged_in())
#print ("Current CPU System Used          :- ",  cpu_usage_system())
#print ("Memory Usage in MB               :- ",  memory_usage_resource())
print ("Total Physical Memory(GB)        :- ",  physical_memory())
print ("IP Address(Primary)              :- ",  get_ipaddress())
print ("Network Devices                  :- ",  network_devices())
print ("DNS Works (www.google.com) IP is :- ",check_internet_connection())
