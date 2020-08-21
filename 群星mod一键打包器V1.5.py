# -*- encoding: utf-8 -*-
'''
@File    :   群星mod一键打包器V1.5.py
@Time    :   2020/08/21
@Author  :   Ra1n 
@Version :   1.5
'''
import os
import re
import socket
import getpass
import zipfile
def Getpath():
    user_name = getpass.getuser() 
    global path 
    path='C:\\Users\\' + user_name + '\\Documents\Paradox Interactive\Stellaris\mod\\'
    print(path)
    try:
        dirs = os.listdir( path )
    except IOError:
        input("群星mod路径不存在，请确认是否安装正版群星/当前用户是否安装正版群星!按回车结束程序")
        os._exit(0)
    for filename in dirs:
        File=os.path.splitext(filename)[1]
        if File =='.mod':
            global file_path
            file_path=path+filename
            read_file=open(file_path,encoding='UTF-8')
            for line in read_file.readlines():
                key='name'
                if key in line:
                    global mod_name
                    mod_name=re.sub(r'[#$/\\]+',' ',line[6:-2])+".zip"
                Key="path"
                if Key in line:
                    global mod_path
                    mod_path=line[6:-2]
                    read_file.close()
                    Packing()
def Create_Modlist():
    try:
        Read_file=open(file_path,encoding='UTF-8')
        Line=Read_file.readlines()
        copy_path=path+mod_name[:-4]+'.mod'
        copy_file=open(copy_path,"w",encoding='utf-8')
        for i in range(len(Line)):
            key='name'
            Key='path'
            KEY='remote_file_id'
            change='archive'
            if key in Line[i]:
                Line[i]=Line[i][:6]+"【LOCAL】"+Line[i][6:]
            if Key in Line[i]:
                Line[i]=Line[i][:6].replace(Key,change)+Mod_Path+mod_name+Line[i][-2:]
            if KEY in Line[i]:
                Line[i]=""
        copy_file.writelines(Line)
        copy_file.close()
        Read_file.close()
        print(mod_name[:-4]+"已经添加到mod列表")
    except:
        print(mod_path+"添加mod列表失败，错误原因未知，请手动添加,mod目录路径："+file_path+"已经跳过该mod")

def Packing():
    try:
        print("保存路径："+Mod_Path+mod_name)
        z = zipfile.ZipFile(Mod_Path+mod_name, 'w', zipfile.ZIP_DEFLATED)
        for dirpath,dirmanes,filenames in os.walk(mod_path):
            fpath = dirpath.replace(mod_path,'')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                FiLe=os.path.splitext(filename)[1]
                if FiLe !='.mod':
                    a=os.path.join(dirpath,filename)
                    print("正在处理："+a)
                    z.write(a,fpath + filename)
        z.close()
        print(mod_name+'压缩成功')
        Create_Modlist()
    except:
        print(mod_path+"打包处理失败，错误原因未知，请手动打包,mod目录路径："+file_path+"已经跳过该mod")

def Mkdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print(path+' 创建成功,将会在该目录下存放mod压缩文件')
    else:
        print (path+' 目录已存在,将会在该目录下存放mod压缩文件')
if __name__ == "__main__":
    print("欢迎使用群星MOD一键打包器V1.5   Author：Ra1n")
    Mod_Path="D:/Stellaris_Mod/"
    Mkdir(Mod_Path)
    Getpath()
    print("感谢使用群星MOD一键打包器V1.5   Author：Ra1n")
    input("所有MOD打包处理完毕，请按回车键退出")
