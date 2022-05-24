# -*- coding: utf-8 -*-
"""
@Time    : 2022/1/3 11:32
@Author  : AI悦创
@FileName: main.py
@Software: PyCharm
@Blog    ：https://www.aiyc.top
@公众号   ：AI悦创
@description：
"""
import tkinter as tk


class MainWindow():
	def __init__(self):
		# 创建主窗口
		self.window = tk.Tk()
		self.window.minsize(300, 300)  # 设置窗口的最小值，如果不设置最小值的话，窗口是可以被用户随意拖动的。我们为了里面的组件能够方便的展示出来，不允许用户把此窗口缩小的很小。
		self.window.title("示例1")
		# 添加组件
		self.addComponents()

		# 进入消息循环
		self.window.mainloop()

	def addComponents(self):
		# self.window: 父组件
		my_frame = tk.Frame(self.window, width=100,
							height=300)  # 就是要把组件 frame 放在哪个主窗口：self.window。 my_frame 又是其他组件的父组件。
		# 设置 my_frame 的布局方式，在最上面
		my_frame.pack(side=tk.TOP)
		# 创建按钮
		# tk.Button(父窗体, text="str")
		# my_button = tk.Button(my_frame, text="执行", command=self.button_clicked)
		my_button = tk.Button(my_frame, text="执行", command=self.button_clicked)
		my_button.pack(side=tk.LEFT)
		

	def button_clicked(self):
		print("啊哦，按钮被点击了！")


if __name__ == '__main__':
	MainWindow()