from tty_menu import tty_menu
import os
from menu import Menu
import sys
import getopt
import yaml

# 定义菜单
def menu(hosts_list):
    m = Menu()
    m.menu_style(page_size=5)
    pos = m.menu(hosts_list, title="请选择你的主机")
    #根据长度判断是不是有端口

    if pos[1] is not None:
        # 连接主机
        if len(pos[1].split(":"))==2:
            ip = pos[1].split(":")[0]
            port = pos[1].split(":")[1]
        else:
            ip = pos[1].split(":")[0]
            port = "22"
        os.system("ssh root@%s -p %s" % (ip,port))
    else:
        quit

def print_help():
    pass

def get_opt():
    # 从终端获取参数输入
    opts,args = getopt.getopt(sys.argv[1:],'-h-f:-g:-v',["help","filename","group","version"])
    # 判断用户输入参数是否为空
    command = {}
    if len(opts) >0:
        for opt_name,opt_val in opts:
            if opt_name in ('-f','--filename'):
                command['filename'] = opt_val
            if opt_name in ('-h','--help'):
                print("help")
                exit()
            if opt_name in ('-v','--version'):
                print('v1.0 Powered by Bboysoul')
                exit()
            if opt_name in ('-g','--group'):
                command['group'] = opt_val
        return command
    else:
        return {}



# 获取主机组
def read_group(filename):
    try:
        f = open(filename)
    except Exception as e:
        print(e)
        exit()
    all_content = yaml.load(f,Loader=yaml.BaseLoader)
    group = list(all_content.keys())
    return(group)

# 获取主机
def read_hosts(command):
    hosts = []
    # 判断输入的参数赋值给filename和group
    if 'filename' in command.keys():
        filename = command['filename']
    else:
        filename = './hosts'
    if 'group' in command.keys():
        group = [command['group']]
    else:
        group = read_group(filename)
    # 读取hosts文件
    try:
        f = open(filename)
    except Exception as e:
        print(e)
        exit()
    # 获取文件所有内容
    all_hosts = yaml.load(f,Loader=yaml.BaseLoader)
    # 获取所有主机
    for i in group:
        hosts=all_hosts[i]+ hosts
    return hosts


def main():
    #获取参数
    command = get_opt()
    # 获取主机列表
    hosts_list = read_hosts(command)
    # 生成菜单
    menu(hosts_list)



if __name__ == "__main__":
    main()



    