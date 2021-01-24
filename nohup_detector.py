import psutil
import os
import re

NOHUP_DEFAULT_FD = "nohup.out"

def check_fd(file_descriptors):
	'''
	check_fd(file_descriptors) --> Boolean
	The function checks for constant file descriptor of the nohup command
	'''

	for _fd in file_descriptors:
		path = _fd[0]
		if NOHUP_DEFAULT_FD in path:
			return True
	return False


def check_hanghandle(pid):
	'''
	check_hanghandle(pid) --> Boolean
	The function checks if the SIGHUG flag is turn on the SIGIGN line in the status file under /proc.
	'''

	file_path = "/proc/{}/status".format(pid)
	try:
		with open(file_path, "r") as file_obj:
			data = file_obj.read()
	except Exception as e:
		print("Failed to open status file: {} {}".format(file_path, e))
		return False
	res = re.findall("SigIgn:\t([0-9A-F]{16})", data)
	if len(res) > 0:
		_bitmap = res[0]
		if _bitmap[-1] == "1":
			return True
		else:
			return False


def check_env(env_dict):
	'''
	check_env(env_dict) --> Boolean
	The function checks if the $_ enviroment variable holds the nohup command.
	'''
	if "_" in env_dict.keys():
		if "nohup" in env_dict["_"]:
			return True
		else:
			return False

def run():
	results = {}
	for proc in psutil.process_iter():
		proc_results = {}

		try:
			_pid = proc.pid
			_enviroment = proc.environ()
			_cmdline = proc.cmdline()
			_ppid = proc.ppid()
			_fd = proc.open_files()
		except Exception as e:
			print("Failed to access process, error: {}".format(e))
			continue

		res = check_fd(_fd)
		
		if res:
			results[_pid] = {"Name":proc.name(), "Cmdline":_cmdline, "PPID":_ppid}
			proc_results["fd"] = True

		res = check_env(_enviroment)

		if res:
			results[_pid] = {"Name":proc.name(), "Cmdline":_cmdline, "PPID":_ppid}
			proc_results["environ"] = True

		res = check_hanghandle(_pid)

		if res:
			results[_pid] = {"Name":proc.name(), "Cmdline":_cmdline, "PPID":_ppid}
			proc_results["SigHNG"] = True

		if _pid in results.keys():
			results["Results"] = dict(proc_results)

	print(results)
run() 
