Title: Goagent在MacOS上的自动启动的实现
Date: 2013-09-11 09:53
Tags: macos, goagent, daemon
Slug: how-macos-launch-the-daemon-on-startup

# Goagent在MacOS上的自启动的实现

主要是想知道MacOS上面的开机自启动的程序是如何实现的。

Goagent提供了一个Python脚本来添加自启动的配置，脚本如下

    import sys
    import os
    import re
    import time

    def main_macos():
        if os.getuid() != 0:
            print 'please use sudo run this script'
            sys.exit()
        PLIST = '''\
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>GroupName</key>
        <string>wheel</string>
        <key>Label</key>
        <string>org.goagent.macos</string>
        <key>OnDemand</key>
        <false/>
        <key>ProgramArguments</key>
        <array>
            <string>/usr/bin/python</string>
            <string>%(dirname)s/proxy.py</string>
        </array>
        <key>RunAtLoad</key>
        <true/>
        <key>ServiceIPC</key>
        <true/>
        <key>StandardErrorPath</key>
        <string>%(dirname)s/proxy.log</string>
       ychain Failed!'
            sys.exit(0)
        print 'Adding CA.crt to system keychain Done'

    def main():
        main_macos()


    if __name__ == '__main__':
       try:
           main()
       except KeyboardInterrupt:
           pass
}}}

可以看出来，这个脚本做了两件事，添加自启动配置和添加CA证书。证书那个就先不关心了，就看下自启动都做了什么。

其实就将一段xml配置写进了`/System/Library/LaunchDaemons/org.goagent.macos.plist`文件里面了，其他啥也没有。

下面再看下这个文件的内容都有些啥。
{{{ lang=xml >
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>GroupName</key> <!-- 以下的配置都是按照key-value的顺序排列的，比如当前这个的key就是GroupName, 表示以什么Group身份运行该程序 -->
        <string>wheel</string>
        <key>Label</key> <!-- Label表示各个自启动程序的唯一标示 -->
        <string>org.goagent.macos</string>
        <key>OnDemand</key>
        <false/>
        <key>ProgramArguments</key> <!-- 启动参数 -->
        <array>
            <string>/usr/bin/python</string>
            <string>%(dirname)s/proxy.py</string>
        </array>
        <key>RunAtLoad</key> <!-- 开机启动-->
        <true/>
        <key>ServiceIPC</key>
        <true/>
        <key>UserName</key> <!-- 以root来运行 -->
        <string>root</string>
        <key>WorkingDirectory</key> <!-- 工作目录 -->
        <string>%(dirname)s</string>
        <key>StandardOutPath</key> <!-- 重定向标准输出 --> 
        <string>/var/log/goagent.log</string>
        <key>StandardErrorPath</key> <!-- 重定向标准错误 --> 
        <string>/var/log/goagent.log</string>
    </dict>
    </plist>

现在服务已经可以在开机时候自动启动了。再参考一下官方文档，发现可以有一个命令来配合使用。

    停止服务
    sudo launchctl unload $plist_filename
    启动服务
    sudo launchctl load $plist_filename

其他详细的配置介绍可以参见[官方文档][http://developer.apple.com/library/mac/#documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html].
