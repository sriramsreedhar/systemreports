=============
SystemReports
=============


* GitHub: https://github.com/sriramsreedhar/systemreports.git
* Free and open source software: `Apache License 2.0` (see ``LICENSE``)


Features
--------

* **Web dashboard** (Windows, macOS, Linux): run ``systemreports`` and open the URL shown in your browser. Sections include CPU, memory, OS, disk (including I/O counters), network (interfaces, traffic totals, optional listening ports), top processes, and uptime.

* **CLI / JSON**: ``systemreports --cli`` for a text summary; ``systemreports --json`` for full JSON.

* Legacy Unix-only script is kept as ``legacy_cli.py`` (original CentOS-oriented behavior).

* Requires **Python 3.8+**, **psutil**, and **Flask**.

Install
---------
|# pip install -e .

|# Or: pip install systemreports

**Run the dashboard**

|# systemreports

|# Optional: bind on all interfaces (e.g. remote viewing on a trusted network)

|# systemreports --host 0.0.0.0 --port 5050

|# Skip opening a browser

|# systemreports --no-browser

----

Older pip example (Python 3.6 era):

|# pip3.6 install systemreports . 
Collecting systemreports
  Downloading https://files.pythonhosted.org/packages/f1/bd/f3a10752a279750a7136bdc849aba65676d44bfb63e4a269ea6e09a2efff/systemreports-1.0.0.tar.gz
Building wheels for collected packages: systemreports
  Running setup.py bdist_wheel for systemreports ... done
  Stored in directory: /root/.cache/pip/wheels/0b/61/5d/c99a4e88a009a7ee08f64c0b358c063eaefb58937450d95f7e
Successfully built systemreports
Installing collected packages: systemreports
Successfully installed systemreports-1.0.0

Output:
---------
|[root@1d939f630440 sys]# systemreports .  

|This System Report is Generated on :- Sat Jan 26 19:01:37 2019 .   
|========================================================= . 
|Name of Operating System is      :-  Linux . 
|Host Name                        :-  1d939f630440 . 
|Load Average                     :-  (0.09, 0.02, 0.01) .  
|System Architecture              :-  x86_64 . 
|Home environment is set to       :-  /root . 
|Current UID                      :-  0 . 
|Current User Name                :-  root . 
|Actual root Disk Size            :-  58.42GB .  
|root (/) Disk Used               :-  7.27GB . 
|root (/) Free Space Available    :-  48.15GB . 
|Number of Logical Cores          :-  2 . 
|Current System Platform          :-  linux-x86_64 . 
|Processor in use                 :-  x86_64 . 
|Total Physical Memory(GB)        :-  1.9522056579589844 . 
|[root@1d939f630440 sys]# 

|Dependencies .  
-------------
OS |
SHUTIL |
DATETIME |
SYSCONFIG |
PLATFORM |
COMMANDS|

