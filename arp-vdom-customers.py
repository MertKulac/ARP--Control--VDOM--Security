import paramiko
import re
from termcolor import colored
from queue import Queue
import time, smtplib
import pandas as pd
import schedule
import time

def vdom_update():
    hosts = []
    ExcelExport = [["Vdom_Name", "Arp"]]
    ExcelData = pd.read_excel("vdom_list.xlsx")

    for x in range(len(ExcelData)):
        vdomName = ExcelData["OBJE-NETWORK"][x]
        print(vdomName)
        hosts.append("%s" % (vdomName))

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    bekci = "10.222.247.240"
    bekci_yedek1 = "bekci.superonline.net"
    VDOM_IP = "10.42.1.104"
    Flag = False

    try:
        ssh.connect(VDOM_IP, port=22, username=username, password=password, timeout=20)
        remote_connection = ssh.invoke_shell()
        print(colored("Connected_Vdom:" + VDOM_IP, "blue"))
        remote_connection.send("config vdom" + "\r")
        time.sleep(1)
        for host in hosts:

            remote_connection.send(" edit {}".format(host) + " \n")
            remote_connection.send("get system arp" + "\r")
            output = remote_connection.recv(65535)
            result = output.decode('ascii').strip("\n")
            print(result)
            with open('vdom_sonuc.txt', 'a') as f:
                f.write(str(result) + "\n")
            remote_connection.send("next" + "\r")
            time.sleep(1)

    except Exception as e:
        print("erisim yok_" + "\n")
global password
username = "admin"
password = " admin "

vdom_update()
