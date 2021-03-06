#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import re
import sys
import termios
import tty


class Menu(object):
    def __init__(self, clear_screen=True):
        if clear_screen:
            os.system("clear")
        self._term_start_pos = self.getpos()[0]
        self._term_end_pos = self._term_start_pos
        self.offset = " " * 8   # 菜单距离左侧偏移量
        self.id_show = True  # 是否显示列表id
        self.title = True  # 标题是否显示
        self.foot = True   # 页脚是否显示
        self.page_size = 10  # 每页显示多少条
        self.title_delimiter = "  "  # 定义标题分隔符
        self.pointer = "->"   # 定义选择指示器
        self.title_color = "purple"
        self.foot_color = "yellow"
        self.body_word_color = ""
        self.body_word_switch_color = "blue"

    def menu_style(self, offset=8, id_show=True, title=True, foot=True,
                   page_size=10, title_delimiter=" > ", pointer="->",
                   title_color="purple", foot_color="yellow", body_word_color="",
                   body_word_switch_color="blue"):
        """
        菜单样式设置
        供选择的颜色：'black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'
        :param offset:
        :param id_show:
        :param title:
        :param foot:
        :param page_size:
        :param title_delimiter:
        :param pointer:
        :param title_color: 'black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'
        :param foot_color: 'black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'
        :param body_word_color: 'black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'
        :param body_word_switch_color: 'black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'
        :return:
        """
        self.offset = " " * offset   # 菜单距离左侧偏移量
        self.id_show = id_show  # 是否显示列表id
        self.title = title  # 标题是否显示
        self.foot = foot   # 页脚是否显示
        self.page_size = page_size  # 每页显示多少条
        self.title_delimiter = title_delimiter  # 定义标题分隔符
        self.pointer = pointer   # 定义选择指示器
        self.title_color = title_color   # 标题颜色
        self.foot_color = foot_color  # 页脚颜色
        self.body_word_color = body_word_color  # 主体文字颜色
        self.body_word_switch_color = body_word_switch_color  # 选择的主体文字颜色

    def _font_style(self, string, mode='', fg='', bg=''):
        """字体样式选择"""
        styles = {
            'fg': {
                'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
                'blue': 34, 'purple': 35, 'cyan': 36, 'white': 37,
            },
            'bg': {
                'black': 40, 'red': 41, 'green': 42, 'yellow': 43,
                'blue': 44, 'purple': 45, 'cyan': 46, 'white': 47,
            },
            'mode': {
                'bold': 1, 'underline': 4, 'blink': 5, 'invert': 7,
            },
            'default': {
                'end': 0,
            }
        }
        mode = '%s' % styles['mode'][mode] if mode in styles['mode'].keys() else ''
        fore = '%s' % styles['fg'][fg] if fg in styles['fg'].keys() else ''
        back = '%s' % styles['bg'][bg] if bg in styles['bg'].keys() else ''
        style = ';'.join([s for s in [mode, fore, back] if s])
        style = '\033[%sm' % style if style else ''
        end = '\033[%sm' % styles['default']['end'] if style else ''
        return '%s%s%s' % (style, string, end)

    def getpos(self):
        buf = ""
        stdin = sys.stdin.fileno()
        tattr = termios.tcgetattr(stdin)

        try:
            tty.setcbreak(stdin, termios.TCSANOW)
            sys.stdout.write("\x1b[6n")
            sys.stdout.flush()

            while True:
                buf += sys.stdin.read(1)
                if buf[-1] == "R":
                    break
        finally:
            termios.tcsetattr(stdin, termios.TCSANOW, tattr)

        # reading the actual values, but what if a keystroke appears while reading
        # from stdin? As dirty work around, getpos() returns if this fails: None
        try:
            matches = re.match(r"^\x1b\[(\d*);(\d*)R", buf)
            groups = matches.groups()
        except AttributeError:
            return None
        return int(groups[0]), int(groups[1])

    def clear_old_content(self):
        """
        清理屏幕
        """
        self._term_end_pos = self.getpos()[0]
        back_line = self._term_end_pos - self._term_start_pos
        for i in range(back_line):
            sys.stdout.write("\r\033[K\033[1A")
            sys.stdout.flush()

    def getch(self):
        """获取键盘输入"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                ch += sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def title_box(self, title):
        """ title block"""
        if self.title:
            # title_base = "\n" + self.offset + (len(self.pointer) + 1) * " " + "主菜单"
            title_base = "\n" + (len(self.pointer) + 6) * " "
            if title is not None and isinstance(title, list):
                title_info = title_base + self.title_delimiter + self.title_delimiter.join(title)
            else:
                title_info = title_base
            sys.stdout.write(self._font_style(title_info, mode="bold", fg=self.title_color) + '\n\n')
            sys.stdout.flush()

    def body_box(self, pos, choose, start):
        """ body block """
        i = 0
        s = ""
        while i < self.page_size:
            if i >= len(choose):
                s += "\r\n"
                i += 1
                continue
            line_content = str(choose[i][1])
            if i == pos:
                content = str(start + i) + ". " + line_content if self.id_show else line_content
                temp = self.pointer + " " + content
                temp = self._font_style(temp, fg=self.body_word_switch_color, bg="")
            else:
                content = str(start + i) + ". " + line_content if self.id_show else line_content
                temp = (len(self.pointer) + 1) * " " + content
                temp = self._font_style(temp, fg=self.body_word_color)
            s += "\r" + self.offset + temp + "\n"
            i += 1
        sys.stdout.write(s)
        sys.stdout.flush()

    def foot_box(self, total, start, page):
        """  foot block """
        s = ""
        next_page = False
        prev_page = False
        if self.foot:
            if start + self.page_size < total:
                next_page = True
            if start - self.page_size >= 0:
                prev_page = True

            foot = "\n" + self.offset + (len(self.pointer) + 1) * " " + "<第{}页/共{}项".format(page, total)
            if next_page and prev_page:
                foot = foot + " 上一页 下一页"
            elif next_page:
                foot = foot + " 下一页"
            elif prev_page:
                foot = foot + " 上一页"
            foot += ">"
            foot += "\n\n" + (len(self.pointer) + 9) * " " + "Powered by Bboysoul"
            s = s + self._font_style(foot, fg=self.foot_color) + "\n"
        sys.stdout.write(s)
        sys.stdout.flush()

    def search_box(self, choose, title):
        self.clear_old_content()
        search_title = ["搜索"] if title is None else title + ["搜索"]
        self.title_box(search_title)
        s = "\r\n" + self.offset + "关键字: "
        sys.stdout.write(s)
        sys.stdout.flush()
        keyword = sys.stdin.readline().strip()
        filter_choose = list(filter(lambda x: keyword in str(x[1]), choose))
        return filter_choose

    def menu_box(self, choose, pos, page_data, page, start, title=None):
        self.clear_old_content()
        total = len(choose)
        self.title_box(title)
        self.body_box(pos, page_data, start)
        self.foot_box(total, start, page)

    def menu(self, choose, title=None):
        pos = 0
        start = 0
        page = 1
        page_size = self.page_size

        if title and isinstance(title, list) is False:
            title = [str(title)]
        choose_with_id = [[i, v] for i, v in enumerate(choose)]
        choose_list = choose_with_id

        while True:
            total = len(choose_list)
            if start + page_size < total:
                page_list = choose_list[start:start + page_size]
            else:
                page_list = choose_list[start:total]

            # 控制指针到达边界时
            if pos < 0:
                pos = len(page_list) - 1
            elif pos >= len(page_list):
                pos = 0

            self.menu_box(choose_list, pos,  page_list, page, start, title)

            key = self.getch()
            if key == "\r":  # enter
                if len(choose_list) != 0:
                    id = page_size * (page - 1) + pos
                    return choose_list[id][0], choose_list[id][1]

            elif key in ["q", "Q"]:  # 返回
                return -1, None

            elif key in ["\x1b[A", "k", "K"]:
                pos -= 1

            elif key in ["\x1b[B", "j", "J"]:
                pos += 1

            elif key in ["\x1b[D", "h", "H"]:  # 上一页
                if start - page_size >= 0:
                    pos = 0
                    start = start - page_size
                    page -= 1

            elif key in ["\x1b[C", "l", "L"]:  # 下一页
                if start + page_size < total:
                    pos = 0
                    start = start + page_size
                    page += 1

            elif key in ["S", "s"]:  # 搜索
                choose_list = self.search_box(choose_list, title)

            elif key in ["x", "x"]:  # 取消搜索
                choose_list = choose_with_id


if __name__ == '__main__':
    test_data = ["阿里巴巴", "百度", "腾讯", "今日头条", "爱奇艺", "美团", "饿了吗", "小米",
                 "支付宝", "京东", "拼多多", "微博", "携程", "网易", "哔哩哔哩", "迅雷", "360"]
    m = Menu(clear_screen=False)
    m.menu_style(page_size=10, title=False)
    pos = m.menu(test_data, title="互联网公司")
    print("Your word is ", pos)