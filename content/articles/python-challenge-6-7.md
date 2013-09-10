Title: PythonChallenge[6-7]
Date: 2012-09-03 02:32
Tags: python, python-challenge
Slug: python-challenge-6-7

##第六题

打开<http://www.pythonchallenge.com/pc/def/channel.html>看到的又是一幅图片，还是得看看html源码

    :::html
    <html> <!-- <-- zip -->
    <head>
      <title>now there are pairs</title>
      <link rel="stylesheet" type="text/css" href="../style.css">
    </head>
    <body>
    <center>
    <img src="channel.jpg">
    <br/>
    ......

嗯，好像没啥特殊的，除了这个"zip"。好吧，又被难住了，上网找下线索，说是把网址改成zip结尾的。

得到一个zip文件，打开看看，有个readme

> welcome to my zipped list.
>
> hint1: start from 90052
> hint2: answer is inside the zip

在看下其他文件，知道了原来是和第四题一个思路，这次是想考下zipfile模块的用法，那好吧

    :::python
    #work on python3
    import zipfile

    z = zipfile.ZipFile("channel.zip", "r")

    next = "90052"
    head = "Next nothing is"

    while next:
        print("open: " + next + ".txt")
        str = z.read(next+".txt").decode()
        print("got: " + str)
        if str.startswith(head):
            next = str.split()[-1]
            print("next: " + next)
        else:
            break

    print("END"

执行后，输出如下
<blockquote><pre>
open: 45100.txt
got: Next nothing is 68628
next: 68628
open: 68628.txt
got: Next nothing is 67824
next: 67824
open: 67824.txt
got: Next nothing is 46145
next: 46145
open: 46145.txt
got: Collect the comments.
END
</pre></blockquote>

看来还不行，让我们看看zip文件的comments。试了一下发现该zip文件的z.comment为空。难道是里面文件的comments？

    :::python
    #work on python3
    import zipfile

    z = zipfile.ZipFile("channel.zip", "r")

    next = "90052"
    head = "Next nothing is"
    comments = []

    while next:
        print("open: " + next + ".txt")
        str = z.read(next+".txt").decode()
        print("got: " + str)
        comments.append(z.getinfo(next+".txt").comment.decode())
        if str.startswith(head):
            next = str.split()[-1]
            print("next: " + next)
        else:
            break

    print("END")

    print("ok let's print the comments")
    print("".join(comments))

好了，现在可以看见结果了

<blockquote><pre>
open: 46145.txt
got: Collect the comments.
END
ok let's print the comments
****************************************************************
****************************************************************
**                                                            **
**   OO    OO    XX      YYYY    GG    GG  EEEEEE NN      NN  **
**   OO    OO  XXXXXX   YYYYYY   GG   GG   EEEEEE  NN    NN   **
**   OO    OO XXX  XXX YYY   YY  GG GG     EE       NN  NN    **
**   OOOOOOOO XX    XX YY        GGG       EEEEE     NNNN     **
**   OOOOOOOO XX    XX YY        GGG       EEEEE      NN      **
**   OO    OO XXX  XXX YYY   YY  GG GG     EE         NN      **
**   OO    OO  XXXXXX   YYYYYY   GG   GG   EEEEEE     NN      **
**   OO    OO    XX      YYYY    GG    GG  EEEEEE     NN      **
**                                                            **
****************************************************************
 **************************************************************
</pre></blockquote>

下一关的地址应该就是<http://www.pythonchallenge.com/pc/def/hockey.html>了。

但是进去之后显示一句
>it's in the air. look at the letters.
然后又是啥线索也没有了。

在上网查下，原来下一关是oxygen（上附图中的小字），太变态了，怎能猜得着？？

这样，地址就变成了<http://www.pythonchallenge.com/pc/def/oxygen.html>了。

##第七题

打开<http://www.pythonchallenge.com/pc/def/oxygen.html>后就得到一幅图像，html中也没有更多信息。图片中间有一层灰度变化的线，估计把灰度提取出来就是线索了吧。

    :::python
    #work on python2
    import Image

    image = Image.open("oxygen.png", "r")

    width, height = image.size
    ss = []

    mid = int(height/2)
    # 这里7是灰色方格宽度
    for i in range(0,width,7):
        curc = image.getpixel((i,mid))
        if curc[0] == curc[1] and curc[1] == curc[2]:
            ss.append(chr(curc[0]))

    print "".join(ss)

运行输出

> smart guy, you made it. the next level is [105, 110, 116, 101, 103, 114, 105, 116, 121]

再把这个数组转成char

    :::python
    >>> ll = [105, 110, 116, 101, 103, 114, 105, 116, 121]
    >>> print "".join([chr(num) for num in ll])
    integrity

所以，下一关就是<http://www.pythonchallenge.com/pc/def/integrity.html>了。
