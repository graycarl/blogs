Title: PythonChallenge[18-19]
Date: 2012-09-06 22:02
Tags: python, python-challenge
Slug: python-challenge-18-19

##第十八题

这题太难，提示都是网上找到的，哎，看来智商的确不够啊。

一开始是两张图片，几乎完全一样，只有亮度不同。标题是**can you tell the diffrence**，源码中有**it is more obvious that you might think**，不同的就是亮度嘛，所以下一步就是访问<http://www.pythonchallenge.com/pc/return/brightness.html>。

    :::html
    ......
        <font color="gold">
        <img src="balloons.jpg" border="0"/>
    <!-- it is more obvious that what you might think -->
    </body>
    </html>

打开还是一样的页面，源码中的注释变了。

    :::html
    ......
        <font color="gold">
        <img src="balloons.jpg" border="0"/>
    <!-- maybe consider deltas.gz -->
    </body>
    </html>

那就在打开<http://www.pythonchallenge.com/pc/return/deltas.gz>，这样得到一个deltas.gz文件。里面的内容比较有规律

<blockquote><pre>
e0 e0 5a 34 0e 5d 40 88 17 27 22 86 e7 88 88 88 88 2f   e0 e0 5a 34 0e 5d 40 88 17 27 22 86 e7 88 88 88 88 2f
00 0d 9d a3 2c 51 25 94 6a 18 00 1e ae e5 66 89 c5 1a   00 0d 9d a3 2c 51 25 94 6a 18 00 1e ae e5 66 89 c5 1a
4b 0f 1f 2f 51 c4 c7 c0 c4 4b 10 11 11 11 f1 01 75 73   4b 0f 1f 2f 51 c4 c7 c0 c4 4b 10 11 11 11 f1 01 75 73
8e 72 42 d3 14 99 82 da 96 3a 49 4a 59 82 14 8c 15 16   8e 72 42 d3 14 99 82 da 96 3a 49 4a 59 82 14 8c 15 16
b1 86 8e 88 e1 39 22 22 22 e2 96 8f 4e 5b 61 50 a0 ca   b1 86 8e 88 e1 39 22 22 22 e2 96 8f 4e 5b 61 50 a0 ca
90 e7 28 0c 2c 00 87 6e 8d 95 86 e9 d0 b6 68 5a 34 f1   90 e7 28 0c 2c 00 87 6e 8d 95 86 e9 d0 b6 68 5a 34 f1
42 45 c4 f0 1c 11 11 11 71 7b 48 91 0d 68 34 c2 24 45   42 45 c4 f0 1c 11 11 11 71 7b 48 91 0d 68 34 c2 24 45
......
</pre></blockquote>

一开始左右两边的数据一样，后来有些行一样，有些行不一行，而这题的主题的diffrence，所以我们可以对这两组内容做diff。

思路是这样的，做出diff结果，把两边一致的数据拉出来写入一个文件，把左边比右边多的数据写入第二个文件，把右边比左边多的数据再写入一个文件。最后会得到三张图片。

    :::python
    #work on python2
    import Image
    import gzip
    import difflib

    data = gzip.GzipFile("deltas.gz").read()

    data = data.splitlines()
    left = []; right = []
    for line in data:
        left.append(line[:53])
        right.append(line[56:])

    diff = difflib.ndiff(left, right)
    left = ""; right = ""; common = ""
    for row in diff:
        d = [chr(int(s, 16)) for s in row[2:].split()]
        if row.startswith(' '):
            common += "".join(d)
        elif row.startswith('+'):
            left += "".join(d)
        elif row.startswith('-'):
            right += "".join(d)

    open("left.png", "w").write(left)
    open("right.png", "w").write(right)
    open("common.png", "w").write(common)

得到的图片的内容分别是**../hex/bin.html**, **butter**, **fly**。

这样，下一关就是<http://www.pythonchallenge.com/pc/hex/bin.html>，用户名butter，密码fly。

##第十九题

打开是一幅地图的图片，标题是**please**，没有其他信息。

html源码里面有一段很长的注释，看内容应该是一封带附件的邮件。

    From: leopold.moz@pythonchallenge.com
    Subject: what do you mean by "open the attachment?"
    Mime-version: 1.0
    Content-type: Multipart/mixed; boundary="===============1295515792=="

    It is so much easier for you, youngsters.
    Maybe my computer is out of order.
    I have a real work to do and I must know what's inside!

    --===============1295515792==
    Content-type: audio/x-wav; name="indian.wav"
    Content-transfer-encoding: base64

    UklGRvyzAQBXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YdizAQBABkAMQAtAAEADQAJA
    BEAEQAJAAkAGQAVABUAEQApAC0AJQAhAD0APQANADUAFQAVAD0AEQA5ADUAGQAlAAj8PQAVABkAE
    ......

下面显然就是要把附件恢复了，看看是什么。

    :::python
    #work on python3

    import email, base64

    mail = email.message_from_file(open("/tmp/tmpmail"))
    sub = mail.get_payload()[0]
    open("/tmp/"+sub.get_filename(), "wb").write(base64.b64decode(sub.get_payload().encode()))

得到一个*indian.wav*文件，但是听了下内容，就一句**Sorry!**。

打开<http://www.pythonchallenge.com/pc/hex/sorry.html>，出现一句话
> what are you apologizing for?

对什么感到抱歉？我对我的智商感到抱歉！好吧，又没有思路了。

......Googleing

说是看到图片颜色被反转了，应该想到把声音文件的字节反转（我是想不到）。

    :::python
    import wave, array
    winput = wave.open("/tmp/indian.wav", "rb")
    woutput = wave.open("/tmp/revert.wav", "wb")

    woutput.setparams(winput.getparams())
    data = array.array('i')
    data.fromstring(winput.readframes(winput.getnframes()))
    data.byteswap()
    woutput.writeframes(data.tostring())

    winput.close(); woutput.close()

最后弄出来*revert.wav*，听一下，**you are the idiot**，居然还是唱出来的。

下一关应该就是<http://www.pythonchallenge.com/pc/hex/idiot.html>了，进去之后又是一张图片，不过已经把下关链接给出来了。
