Title: PythonChallenge[4-5]
Date: 2012-09-03 01:39
Tags: python, python-challenge
Slug: python-challenge-4-5

##第四题

打开上一题的地址后，出来了提示让我们把地址改成<http://www.pythonchallenge.com/pc/def/linkedlist.php>。

再开地址后，出现一张图片。点击图片，跳到地址<http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=12345>。内容为
> and the next nothing is 44827

再进连接<http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=44827>，内容为

> and the next nothing is 45439

看来我们是要找到这个规律了。

先把这些数字按顺序列出来

> 12345
> 44827
> 45439
> 94485
> 72198
> 80992
> 8880
> 40961

靠，看来是没有规律的，只能用程序自动往下走了。

    :::python
    #work in python3
    from urllib.request import urlopen

    baseurl = r"http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing="
    next = "12345"

    while(next):
        print("open: " + baseurl + next)
        with urlopen(baseurl+next) as pf:
            str = pf.read().decode()
            print("get: " + str)
            if str.startswith("and the next nothing is"):
                next = str.split()[-1]
                print("next: "+next)
            else:
                print("End")
                break

把程序跑起来，然后就等着吧。

> ......
> open: http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=75635
> get: and the next nothing is 52899
> next: 52899
> open: http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=52899
> get: and the next nothing is 66831
> next: 66831
> open: http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=66831
> get: peak.html
> End

好了，找到下一关入口了<http://www.pythonchallenge.com/pc/def/peak.html>。

##第五题

一座叫peak hell的山，html里面有这么一段

    <peakhell src="banner.p"> </peakhell>

再访问<http://www.pythonchallenge.com/pc/def/banner.p>得到一个文件。打开后里面实在是看不懂。

> (lp0
> (lp1
> (S' '
> p2
> I95
> tp3
> aa(lp4
> (g2
> I14
> tp5
> a(S'#'
> p6
> ...

没法办法了，做个弊吧。上网找到线索，原来peak hell是想指的是python的pickle模块，我们需要用这个模块反序列化这个文件内容，再打印出来

    :::python
    # work on python3
    import pickle

    with open("banner.p", "rb") as file:
        pick = pickle.loads(file.read())
        print(pick)

得到如下玩意
<blockquote>
[(' ', 95)]<br/>
[(' ', 14), ('#', 5), (' ', 70), ('#', 5), (' ', 1)]<br/>
[(' ', 15), ('#', 4), (' ', 71), ('#', 4), (' ', 1)]<br/>
[(' ', 15), ('#', 4), (' ', 71), ('#', 4), (' ', 1)]<br/>
[(' ', 15), ('#', 4), (' ', 71), ('#', 4), (' ', 1)]<br/>
[(' ', 15), ('#', 4), (' ', 71), ('#', 4), (' ', 1)]<br/>
[(' ', 15), ('#', 4), (' ', 71), ('#', 4), (' ', 1)]<br/>
[(' ', 15), ('#', 4), (' ', 71), ('#', 4), (' ', 1)]<br/>
[(' ', 15), ('#', 4), (' ', 71), ('#', 4), (' ', 1)]<br/>
......
</blockquote>

好像知道要干什么了，它是想用"#"拼出来什么东西吧，那就继续

    :::python
    #work in python3
    import pickle

    with open("banner.p", "rb") as file:
        pick = pickle.loads(file.read())
        for row in pick:
            for (char, num) in row:
                print(char*num, end="")
            print("")

执行结果，相当帅气

<blockquote>
<pre>

              #####                                                                      #####
               ####                                                                       ####
               ####                                                                       ####
               ####                                                                       ####
               ####                                                                       ####
               ####                                                                       ####
               ####                                                                       ####
               ####                                                                       ####
      ###      ####   ###         ###       #####   ###    #####   ###          ###       ####
   ###   ##    #### #######     ##  ###      #### #######   #### #######     ###  ###     ####
  ###     ###  #####    ####   ###   ####    #####    ####  #####    ####   ###     ###   ####
 ###           ####     ####   ###    ###    ####     ####  ####     ####  ###      ####  ####
 ###           ####     ####          ###    ####     ####  ####     ####  ###       ###  ####
####           ####     ####     ##   ###    ####     ####  ####     #### ####       ###  ####
####           ####     ####   ##########    ####     ####  ####     #### ##############  ####
####           ####     ####  ###    ####    ####     ####  ####     #### ####            ####
####           ####     #### ####     ###    ####     ####  ####     #### ####            ####
 ###           ####     #### ####     ###    ####     ####  ####     ####  ###            ####
  ###      ##  ####     ####  ###    ####    ####     ####  ####     ####   ###      ##   ####
   ###    ##   ####     ####   ###########   ####     ####  ####     ####    ###    ##    ####
      ###     ######    #####    ##    #### ######    ###########    #####      ###      ######
</pre>
</blockquote>

好了，这个应该就是入口了<http://www.pythonchallenge.com/pc/def/channel.html>。
