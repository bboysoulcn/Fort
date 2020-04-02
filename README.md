

[![](https://img.shields.io/badge/@Bboysoul-black?style=flat)](https://www.bboy.app)
![](https://img.shields.io/github/followers/bboysoulcn)
![](https://img.shields.io/github/forks/bboysoulcn/Fort)
![](https://img.shields.io/github/stars/bboysoulcn/Fort)
![](https://img.shields.io/github/watchers/bboysoulcn/Fort.svg)

![](https://s1.ax1x.com/2020/04/02/GJlQFP.png)

<h6>一个简单的保存主机的小程序</h6>

### 菜单

- [菜单](#菜单)
- [使用方法](#使用方法)
- [其他功能](#其他功能)
- [Todo](#todo)
- [感谢](#感谢)


### 使用方法

clone脚本

`git clone https://github.com/bboysoulcn/Fort.git`

把Fort文件夹放入一个你喜欢的地方比如bin目录

`mv Fort bin`

安装依赖库

`pip install -r Fort/requirements.txt`

之后设置别名

`vim ~/.zshrc`

加入

`alias fort='python /Users/bboysoul/bin/Fort/main.py'`

使环境变量生效

`source ~/.zshrc`

之后把你的所有主机存入一个yaml文件中比如

`hosts.yaml`

```yaml
group1:
  - 10.10.10.10:10
  - 10.10.10.100
group2:
  - 10.10.10.1
  - 10.10.200.1
```

并且分好组，比如group1,group2，如果ssh端口不是22那么你可以在主机后面加上端口号比如

`10.10.10.10:10`

之后运行命令

`fort -f hosts.yml`

你可以看到下面界面

```bash
         > 请选择你的主机

        -> 0. 10.10.10.10:10
           1. 10.10.10.100
           2. 10.10.10.1
           3. 10.10.200.1

           <第1页/共12项 下一页>

           Powered by Bboysoul
```

如果你配置了免密登陆，回车即可连接主机

### 其他功能

在菜单界面输入

- s 可以查找主机
- q 退出菜单
- k 光标向上
- j 光标向下
- h 上一页
- l 下一页

### Todo

- √ 添加分组的功能
- √ hosts文件作为参数传入
- □ 主机列表后面加入组名称
- □ -s参数批量设置免密登陆 

### 感谢

`https://github.com/gojuukaze/tty_menu`

`https://github.com/huangguang93/terminal_menu`