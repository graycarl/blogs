Title: PythonChallenge[10-11]
Date: 2012-09-03 17:55
Tags: python, python-challenge
Slug: python-challenge-10-11

##第十题

打开页面是一张图片，下面给出问题
> len(a[30]) = ?

点击图片出现如下内容
> a = [1, 11, 21, 1211, 111221,

就是找规律了。本来以为不能，结果耗了好长时间也没发现规律。只能又是依靠google了。

规律就是，队列中的每个元素都是对前一个元素的描述
> 1
> 11 表示前一个元素是1个1
> 21 表示前一个元素的2个1
> 1211 表示前一个元素是1个2和1个1
> ......

好了，*找到*规律就可以写代码了。

    :::python
    # work on python3
    def descrip(a):
        des = []
        curchar,curcount = a[0],0
        for c in a:
            if c == curchar:
                curcount += 1
            else:
                des.append((curchar,curcount))
                curchar,curcount = c,1
        else:
            des.append((curchar,curcount))
        des = ["%d%s"%(count,char) for (char,count) in des]
        return "".join(des)

    a = "1"
    for i in range(1,31):
        a = descrip(a)

    print("len(a[30]) = %d" % len(a))

执行，输出为5808，所以下一个就是<http://www.pythonchallenge.com/pc/return/5808.html>了。

##第十一题

打开页面，又是图片，没有其他信息，只有标题写着*odd even*，奇数偶数的意思。在看看图片，相邻像素总是不合拍，好像是两张图片重合到一块的。

看来这又是图像处理了，把重合的图片分隔开。

    :::python
    #work on python2
    import Image

    image = Image.open("cave.jpg", "r")

    size = image.size

    image1 = Image.new(image.mode, (size[0]/2,size[1]/2))
    image2 = Image.new(image.mode, (size[0]/2,size[1]/2))

    for x in range(0,size[0]/2):
        for y in range(0,size[1]/2):
            image1.putpixel((x,y),image.getpixel((x*2,y*2)))

    for x in range(0,size[0]/2):
        for y in range(0,size[1]/2):
            image2.putpixel((x,y),image.getpixel((x*2+1,y*2)))

    image1.show()
    image2.show()

执行完产生两张图片，一张和原始图片差不多，一张里面出现了单词evil，看来这就是下一关入口了<http://www.pythonchallenge.com/pc/return/evil.html>。
