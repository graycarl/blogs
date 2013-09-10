Title: Bash持续积累
Date: 2012-08-24 03:25
Tags: bash, shell
Slug: bash-notes

##条件判断

**语法**,可以用`[ -e /tmp/tf1 ]`或者`test -e /tmp/tf1`。

###文件类型判断

    -e    判断文件是否存在
    -f    判断该文件是否存在且是一个文件(file)
    -d    判断该文件是否存在且是一个目录(directory)
    -b    判断该文件是否存在且是块设备
    -c    判断该文件是否存在且是字符设备
    -S    判断该文件是否存在且是一个Socket
    -p    判断该文件是否存在且是一个管道文件(pipe)
    -L    判断该文件是否存在且是一个软链接

###文件权限判断

    -r    判断该文件是否存在且具有可读权限
    -w    判断该文件是否存在且具有可写权限
    -x    判断该文件是否存在且具有可执行权限

###文件比较，例如`test file1 -nt file2`。

    -nt   判断file1是否比file2新
    -ot   判断file1是否比file2旧
    -ef   判断file1和file2是否为同一文件（用在判断hard link时）

###数值比较，只能用于整数。例如`test n1 -eq n2`。

    -eq   判断n1是否等于n2
    -ne   判断n1是否不等于n2
    -gt   判断n1是否大于n2
    -lt   判断n1是否小于n2
    -ge   判断n1是否大于等于n2
    -le   判断n1是否小于等于n2

###字符串判断

    test -z string    判断string为空
    test -n string    判断string不为空
    test str1 = str2  判断str1等于str2
    test str1 != str2 判断str1不等于str2

###逻辑运算

    -o    逻辑或，例如 test -e file1 -o -e file2
    -a    逻辑与，例如 test -e file1 -a -e file2
    !     逻辑非，例如 test ! -e file1

##find

基本用法，就是找某个名称的文件了。

    find . -name '*.[ch]'

注意，这个name后面不是正则（以前一直以为这里是按正则来匹配的，所有总觉得用起来完全不对啊）。按man手册的说法，这里匹配的是"shell patter±？）。

    find . -name '*.[ch]' | xargs -i mv {} {}.bak

这里用了-i这个参数，后面就可以用{}来代表每次xargs传过来的一个内容了。也就是说mv被调用了n次（n=找到的文件数）。

再有时候，我们希望xargs每次传两个参数给后面的命令来处理？没问题。

    find . -name '*.[ch]' | xargs -n 2 diff

这样也行啊。不过，这样diff出来的东西是个啥？:)

Carl-MBPR:blogsite carl$ sqlite3 database/blogs.db 'select content from blogs where id=7;' > /tmp/b
Carl-MBPR:blogsite carl$ sqlite3 database/blogs.db 'select content from blogs where id=6;' |tee /tmp/b
##条件判断

**语法**,可以用`[ -e /tmp/tf1 ]`或者`test -e /tmp/tf1`。

###文件类型判断

    -e    判断文件是否存在
    -f    判断该文件是否存在且是一个文件(file)
    -d    判断该文件是否存在且是一个目录(directory)
    -b    判断该文件是否存在且是块设备
    -c    判断该文件是否存在且是字符设备
    -S    判断该文件是否存在且是一个Socket
    -p    判断该文件是否存在且是一个管道文件(pipe)
    -L    判断该文件是否存在且是一个软链接

###文件权限判断

    -r    判断该文件是否存在且具有可读权限
    -w    判断该文件是否存在且具有可写权限
    -x    判断该文件是否存在且具有可执行权限

###文件比较，例如`test file1 -nt file2`。

    -nt   判断file1是否比file2新
    -ot   判断file1是否比file2旧
    -ef   判断file1和file2是否为同一文件（用在判断hard link时）

###数值比较，只能用于整数。例如`test n1 -eq n2`。

    -eq   判断n1是否等于n2
    -ne   判断n1是否不等于n2
    -gt   判断n1是否大于n2
    -lt   判断n1是否小于n2
    -ge   判断n1是否大于等于n2
    -le   判断n1是否小于等于n2

###字符串判断

    test -z string    判断string为空
    test -n string    判断string不为空
    test str1 = str2  判断str1等于str2
    test str1 != str2 判断str1不等于str2

###逻辑运算

    -o    逻辑或，例如 test -e file1 -o -e file2
    -a    逻辑与，例如 test -e file1 -a -e file2
    !     逻辑非，例如 test ! -e file1

##find

基本用法，就是找某个名称的文件了。

    find . -name '*.[ch]'

注意，这个name后面不是正则（以前一直以为这里是按正则来匹配的，所有总觉得用起来完全不对啊）。按man手册的说法，这里匹配的是"shell pattern"。

进阶一点，就是找满足各种条件的文件了。

    find . -type d 找directory
                 f 找plain file
                 l 找symbolic link
                 p 找named pipe file
                 b 找block device
                 c 找char device
    find . -perm 755
    find . -user carl

PS. 如果经常要在全局按文件名来找文件的话，强烈建议用`updatedb+locate`，`find / ...`实在太慢了。这两个命令在各个发行版下面对应的包可能都不同吧，自己找找好了。

##xargs

处理批量作业时候最常用也是最好用的东西啊，大爱。

基本用法，就是把其标准输入的内容转变成它随后的命令的参数。

    find . -name '*.[ch]' | xargs wc -l

这么一个简单的一行命令就可以统计该目录下所有c程序源码总行数了。

进阶一点，有时候，我们希望前面find找到的文件需要一个个的来处理。比如，对前面找到的所有c源码文件的文件名加个bak后缀（怎么会有这么诡异的需求？）。

    find . -name '*.[ch]' | xargs -i mv {} {}.bak

这里用了-i这个参数，后面就可以用{}来代表每次xargs传过来的一个内容了。也就是说mv被调用了n次（n=找到的文件数）。

再有时候，我们希望xargs每次传两个参数给后面的命令来处理？没问题。

    find . -name '*.[ch]' | xargs -n 2 diff

这样也行啊。不过，这样diff出来的东西是个啥？:)
