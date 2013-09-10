Title: PythonChallenge[12-13]
Date: 2012-09-03 20:16
Tags: python, python-challenge
Slug: python-challenge-12-13

##第十二题

打开页面，又是图片，上面一个人正在发扑克牌，没有啥其他信息了。

以为又是图片处理，但是看了半天图片，也没有找到什么线索，只好又依靠Google了。

在html中看见图片的名称为evil1.jpg，那么是不是还有evil2.jpg呢？打开<http://www.pythonchallenge.com/pc/return/evil2.jpg>，果然又是一张图片，上面说不是jpg，是gfx。在打开<http://www.pythonchallenge.com/pc/return/evil2.gfx>得到evil2.gfx文件。

关于这个文件的用法，是根据那张扑克牌的图片得来的，扑克牌正在被分发成5组，这个文件也应该分发成5个文件。（能想到吗，反正我是想不到)

    :::python
    # work on python3
    f = open("/tmp/evil2.gfx", "rb")

    data = f.read()

    for i in range(0,5):
        file = open("/tmp/out%d.jpg"%i, "wb")
        file.write(data[i::5])
        file.close()

这样得到5张图片，打开有是5组字母
> dis pro port ional ity

其中最后一组字母被划去，所以结果就是disproportional，即<http://www.pythonchallenge.com/pc/return/disproportional.html>。
##第十三题

这题我是在没辙了，只能完全依靠Google了。

几个关键点
1. 上一关中给出了evil的名字<http://www.pythonchallenge.com/pc/return/evil4.jpg>
2. 本关页面中是一个电话，标题是call him，图片下写着phone that evil，显然就是让我们打电话给bert。
3. 点击电话，出现一个xml的出错页面，地址是<http://www.pythonchallenge.com/pc/phonebook.php>。

    由这个页面应该能看出来这是一个xmlrpc服务，对于我这种没听过这种服务的人现在是没办法了。

    :::xml
    <?xml version="1.0"?>
    <methodResponse>
    <fault>
    <value>
    <struct><member><name>faultCode</name>
    <value><int>105</int></value>
    </member>
    <member>
    <name>faultString</name>
    <value><string>XML error: Invalid document end at line 1, column 1</string></value>
    </member>
    </struct>
    </value>
    </fault>
    </methodResponse>


现在思路清楚了，就是用这个xmlrpc服务查到bert的电话号码，这应该就是下一关的入口了。

    :::python
    #work on python3
    from xmlrpc import client

    server = client.Server("http://www.pythonchallenge.com/pc/phonebook.php")
    print(server.phone("Bert"))

运行，得到结果**555-ITALY**，对555和ITALY分别尝试，ITALY的页面告诉我们要用小写。所以，下一关就是<http://www.pythonchallenge.com/pc/return/italy.html>。
