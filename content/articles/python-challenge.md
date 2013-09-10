Title: Python Challenge
Date: 2012-08-24 03:33
Tags: python, python-challenge
Slug: python-challenge

[pythonchallenge](http://www.pythonchallenge.com/) 这个网站挺有意思，以后没事做做题。据说闯到18关以上就是高手了^_^。

##第0题

这就很简单了

    :::python
    #!/usr/bin/python

    print 2**38

所以就是http://www.pythonchallenge.com/pc/def/274877906944.html了。

##第一题

看图片可以看出了将每个字母按ascii码的值加上2，翻译一遍。

但是我还不熟悉python嘛，都不知道怎么来取每个字母的ascii码。难道这样就没办法了吗，反正没有性能要求，就先用数组来映射嘛。

    :::python
    #!/usr/bin/python

    a="abcdefghijklmnopqrstuvwxyzab"

    source="""
    g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp.
    bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle.
    sqgle qrpgle.kyicrpylq() gq pcamkkclbcb.
    lmu ynnjw ml rfc spj.
    """

    out=""

    for i in range(0, len(source)):
        p = a.find(source[i])
        if p >= 0:
            out = out + a[p+2]
        else:
            out = out + source[i]

    print out

翻译出来如下

    i hope you didnt translate it by hand.
    thats what computers are for.
    doing it in by hand is inefficient and that's why this text is so long.
    using string.maketrans() is recommended.
    now apply on the url.

照他说的，再把map这三个字母翻译一下，变成ocr。

所以下个地址就是http://www.pythonchallenge.com/pc/def/ocr.html。

##第二题

提示说秘密在页面源码中，打开该页面的源码，找到里面的一串很长的注释，发现里面大多数都是特殊字符，看来得从中找到全部的字母。把注释的内容先保存到文件，再用python一个个过滤。

    :::python
    #!/usr/bin/env python

    import string

    f = open("pc2data")

    for c in f.read():
        if c in string.letters:
            print c,

    f.close()

运行得到输出：

    carl@ThinkPad-T500:~/tmp$ python pc2.py
    e q u a l i t y

所有，下面的页面是http://www.pythonchallenge.com/pc/def/equality.html.

##第三题

提示说要找到所有被3个（只能是3个大写字母包围的小写字母），这当然得是正则表达式的事情了。但苦于我不会用这个re模块，就先死办法弄一个出来吧。先从页面注释里面找到数据，保存到文件。

    :::python
    #!/usr/bin/env python

    import string

    f = open("pc3data")

    status=0
    char='*'
    result=""

    for c in f.read():
        if status < 0:
            if c in string.lowercase:
                status = 0
        elif status

然后运行，看结果

    carl@ThinkPad-T500:~/tmp$ python pc3.py
    linkedlist

这样，下一个页面的地址就是http://www.pythonchallenge.com/pc/def/linkedlist.html
