# ipapy
iOS项目自动打包脚本


1.脚本自动打包

2.上传到fir.im

3.发送邮件给测试人员



###需要安装的相关指令软件:

1.python 2.7

2.xcode

3.fir.im指令



###使用方法:

1.安装xcode

2.安装fir.im的指令,安装方法见 https://github.com/FIRHQ/fir-cli/blob/master/README.md

3.配置相关信息 python ipa.py -c 或者 python ipa.py --config

targetName:工程的名称,如：我的工程是BossZP.xcodeproj,所以我的targetName就是BossZP

gitPath:工程的git地址,如：我的git地址是http://git.xxx.org/xxxxxx/xxxxxx.git

certificateName:证书名称,如：我的是iPhone Developer: YANG YU (7XC3UZCAZM)

firToken:在fir.im上创建应用后的token,如：我的是2ac8uf3j9z3ur98d7gxxxxxxxx

下面的是邮件设置:

emailFromUser:我的邮箱,如：xxxxxx@163.com

emailToUser:测试人员的邮箱，如 xxxxxx@163.com

emailPassword:我的邮箱的密码

emailHost:邮箱的host，可以去邮箱网页查看,如：我的是smtp.163.com

keychainPassword:(选填)远程SSH连接打包的话需要设置这个参数，内容为你电脑的密码

4.配置完信息，可以通过 --help 或者 -h 查看基本的使用方法

-h, --help            查看帮助信息

-c, --config          配置基本信息

-s, --showTags        显示git上所有的版本

-t TAG, --tag=TAG     设置打包时的版本

● 如果你不喜欢我把放在Documents下面，你可以把脚本的第28行改成你喜欢的目录，如:target_path = "/Users/yuyang/clone/BossZP"

###你可以这样使用:

python ipa.py -h

python ipa.py --help

python ipa.py -c

python ipa.py --config

python ipa.py -s

python ipa.py --showTags

python ipa.py -t v3.0 (打包时候这样使用，后面的v3.0参数可以使用python ipa.py -s获取)

python ipa.py -tag v3.0 (打包时候这样使用，后面的v3.0参数可以使用python ipa.py -s获取)

python ipa.py (tag不写，默认是master)

***

2016.03.04更新：

> 修改远程SSH连接打包失败的问题，添加设置参数keychainPassword
(选填)远程SSH连接打包的话需要设置这个参数，内容为你电脑的密码







