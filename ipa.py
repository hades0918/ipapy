# -*- coding: utf-8 -*-

#使用需要首先安装fir.im的指令支持
#需要安装pyobjc
#需要设置相关参数

import os
import sys
import Foundation
import objc
import AppKit
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import date, time, datetime, timedelta

#工程名
targetName = "BossZP"
#临时文件夹名称
m = hashlib.md5()
m.update(targetName)
tempFinder = m.hexdigest()
#git地址
gitPath = "http://xxxxxxxxxxxxxxxxxxxxx/mobile_ios.git"
#checkout后的本地路径
target_path = "/Users/yuyang/Documents"
#主路径
mainPath = target_path + '/' + tempFinder
#证书名
certificateName = "iPhone Developer: MAOSHENG YANG (xxxxxxxx)"
#firToken
firToken = "xxxxxxxxxxxxxxxxxxxxxxxxxxx"
#邮件参数
emailFromUser="xxxxxxxxxxxx@163.com"
emailToUser="xxxxxxxxxx@kanzhun.com"
emailPassword="xxxxxxxxxxxxxxx"
emailHost="smtp.163.com"
#钥匙链相关
keychainPath="~/Library/Keychains/login.keychain"
keychainPassworld=""

#删除文件夹
def rmoveFinder():
    os.system("rm -r -f %s"%mainPath)
    return
    
#创建文件夹
def createFinder():
    os.system("mkdir %s"%mainPath)
    return
    
#对文件夹授权
def allowFinder():
    os.system("chmod -R 777 %s"%mainPath)
    return
    
#查找文件
def scan_files(directory,postfix):
  files_list=[]
  for root, sub_dirs, files in os.walk(directory):
    for special_file in sub_dirs:
        if special_file.endswith(postfix):
            files_list.append(os.path.join(root,special_file))    
  return files_list
  
#判断文件夹是否存在
def isFinderExists():
    return os.path.exists(mainPath)

#clone工程
def gitClone():
    os.system ('git clone %s %s'%(gitPath,mainPath))
    return
    
#pull工程
def gitPull():
    os.system("cd %s;git reset --hard;git pull"%mainPath)
    return
   
#设置版本 
def setGitVersion(version):
    if len(version)>0:
        os.system("cd %s;git reset --hard;git checkout %s"%(mainPath,version))
    return
    
#回到主版本
def setGitVersionMaster():
    setGitVersion("master")
    return
 
#clean工程   
def cleanPro():
    os.system('cd %s;xcodebuild -target %s clean'%(mainPath,targetName))
    return

#清理pbxproj文件
def clearPbxproj():
    global all_the_text
    path = "%s/%s.xcodeproj/project.pbxproj"%(mainPath,targetName)
    file_object = open(path)
    try:
        all_the_text=file_object.readlines()
        for text in all_the_text:
            if 'PROVISIONING_PROFILE' in text:
                all_the_text.remove(text)
    finally:
        file_object.close()
       
    file_object = open(path,'w')
    try:
        for text in all_the_text:
            file_object.write(text)
    finally:
        file_object.close()
    return

def allowKeychain():
    # User interaction is not allowed
    os.system("security unlock-keychain -p '%s' %s"%(keychainPassworld,keychainPath))
    return

#编译获取.app文件和dsym
def buildApp():
    files_list=scan_files(mainPath,postfix=".xcodeproj")
    temp = -1
    for k in range(len(files_list)):
        if files_list[k] == mainPath + "/" + targetName + ".xcodeproj":
            temp = k
    if temp >= 0:
        files_list.pop(temp)
    for target in files_list:
        target=target.replace(".xcodeproj","")
        tmpList=target.split('/')
        name=tmpList[len(tmpList)-1]
        path=target.replace(name,"")
        path=path[0:len(path)-1]
        os.system("cd %s;xcodebuild -target %s CODE_SIGN_IDENTITY='%s'"%(path,name,certificateName))
    os.system("cd %s;xcodebuild -target %s CODE_SIGN_IDENTITY='%s'"%(mainPath,targetName,certificateName))
    return
    
#创建ipa
def cerateIPA():
    os.system ("cd %s;rm -r -f %s.ipa"%(mainPath,targetName))
    os.system ("cd %s;xcrun -sdk iphoneos PackageApplication -v %s/build/Release-iphoneos/%s.app -o %s/%s.ipa CODE_SIGN_IDENTITY='%s'"%(mainPath,mainPath,targetName,mainPath,targetName,certificateName))
    return
    
#上传
def uploadToFir():
    if os.path.exists("%s/%s.ipa"%(mainPath,targetName)):
        os.system("fir p '%s/%s.ipa' -T '%s'"%(mainPath,targetName,firToken))
    else:
        print "没有找到ipa文件"
    return
        
