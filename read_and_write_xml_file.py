# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 11:10:48 2020
print
@author: Administrator
"""
from lxml import etree
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from make_branches import *
from lxml import objectify
from tkinter import messagebox
import re

#调用filedialog，弹窗选择要读取的xml文件
open_xml = tk.Tk()
open_xml.withdraw()
filepath = filedialog.askopenfilename()
index_filename = filepath.rfind("/") + 1
file_name = filepath[index_filename:]
#print(type(file_name))
#print(filepath)
open_xml.destroy()

#用etree模块读取引入的xml文件
parsed = etree.parse(filepath) 
#获取xml文件的根目录
root = parsed.getroot()

#通过索引，依次获取模拟量和数字量信号所在的目录
variables_ana_bcu = root[4][2][3][0]
#print(type(variables_ana_bcu))
#print(type(variables_ana_bcu.tag))
variables_dig_bcu = root[4][2][3][1]
variables_ana_physical = root[4][2][3][2]
variables_dig_physical = root[4][2][3][3]

def get_var(variables):
    """定义get_var函数，遍历目录，从里边读取address，variable id，和variable size等信息，
    并给不同的变量，添加不同的标识符【BCU_analog, BCU_digital, physical_analog, physical_digital】,
    最终将这些信息存储到一个pandas模块的DataFrame里
    """
    list_temp = []
    for child in variables:
        dict_temp = {}
        for subchild in child.iter():
            dict_temp[subchild.tag] = subchild.text
        list_temp.append(dict_temp)
    #return list_temp
    data = pd.DataFrame(list_temp)
    #print(data.head(10))
    data = data[["address", "variable_id", "variable_size"]]
    if variables.tag == "analogue_addresses":
        data["type"] = "BCU_analog"
    elif variables.tag == "digital_addresses":
        data["type"] = "BCU_digital"
    elif variables.tag == "physical_analogue_addresses":
        data["type"] = "physical_analog"
    elif variables.tag == "physical_digital_addresses":
        data["type"] = "physical_digital"
    return data

#把读取的DataFrame存储起来
results_1 = get_var(variables_ana_bcu)
#print(results_1)
results_2 = get_var(variables_dig_bcu)  
results_3 = get_var(variables_ana_physical)  
results_4 = get_var(variables_dig_physical)    
#print(results_4)

#合并4个DataFrame
results = pd.concat([results_1, results_2, results_3, results_4])

#用变量名作为该DataFrame的索引
results.set_index("variable_id", inplace=True)
#print(results)

#添加重命名栏,默认为空
results["newname"] = ""
#print(results.head(30))
#results.to_csv("C:\\results.txt")

#把合并后的DataFrame的index转成列表
ls_01 = list(results.index)
#print(list_for_selection, len(list_for_selection))

ls_03 = []
ls_04 = []


#定义一个Tk对象，用来交互
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("read_and_write_xml_file    Version1.5")
        self.var = tk.StringVar()
        self.newname = tk.StringVar()
        self.filename = tk.StringVar()
        #print(file_name)
        #把读取的文件名显示到窗口
        self.filename.set(file_name)
        #print(self.filename)
        self.var.trace("w", self.show_selection)
        self.lab = tk.Label(self, text="输入正则表达式", height=1, fg="gray")
        self.lab_change = tk.Label(self, text="新变量名", height=1, fg="gray")        
        
        #定义输入框
        self.entry = tk.Entry(self, textvariable=self.var)
        
        self.rename_button = tk.Button(self, text="修改变量", command=self.rename_var, height=1, fg="blue")
        #定义变量名输入框
        self.rename_entry = tk.Entry(self, textvariable=self.newname)
        #定义选择栏
        self.listbox = tk.Listbox(self, selectmode=EXTENDED, height=20, width=30)
        #定义已选择栏
        self.selected_box = tk.Listbox(self, selectmode=SINGLE, height=20, width=30)
        #清空所选
        self.clear = tk.Button(self, text="清空变量", command=lambda: self.selected_box.delete(0, END), fg="blue")
        #注释栏
        self.comment = tk.Label(self, text="正则表达式相关注释\n不区分大小写\n\d  匹配单个数字0-9\n.*  \
. 匹配任意单个字符 * 表示重复任意次\n[a-c] [abc]匹配a或b或c\n^ 表示开始\n$ 表示结束\n\n示例\ncar\d[a-c]_asp\d\ncar.*bcpaxle\
\n.*speedaxle\d\n.*speedaxle\d$\n^ccu\n\n注意请使用英文输入法", justify=LEFT)      

        #定义buttons
        self.add = tk.Button(self, text="添加变量", command=self.add_var, fg="blue")
        self.delete = tk.Button(self, text="删除变量", command=self.delete_var, fg="blue")
        self.save_to_XML = tk.Button(self, text="保存至Brake Consultant", command=self.save_to_XML, fg="blue")
        self.reload_XML = tk.Button(self, text="重新载入xml文件", command=self.reload, fg="blue")
        self.file = tk.Label(self, textvariable=self.filename, height=1, fg="gray")
                    
        #opts = {}
        opts = {"ipadx":0, "ipady":0, "sticky": "nswe"}
        
        self.lab.grid(row=0, column=0, columnspan=1, **opts)
        self.entry.grid(row=0, column=1, columnspan=1, **opts)
        self.lab_change.grid(row=0, column=2, columnspan=1, **opts)
        self.rename_entry.grid(row=0, column=3, columnspan=1, **opts)
        
        self.listbox.grid(row=1, column=0, **opts)
        self.selected_box.grid(row=1, column=1, **opts)
        self.comment.grid(row=1, column=3, **opts)
        
        self.add.grid(row=2, column=0, **opts)
        self.delete.grid(row=2, column=1, **opts)
        self.rename_button.grid(row=2, column=2, **opts)
        self.clear.grid(row=2, column=3, **opts)
        
        self.reload_XML.grid(row=3, column=0, **opts)
        self.save_to_XML.grid(row=3, column=3, **opts)
        self.file.grid(row=3, column=1, columnspan=2, **opts)
 
        self.num = tk.Listbox(self, height=20, fg="green", width=8)
        self.num.grid(row=1, column=2)
        numbers = range(1, 20)
        self.num.insert(0, *numbers)
        
    def show_selection(self, *args):
        value = self.var.get()
        pattern = value
        #print(pattern)
        ls_02 = []
        self.listbox.delete(0, END) #改动关键字，会先使得可选列表先清空
        for item in ls_01:
            #if value in item or value.capitalize() in item or value.upper() in item:
            if re.search(pattern, item, re.I):       
                ls_02.append(item)        
        if ls_02:
            ls_02.sort()
            self.listbox.insert(0, *ls_02)
        #else:
            #self.listbox.insert(0, *ls_02)
    def add_var(self, *args):
        keys = self.listbox.curselection()
        for key in keys:
            value = self.listbox.get(key)
            self.selected_box.insert(END, value)
            
    def delete_var(self, *args):
        self.selected_box.delete(ANCHOR)
    
    def rename_var(self, *args):
        newname = self.newname.get()
        #print(newname)
        key = self.selected_box.curselection()
        if newname and key:
            selected_var = self.selected_box.get(key)
            results.loc[selected_var]["newname"] = newname
            #print(results.loc[selected_var])
            messagebox.showinfo("提示", selected_var+"已经更名为"+newname)
        else:
            messagebox.showinfo("警告", "请先选择要更改的变量并输入新名称！")
            
    def reload(self, *args):
        self.var.set("")
        self.listbox.delete(0, END)
        self.selected_box.delete(0, END)
        
        
        reopen_xml = tk.Tk()
        reopen_xml.withdraw()
        filepath_re = filedialog.askopenfilename()
        index_filename_re = filepath_re.rfind("/") + 1
        file_name_re = filepath_re[index_filename_re:]
        #print(file_name_re)
        reopen_xml.destroy()
        self.filename.set(file_name_re)
        
        if filepath_re:
            parsed_re = etree.parse(filepath_re)
            root_re = parsed_re.getroot()
            variables_ana_bcu_re = root_re[4][2][3][0]
            variables_dig_bcu_re = root_re[4][2][3][1]
            variables_ana_physical_re = root_re[4][2][3][2]
            variables_dig_physical_re = root_re[4][2][3][3]
            #把读取的DataFrame存储起来
            results_a = get_var(variables_ana_bcu_re)
            print(results_a.head(10))
            results_b = get_var(variables_dig_bcu_re)  
            results_c = get_var(variables_ana_physical_re)  
            results_d = get_var(variables_dig_physical_re)    
            
            #合并4个DataFrame
            global results
            results = pd.concat([results_a, results_b, results_c, results_d])
            
            #用变量名作为该DataFrame的索引
            results.set_index("variable_id", inplace=True)
            
            #添加重命名栏,默认为空
            results["newname"] = ""
            #print(results_re.head(30))
    
            #把合并后的DataFrame的index转成列表
            global ls_01
            ls_01 = list(results.index)
            print(results.loc[["BsEbActive"]])        
        else: 
            pass

    def save_to_XML(self, *args):
        ls_04 = list(self.selected_box.get(0, END))
        dataframe = results.loc[ls_04]
        long = len(ls_04)
        if long > 0 and long <= 19: 
            #选择要保存的路径
            save_xml = tk.Tk()
            save_xml.withdraw()
            save_path = filedialog.asksaveasfilename()
            index = save_path.rfind("/") + 1
            save_name = save_path[index:]
            #print(save_name)
            save_xml.destroy()
            #每次执行save_to_xml,都重新创建xml文件的根目录
            E = objectify.ElementMaker(annotate=False)
            base = E.real_time_data_screen(
                    E.screen_title(
                            E.english(save_name),
                            E.alternate_language(save_name)
                            ),
                    E.screen_classification(
                            E.scope_id("NETWORK"),
                            E.bogie_id("UNDEFINED"),
                            E.unit_id("UNDEFINED"),
                            E.user_group_id(0),
                            E.car_code(0),
                            E.common_screen("false"),
                            E.access_level(0)
                            ),
                    E.mFileName(save_path),
                    )
            branch_ana = E.analogue_variables()
            branch_dig = E.digital_leds()

            #print(ls_04, len(ls_04))
            #print(type(ls_04))
            gauge_id = -1
            led_id = -1
            for index, row in dataframe.iterrows():
                if row["newname"]:
                    var_name = row["newname"]
                else:
                    var_name = index
                alt_name = index
                var_id = row["address"]
                var_size = row["variable_size"]
                var_type = row["type"]
            
                if var_type == "BCU_analog":
                    gauge_id = gauge_id + 1
                    add_analog_bcu(branch_ana, var_name, var_id, var_size, gauge_id, alt_name)
                elif var_type == "BCU_digital":
                    led_id = led_id + 1
                    add_digital_bcu(branch_dig, var_name, var_id, var_size, led_id, alt_name)
                elif var_type == "physical_analog":
                    gauge_id = gauge_id + 1
                    add_analog_physical(branch_ana, var_name, var_id, var_size, gauge_id, alt_name)
                elif var_type == "physical_digital":
                    led_id = led_id + 1
                    add_digital_physical(branch_dig, var_name, var_id, var_size, led_id, alt_name)
            base.append(branch_ana)
            base.append(branch_dig)
            if save_name:
                etree.ElementTree(base).write(save_path+".xml", pretty_print=True)
                messagebox.showinfo("提示", "成功生成xml文件到"+save_path+".xml")
            
        elif long > 19: #如果选择好的列表里个数超过19就报错
            messagebox.showinfo("警告", "超过19个变量\n请重新选择")
        elif long == 0:
            messagebox.showinfo("警告", "没有选中变量")
                  
win = Window()
win.mainloop()







