Title: PythonChallenge[16-17]
Date: 2012-09-05 01:37
Tags: python, python-challenge
Slug: python-challenge-16-17

##第十六题

打开页面还是图片，里面有一些杂乱的原色。可以注意到，几乎像素的每一行都有一个紫色短线。

页面的标题是*let me get this straight*，把它弄直？

    :::python
    #work on python2
    import Image

    image = Image.open("mozart.gif", "r")
    new = Image.new(image.mode, image.size)

    size = image.size
    print image.mode


    data = []
    for y in range(size[1]):
        old = -1; start = 0; count = 0
        for x in range(size[0]):
            pixel = image.getpixel((x,y))
            if pixel == old:
                count += 1
            else:
                start = x
                count = 1
            old = pixel
            if count == 4: #find the short line
                for i in range(0,size[0]):
                    if i+start >= size[0]:
                        data.append(image.getpixel((i+start-size[0],y)))
                    else:
                        data.append(image.getpixel((i+start,y)))
                break

    new.putdata(data)
    new.show()

代码有点丑，但是能work，最后会出来一张图片，上面有个单词*romance*，应该就是下一关入口了吧，<http://www.pythonchallenge.com/pc/return/romance.html>。

##第十七题

这题实在有点太复杂了，只能上网找到思路。

列出提示

1. 图中是一块饼干，名称为Cookies。
2. 大图左下角有个小图，为第四题中的图片。

说明是和Cookies有关了，还和第四题有关。继续

1. 打开第四页页面，查看Cookies，看到这么一条
    > info: you should have followed busynothing...
2. 把第四题的解决方法中的nothing改成busynothing，即<http://www.pythonchallenge.com/pc/def/linkedlist.php?busynothing=12345>，返现该cookie编程了'B'。
3. 继续往下Cookie依次是'BZh...'

看来这段Cookie应该是会拼接成一个bz的压缩流了。得把它弄出来。

    :::python
    #work on python3
    from urllib.request import urlopen
    from urllib.parse import unquote_plus
    import bz2

    baseurl = r"http://www.pythonchallenge.com/pc/def/linkedlist.php?busynothing="
    next = "12345"

    data = []
    while(next):
        print("open: " + baseurl + next)
        with urlopen(baseurl+next) as pf:
            str = pf.read().decode()
            ck = pf.info().get("Set-Cookie").split(";")[0].split("=")[1]
            print("get: " + ck); data.append(ck)
            if "and the next busynothing is" in str:
                next = str.split()[-1]
                print("next: "+next)
            else:
                print("End")
                break

    # have got all the cookie
    # python3 using 'utf-8' as default encoding, so we have to specify
    str = "".join(data)
    cookie = unquote_plus(str, encoding='iso-8859-1')

    print(bz2.decompress(cookie.encode('iso-8859-1')))

这段代码用Python3写真是纠结啊，编码问题费了我好长时间。最后运行结果如下
> b'is it the 26th already? call his father and inform him that "the flowers are on their way". he\'ll understand.'

居然还得绕，要找mozart的爸爸的电话，好吧，应该是之前的那题中用到的电话薄了。

    :::python
    #work on python3
    from xmlrpc import client

    server = client.Server("http://www.pythonchallenge.com/pc/phonebook.php")
    print(server.phone("Leopold"))

好了，最终得到'555-VIOLIN'，尝试<http://www.pythonchallenge.com/pc/return/violin.html>，提示修改下地址，那就是<http://www.pythonchallenge.com/pc/stuff/violin.php>了。

结果打开后居然还是没到下一关，老爸的图片出来了，标题是*It's me. what do you want?*, 看来得把信息给他，就是那句*the flowers are on their way*。

尝试用*../violin.php?inform=xxx*的方式，怎么试都没有效果，还是得求助Google，发现是要用Cookie来传信息（我怎么这么笨）。

    :::python
    #work on python3
    from urllib.request import build_opener
    from urllib.parse import quote_plus

    url = r"http://www.pythonchallenge.com/pc/stuff/violin.php"
    msg = "the flowers are on their way"

    opener = build_opener()
    opener.addheaders.append(("Cookie", "info="+quote_plus(msg, encoding='iso-8859-1')))

    req = opener.open(url)

    print(req.read())

好了，最终输入的html包含了leopold的一句话
> oh well, don’t you dare to forget the balloons

Balloons，应该就是下一关了吧，<http://www.pythonchallenge.com/pc/return/balloons.html>。
