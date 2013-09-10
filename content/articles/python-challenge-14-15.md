Title: PythonChallenge[14-15]
Date: 2012-09-04 21:37
Tags: python, python-challenge
Slug: python-challenge-14-15

##第十四题

打开页面，一张面包图片，下面是一个类似条形码的小图。

再看下html

    :::html
    <html>
    <head>
      <title>walk around</title>
      <link rel="stylesheet" type="text/css" href="../style.css">
    </head>
    <body>
    <center>
    <img src="italy.jpg"><br>
    <br>

    <!-- remember: 100*100 = (100+99+99+98) + (...  -->

    <img src="wire.png" width="100" height="100">

    </body>
    </html>

那段注释肯定是关键点之一，正好与图片长宽一样。

不管怎样，先把图片弄下来吧。把图片下载下来会发现另一个线索。这张图片居然是细条状的，只是在html被强制设置成100x100。并且细条状的颜色好像是很有规律的重复，好像有点思路了。

嗯，先看看图片的原始大小是什么。

    :::python
    #work on python2
    import Image

    image = Image.open("wire.png", "r")

    print image.size

大小是(10000,1)，果然，我们应该把这张图叠成100x100的。

    :::python
    #work on python2
    import Image

    image = Image.open("wire.png", "r")

    out = Image.new(image.mode, (100,100))

    for i in range(0,10000):
        out.putpixel((i%100,i/100), image.getpixel((i,0)))

    out.show()

运行得到新的图片，显示一个单词**bit**，但是图片的条文还是很乱。应该是有另一种方式来合成图片的。看着螺旋的面包，我又有想法了。把细条盘成一个100x100的矩阵，正好和html中的那段注释符合。

    :::python
    #work on python2
    import Image

    image = Image.open("wire.png", "r")

    out = Image.new(image.mode, (100,100))

    cur_pos = -1
    def get_next():
        global cur_pos
        global image
        cur_pos += 1
        return image.getpixel((cur_pos,0))

    x,y=-1,0
    for size in range(100, 1, -2):
        for i in range(0,size):
            x += 1
            out.putpixel((x,y),get_next())
        for i in range(0,size-1):
            y += 1
            out.putpixel((x,y),get_next())
        for i in range(0,size-1):
            x -= 1
            out.putpixel((x,y),get_next())
        for i in range(0,size-2):
            y -= 1
            out.putpixel((x,y),get_next())

    out.show()

这下对了，出现了一只猫的图片，所以下一关是cat？打开<http://www.pythonchallenge.com/pc/return/cat.html>出现一只猫，上面写着她叫uzi，再打开<http://www.pythonchallenge.com/pc/return/uzi.html>，就是下一关了。

##第15题

打开页面得到一张日历图片，页面标题是whom。看来是猜人了。

把现有线索整理如下：

* 日历图片，年份被遮住了，但可以知道这一年的1月1号是周四，并且是闰年。1月26号被圈住。
* html源码中有两个注释*(he ain't the youngest, he is the second )*和*(todo: buy flowers for tomorrow)*。
* 标题是whom，所以是要找人。

好了，先把被遮住的年份找出来吧。

    :::python
    #work on python3
    import datetime

    for year in range(1006, 2006, 10):
        fday = datetime.date(year, 1, 1)
        if fday.weekday() == 3 and year % 4 == 0:
            print(year)

运行，输出是** 1176 1356 1576 1756 1976 **。

从*(he ain't the youngest, he is the second)*知道，应该是1756。从*(todo: buy flowers for tomorrow)*知道，应该是1月27号这天。

上Google搜索1756-1-27这个日期，知道这是mozart的生日，所以下一关的入口就是mozart，<http://www.pythonchallenge.com/pc/return/mozart.html>。
