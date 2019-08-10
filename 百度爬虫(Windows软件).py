# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 17:21:09 2019

@author: qiqi
"""

import re
import requests
from urllib import error
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
 
num = 0
List = []

def GUI():
    global windows,tips,word
    windows = tk.Tk()
    windows.title('百度爬虫')
    windows.iconbitmap('image/icon.ico')
    windows['background'] = 'white'
    width, height = 800, 600
    
    '''窗口居中显示'''
    windows.geometry('%dx%d+%d+%d' % (width, height, (windows.winfo_screenwidth() - width) / 2, 
                                               (windows.winfo_screenheight() - height) / 2))
    windows.update()
    
    '''窗口最大值'''
    windows.maxsize(windows.winfo_screenwidth(), windows.winfo_screenheight())
    
    '''窗口最小值'''
    windows.minsize(400, 400)
    
    '''标题'''
    title_image = tk.PhotoImage(file = 'image/title_image.png')
    title_label = tk.Label(windows,image=title_image,bg='white')
    title_label.pack()
    
    '''提示'''
    tips = tk.Label(windows, text='请输入要爬取的图片类别\n输入完成后点击搜索', bg='white', font='楷书', width=100, height=3, wraplength=300)
    tips.place(relx=0.7, rely=0.31, anchor='center')
    
    '''作者'''
    writer = tk.Label(windows, text='作者-王小齐', bg='white', font='楷书', width=20, height=1)
    writer.place(relx=0.5, rely=0.85, anchor='center')
    
    '''选择存储位置按钮'''
    button1 = tk.Button(windows, text='选择存储位置',font='楷书', width=20, height=1, command=Choose_location)
    button1.place(relx=0.23, rely=0.46, anchor='center')
    
    '''搜索按钮'''
    button2 = tk.Button(windows, text='搜索', font='楷书', width=20, height=1, command=Find)
    button2.place(relx=0.23, rely=0.3, anchor='center')
    
    '''开始下载按钮'''
    button3 = tk.Button(windows, text='开始下载', font='楷书', width=20, height=1, command=StartDowmloadPicture)
    button3.place(relx=0.23, rely=0.62, anchor='center')
    
    '''用于输入要爬取内容Entry'''
    word = tk.StringVar()
    entry = tk.Entry(windows, textvariable=word)
    entry.place(relx=0.61, rely=0.51)
    
    windows.mainloop()
    
    

def Find():
    '''在百度图片中寻找指定类别的图片'''
    global List,tips,word,url,s,windows
    if word.get() == '':
        tips['text'] = '您还未输入要爬取的图片类别\n请输入要爬取的图片类别\n输入完成后点击搜索'
        windows.update()
        return
    tips['text'] = '正在检测图片总数，请稍等.....'
    windows.update()
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word.get() + '&pn='
    t = 0
    s = 0
    while t < 10000:
        Url = url + str(t)
        try:
            Result = requests.get(Url, timeout=10)
        except BaseException:
            t = t + 60
            continue
        else:
            result = Result.text
            
            '''利用正则表达式找到图片url'''
            pic_url = re.findall('"objURL":"(.*?)",', result, re.S)
            s += len(pic_url)
            if len(pic_url) == 0:
                break
            else:
                List.append(pic_url)
                t = t + 60
    tips['text'] = '经过检测%s类图片共有%d张\n请点击选择存储位置' % (word.get(), s)
    windows.update()
    return


def Choose_location():
    '''选择文件存储位置'''
    global windows,image_path,tips
    root = tk.Tk()
    root.withdraw()
    image_path_temp = filedialog.askdirectory()
    if image_path_temp != '': image_path = image_path_temp
    tips['text'] = '请点击开始下载'
    windows.update()
    return



def DowmloadPicture(html, keyword):
    '''下载一个页面的图片'''
    global num,tips,image_path,s
    
    '''利用正则表达式找到图片'''
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    for each in pic_url:
        tips['text'] = '正在下载图片\n' + str(num+1) + '/' + str(s)
        windows.update()
        try:
            if each is not None:
                '''获取图片'''
                pic = requests.get(each, timeout=10)
            else:
                continue
        except BaseException:
            tips['text'] = '错误，当前图片无法下载'
            windows.update()
            continue
        else:
            '''将图片存到外存'''
            string = image_path + '/' + keyword + '_' + str(num) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= s:
            return
        
        
        
def StartDowmloadPicture():
    '''下载找到的全部图片'''
    global url,s,tips,word,windows,image_path,num
    if word.get() == '':
        tips['text'] = '您还未输入要爬取的图片类别\n请输入要爬取的图片类别\n输入完成后点击搜索'
        windows.update()
        return
    if image_path == '':
        tips['text'] = '你还未选择存储位置'
        windows.update()
        return
    t = 0
    tmp = url
    while t < s:
        try:
            url = tmp + str(t)
            result = requests.get(url, timeout=10)
        except error.HTTPError as e:
            tips['text'] = '网络错误，请调整网络后重试'
            windows.update()
            t += 60
        else:
            DowmloadPicture(result.text, word.get())
            t += 60
    
    if num == s:
        messagebox.showinfo(title='提示', message='下载完成')
    else:
        messagebox.showinfo(title='提示', message='下载完成，共有%d张图片下载失败' % (s-num))


'''主程序入口'''
if __name__ == '__main__':
    GUI()