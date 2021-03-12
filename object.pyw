# -*- encoding: utf-8 -*-
'''
@File    :   object.py
@Time    :   2021/03/11
@Author  :   Ra1n 
@Version :   3.0
'''
# here put the import lib
import re
import getpass
import os
import wx
import zipfile
import time
import threading
from wx.lib.pubsub import pub

class MyForm(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="正在处理中，请勿关闭", pos=wx.DefaultPosition,
                          size=wx.Size(-1, -1), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        gSizer2 = wx.GridSizer(0, 3, 0, 0)
        self.m_staticText2 = wx.StaticText(
            self, wx.ID_ANY, "当前进度", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        gSizer2.Add(self.m_staticText2, 0, wx.ALL |
                    wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.m_gauge1 = wx.Gauge(
            self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL) #百分比
        self.m_gauge1.SetValue(0)
        gSizer2.Add(self.m_gauge1, 0, wx.ALL |
                    wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(gSizer2)
        self.Layout()
        gSizer2.Fit(self)
        self.Centre(wx.BOTH)
        """绑定事件"""
        pub.subscribe(self.updateDisplay, "update")

    def updateDisplay(self, msg,alL):
        t = int((int(msg)/int(alL))*100)
        if isinstance(t, int):  # 如果是数字，说明线程正在执行，显示数字
            self.m_staticText2.SetLabel("%s%%" % t)
            self.m_gauge1.SetValue(t)
            if t==100:
               self.Close(True)
        else:  # 否则线程未执行，重新开启
            self.m_staticText2.SetLabel("%s" % t)

class CheckBoxFrame(wx.Frame):  
    def __init__(self,Dirs):  
        wx.Frame.__init__(self, None, -1, '请选择需要打包的模组',   
                size=(400, 600))  
        panel = wx.Panel(self, -1)
        Dir=[]
        for i in Dirs:
            Dir.append(i[0])
        self.a=wx.CheckListBox(panel,-1,(35,40),(300,300),Dir)  
        self.checkboxall = wx.Button(panel, -1, "全选",(100,10),(50,20)) 
        self.uncheckboxall = wx.Button(panel, -1, "全不选",(200,10),(50,20)) 
        self.checkboxall.Bind(wx.EVT_BUTTON, self.choose_all)
        self.uncheckboxall.Bind(wx.EVT_BUTTON, self.no_choose_all)
        b=wx.Button(panel,wx.OK,"OK",(300,350))
        b.Bind(wx.EVT_BUTTON,self.confirm,b)


    def confirm(self,event):
        value = self.a.GetCheckedItems()
        global Count
        Count=str(len(value))
        dlg = wx.MessageDialog(None, u'将要打包'+Count+"个文件", u"是否确认", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.Close(True)
            dlg.Destroy()
            global Value
            Value = self.a.GetCheckedItems()

    def choose_all(self,event):
        self.a.SetCheckedItems(range(0,self.a.GetCount()))  #全选
    def no_choose_all(self,event):
        self.a.SetChecked([])   #全不选

def Getpath(result):
    localmod_path=result
    user_name = getpass.getuser() 
    path='C:\\Users\\' + user_name + '\\Documents\Paradox Interactive\Stellaris\mod\\'
    Dirs=[]
    try:
        dirs = os.listdir( path )
    except IOError:
        dlg = wx.MessageBox('无法自动找到群星mod目录路径，请手动选择文件！',"警告",wx.OK )
        path=Choose_File(a=2)
        dirs = os.listdir(path)
    for filename in dirs:
        File=os.path.splitext(filename)[1]
        if File =='.mod':
            File_path=path+filename
            Read_file=open(File_path,encoding='UTF-8')
            Line=str(Read_file.readlines())
            Read_file.close()
            c=[]
            a=re.findall(r'name="(.*?)"|path="(.*?)"|supported_version="(.*?)"',Line)
            for i in a:
                for j in i:
                    if j:
                        matchobj=re.match(r'【LOCAL】',j)
                        if matchobj:
                            break
                        else:
                            c.append(j)
                if matchobj:
                    break
            if c:
                Dirs.append(c)
    CheckBoxFrame(Dirs).Show()
    app.MainLoop()
    MyForm(None).Show()
    try:
        if  Value:
            Time=time.perf_counter()
            thread_list = []
            for i in Value:
                try:
                    mod_name=Dirs[i][0]  #mod名称
                    savemod_name=re.sub(r'[#$/\\:*?"<>|]+',' ',mod_name)
                    savemod_name_path=path+savemod_name
                    savemod_path=localmod_path+savemod_name+".zip"
                    mod_version=Dirs[i][1] #mod版本
                    try:
                        mod_path=Dirs[i][2]  #mod路径
                    except IndexError:
                        mod_path=Dirs[i][1]
                        mod_version="*"
                except IndexError:
                    log(Dirs[i])
                    pass
                t1=threading.Thread(target=Packing, args=(savemod_path,savemod_name_path,mod_name,mod_path,mod_version,))
                thread_list.append(t1)
            for t in thread_list:
                t.setDaemon(True)
                t.start()
            app.MainLoop()
            dlg = wx.MessageBox('处理完毕!\n用时%d秒'%(time.perf_counter()-Time),"注意",wx.OK )
    except NameError:
        os._exit(-1)

def Packing(savemod_path,savemod_name_path,mod_name,mod_path,mod_version):
        z = zipfile.ZipFile(savemod_path, 'w', zipfile.ZIP_DEFLATED)
        for dirpath,dirmanes,filenames in os.walk(mod_path):
            fpath = dirpath.replace(mod_path,'')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                FiLe=os.path.splitext(filename)[1]
                if FiLe !='.mod':
                    a=os.path.join(dirpath,filename)
                    z.write(a,fpath + filename)
        z.close()
        Create_Modlist(savemod_name_path,mod_name,mod_version,savemod_path)

def Create_Modlist(savemod_name_path,mod_name,mod_version,savemod_path):
    write_file=open(savemod_name_path+'.mod','w',encoding='UTF-8')
    Template='''name="【LOCAL】%s"
    tags={
        "LocalMod"
    }
    supported_version="%s"
    archive="%s"
    '''
    write_file.write(Template % (mod_name,mod_version,savemod_path))
    write_file.close()
    global ack_count
    ack_count=ack_count+1
    wx.CallAfter(pub.sendMessage, "update", msg=ack_count,alL=Count)

def warning(a):
    dlg = wx.MessageBox('请选择文件路径！',"警告",wx.OK )
    if dlg== wx.OK:
        Choose_File(a)

def Confirm_File(localmod_path,a):
    dlg = wx.MessageBox('你选择的路径是：'+localmod_path,"\n是否确认路径?",wx.YES_NO|wx.ICON_QUESTION)
    if dlg== wx.NO:
        Choose_File(a)    

def Choose_File(a):
    if a==1:
        dialog = wx.DirDialog(None, "请选择打包后mod保存路径:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    else:
        dialog = wx.DirDialog(None, "请选择mod目录路径:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        localmod_path=dialog.GetPath().replace('\\', '/')+"/"
        Confirm_File(localmod_path,a)
        return localmod_path
    else:
        warning(a)
    dialog.Destroy()

def log(Dirs):
    write_file=open('Log.txt','a',encoding='UTF-8')
    write_file.write(time.asctime( time.localtime(time.time()))+"   %s\n"%(" | ".join(str(i) for i in Dirs)))
    write_file.close()

def main():
    result=Choose_File(a=1)
    Getpath(result)

if __name__ == "__main__":
    ack_count=0
    app = wx.App()
    main()