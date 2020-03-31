from tty_menu import tty_menu
import os
from menu import Menu

def menu(hosts_list):
    m = Menu()
    m.menu_style(page_size=5)
    pos = m.menu(hosts_list, title="请选择你的主机")
    #根据长度判断是不是有端口
    if len(pos[1].split(":"))==2:
        ip = pos[1].split(":")[0]
        port = pos[1].split(":")[1]
    else:
        ip = pos[1].split(":")[0]
        port = "22"
    if pos[1] is not None:
        # 连接主机
        os.system("ssh root@%s -p %s" % (ip,port))
    else:
        quit

def read_hosts():
    with open('./hosts') as f:
        hosts_list = []
        while True:
            line = f.readline()
            if not line.strip():
                break
            else:
                hosts_list.append(line.strip())
        return hosts_list

if __name__ == "__main__":
    hosts_list = read_hosts()
    menu(hosts_list)

    