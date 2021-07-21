import os
import subprocess
import time

def nooptcmd(command):
    subprocess.check_output(command,shell=True)

def clear():
    os.system("cls")

def loading(task,donemsg,amt,endtask,sec=0):
    dring = ["/","-","|"]
    amt2 = 0
    load = 0
    while amt2 != amt:
        clear()
        load += 1
        amt2 += 1
        if load == len(dring):
            load = 0
        print(f"{task} {dring[load]}")
        time.sleep(sec)
    if endtask != None:
        nooptcmd("touch endtask.py")
        with open("endtask.py","w") as endtaskz:
            endtaskz.write(str(endtask))
        nooptcmd("python endtask.py")
        nooptcmd("rm -rf endtask.py")
    return f"{task} : {donemsg}"
