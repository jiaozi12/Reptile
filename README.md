# Reptile
## 百度爬虫，用以爬取百度图片上的图像数据
### 目录
#### ————image
#### ————百度爬虫(Windows软件).exe
#### ————百度爬虫(Windows软件).py
### 文件说明
image文件夹中存放应用程序启动所需要加载的图片文件，为保证正常使用，需将image文件夹和exe文件放在同一目录下

百度爬虫(Windows软件).exe为Windows可执行程序，可以直接双击运行

百度爬虫(Windows软件).py是实现源码
### exe文件制作说明
1.前端界面使用python3的tkinter图形库编写

2.使用Pyinstaller将python代码打包成exe文件，若无Pyinstaller环境，可使用pip命令进行安装
~~~
pip install pyinstaller
~~~
3.安装完成后，在命令行执行命令进行打包
~~~
pyinstaller -F -w 百度爬虫(Windows软件).py
~~~
说明

命令中-w的意思是：直接发布的exe应用带命令行调试窗口，在指令内加入-w命令可以屏蔽

命令中-F的意思是：使用-F指令可以把应用打包成一个独立的exe文件，否则是一个带各种dll和依赖文件的文件夹
4.完成后在新生成的dist文件夹中可找到百度爬虫(Windows软件).exe

致谢

[爬虫部分的代码参考的一篇CSDN博客](https://blog.csdn.net/qq_40774175/article/details/81273198)