#发邮件给测试不带附件
def sendEmail():
    if not os.path.exists("%s/%s.ipa"%(mainPath,targetName)):
        print "没有找到ipa文件"
        return
    msg = MIMEText('地址:http://fir.im/xxxx 密码:xxxx','text','utf-8')
    msg['to'] = emailToUser
    msg['from'] = emailFromUser
    msg['subject'] = '地址:http://fir.im/xxxx 密码:xxxx'
    try:
        server = smtplib.SMTP()
        server.connect(emailHost)
        server.login(emailFromUser,emailPassword)
        server.sendmail(msg['from'], msg['to'],msg.as_string())
        server.quit()
        print '发送成功'
    except Exception, e:  
        print str(e)
    return
    
#发邮件给测试带附件
def sendEmailWithAtt():
    #创建一个带附件的实例
    msg = MIMEMultipart()
    filePath="%s/%s.ipa"%(mainPath,targetName)
    att1 = MIMEText(open(filePath, 'rb').read(), 'base64', 'gb2312')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="%s.ipa"'%targetName
    msg.attach(att1)
    msg['to'] = emailToUser
    msg['from'] = emailFromUser
    msg['subject'] = '地址:http://fir.im/xxxx 密码:xxxx'
    try:
        server = smtplib.SMTP()
        server.connect(emailHost)
        server.login(emailFromUser,emailPassword)
        server.sendmail(msg['from'], msg['to'],msg.as_string())
        server.quit()
        print '发送成功'
    except Exception, e:  
        print str(e)
        sendEmail()
    return
    
#发通知给你的mac
def notify(self, title, subtitle, text, url):
    NSUserNotification = objc.lookUpClass('NSUserNotification')
    NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(str(title))
    notification.setSubtitle_(str(subtitle))
    notification.setInformativeText_(str(text))
    notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setHasActionButton_(True)
    notification.setOtherButtonTitle_("View")
    notification.setUserInfo_({"action":"open_url", "value":url})
    NSUserNotificationCenter.defaultUserNotificationCenter().setDelegate_(self)
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
    
#定时任务
def runTask(func, day=0, hour=0, min=0, second=0):
  # Init time
  now = datetime.now()
  strnow = now.strftime('%Y-%m-%d %H:%M:%S')
  print "now:",strnow
  # First next run time
  period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
  next_time = now + period
  strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
  print "next run:",strnext_time
  while True:
      # Get system current time
      iter_now = datetime.now()
      iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
      if str(iter_now_time) == str(strnext_time):
          # Get every start work time
          print "start work: %s" % iter_now_time
          # Call task func
          func()
          print "task done."
          # Get next iteration time
          iter_time = iter_now + period
          strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
          print "next_iter: %s" % strnext_time
          # Continue next iteration
          continue

#获取设置线上线下参数
def getPara():
    isOnline = 0
    if __name__=="__main__":   
        if len(sys.argv)>1: 
            if int(sys.argv[1]) == 1:
                isOnline = 1
    path = "%s/%s/Supports/Constants.h"%(mainPath,targetName)
    file_object = open(path)
    try:
        all_the_text=file_object.read()
        """      
        if '//#define DEBUG_FILE  1' in all_the_text:
            all_the_text=all_the_text.replace("//#define DEBUG_FILE  1", "#define DEBUG_FILE  1")
        if '#define DEBUG_TESTSERVER' in all_the_text and isOnline:
            all_the_text=all_the_text.replace("#define DEBUG_TESTSERVER", "//#define DEBUG_TESTSERVER")
        if '//#define DEBUG_TESTSERVER' in all_the_text and not isOnline:
            all_the_text=all_the_text.replace("//#define DEBUG_TESTSERVER", "#define DEBUG_TESTSERVER")
        if 'wx9e569a13d211567d' in all_the_text and not isOnline:
            all_the_text=all_the_text.replace("xxxxxxxxxx", "xxxxxxxxxx")
        """
                
    finally:
        file_object.close()
       
    file_object = open(path,'w')
    try:
        file_object.write(all_the_text)
    finally:
        file_object.close()
    return
    
def setVersion():
    if __name__=="__main__":   
        if len(sys.argv)>2: 
            if len(str(sys.argv[2]))>0:
                setGitVersion(str(sys.argv[2]))
        else:
            setGitVersionMaster()
    return

def start():
    #获取最新代码
    if not isFinderExists():
        createFinder()
        gitClone()
    else:
        gitPull()
    #设置版本
    setVersion()
    #设置文件夹权限
    allowFinder()
    allowKeychain()
    #clear pbxproj文件
    clearPbxproj()
    #获取参数
    getPara()
    #clean工程
    cleanPro()
    #编译
    buildApp()
    #生成ipa文件
    cerateIPA()
    #上传到fir.im
    uploadToFir()
    #发邮件给测试
    sendEmail()
    return
   
def main():
    start()
    runTask(start, day=0, hour=6, min=0,second=0)
    return
    
#程序开始
start()