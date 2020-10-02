# Identify the use of the nohup command
The project is designed to locate commands that executes processes detached from session. </br>
Attacker can use commands like nohup, setsid to run malicious process detached from his session </br>
At this moment the project is written only to detect the nohup command.

# Detect nohup

  Nohup, short for no hang up is a command in Linux systems that keep processes running even after exiting the shell or terminal.

  # 1. Detect by File Descriptors 
  By default nohup command redirects the output and error of the executable to file named nohup.out. </br>
  In case an attacker didn't change the output/error location the process should have file decriptor to file named nohup.out
  
![alt text](https://github.com/0x0ranm/NoHup-Finder/blob/master/fd.png?raw=true)


  # 2. Detect by Environment variable
  
  There are some special environment variables in linux.
  One special environment variable is the variable $_. </br>
  This variable holds the last parameter of the last command.</br>
  For example: </br>
  &nbsp;&nbsp;&nbsp;if we run ps aux, the variable will get the value aux. </br>
  &nbsp;&nbsp;&nbsp;but if we run the command ps without parameters, the variable will get the value ps. </br>
  So if we run the command: </br>
   &nbsp;&nbsp;&nbsp; nohup sleep 1000 </br>
  
  The last command that will save in our process environment variables is the nohup command. </br>
  Each process stores in the file /proc/\<pid\>/environ all of his environment variables. </br>
  
  ![alt text](https://github.com/0x0ranm/NoHup-Finder/blob/master/Environment.png?raw=true)
  
  # 3. Detect by specific signal value
  
  When we close the terminal all the processes under our session get signal called SIGHUP. </br>
  This signal indicates that our session was terminate and the processes under the session should be terminated. </br>
  As I wrote before, nohup command is short for no hang up, the command sets the function handles SIGHUP signals to SIGIGN ( Signal Ignore ) </br>
  
  SIG_IGN specifies that the signal should be ignored.
  
  
  ![alt text](https://github.com/0x0ranm/NoHup-Finder/blob/master/Source.png?raw=true)
  
  
  In case we want to check if a process set SIGHUP handle to SIGIGN we can check the file /proc/\<pid\>/status. </br>
  This file contains all information about each sighandles and which signals each handle should be used. </br>
  For example, the file contains the follow lines: </br>
  Each line contains 16bit bitmap, each bit represents another signal. </br>
  In our case the LSB in SigIgn line represents SIGHUP signals. </br>
 
&nbsp;&nbsp;&nbsp;SigPnd: 0000000000000000 </br>
&nbsp;&nbsp;&nbsp;ShdPnd: 0000000000000000 </br>
&nbsp;&nbsp;&nbsp;SigBlk: 0000000000000000 </br>
&nbsp;&nbsp;&nbsp;SigIgn: 0000000000000001 </br>
&nbsp;&nbsp;&nbsp;SigCgt: 0000000000000000 </br>
&nbsp;&nbsp;&nbsp;CapInh: 0000000000000000 </br>
&nbsp;&nbsp;&nbsp;CapPrm: 0000000000000000 </br>
&nbsp;&nbsp;&nbsp;CapEff: 0000000000000000 </br>
&nbsp;&nbsp;&nbsp;CapBnd: 0000003fffffffff </br>
&nbsp;&nbsp;&nbsp;CapAmb: 0000000000000000 </br>


# POC

In case you run the script without root permissions you will not be able to run all over the processes </br>
Usage: python3 nohup_detector.py 


# TODO
- [ ] Write volatility script to detect usage of nohup

