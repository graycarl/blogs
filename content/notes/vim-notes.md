Title: Vim Notes
Date: 2012-08-24 03:39
Tags: vim
Slug: vim-notes

##vimrc_example

在编写自己的~/.vimrc的时候，发现vim包自带的`vimrc_example.vim`文件里面已经帮我写好了很多常用配置。所以，第一步，就是将这个example包含到我们自己的vimrc中来。

    source $VIMRUNTIME/vimrc_example.vim

##Tab及缩进宽度

vim默认的8个字符宽度实在看不习惯，改成4个字符的。

    set tabstop=4
    set softtabstop=4
    set shiftwidth=4

##关于配色

刚开始用vim的时候，在它自带的几种配色方案里面挑来挑去，最后选了`evening`，感觉还不错。

    colo evening

后来无意中发现了`molokai`，觉得虽然颜色艳了点，整体还是挺好看的。于是就决定暂时用它了。

在[http://www.vim.org/scripts/script.php?script_id=2340](http://www.vim.org/scripts/script.php?script_id=2340)下载molokai.vim，放在~/.vim/colors里面，然后修改~/.vimrc。

    set t_Co=256
    colo molokai

##关于备份文件

vim新手应该都碰到过，在我们使用vim编辑代码的时候，经常会在代码目录发现很多类似 xxx.c~ 的文件。这个文件其实是vim的备份文件，保存的是对应文件修改之前的内容（让你有一次后悔的机会）。虽然作用是好的，但是它总是会把本来干净的代码目录搞得一团糟，特别是又使用了某些代码版本管理工具的时候。

其实我们只需要改变一下这些文件的生成目录就可以了

    " 如果有~/tmp目录则文件生成在改目录，否则文件生成在/tmp目录
    set backupdir=~/tmp,/tmp

##vim中查单词

有时候我们很希望在vim中看代码的时候，遇到一个不认识的英语单词可以直接一个快捷键给出翻译结果。很实用的功能，也很简单就能实现。

###安装sdcv

首先需要安装sdcv(stardict-console-version)这个包，可以提供stardict的命令行版本。在终端里面运行包管理器安装sdcv这个包，这里以ubuntu为例

    sudo apt-get install sdcv

什么？你的软件源里面找不到sdcv？自己编译一个呗，看[这里](http://sdcv.sourceforge.net)。

安装完了是不能直接使用的，因为没有字典文件。在sdcv的man手册里面看到，需要将字典文件放在`/usr/share/stardict/dic`中。字典文件在可以在[这里](http://irising.me/2011/07/9021/)找到。

字典文件弄好了之后就可以在shell中使用`sdcv`命令来查单词了。

    carl@carl-VirtualBox:~$ sdcv hello
    Found 1 items, similar to hello.
    -->朗道英汉字典5.0
    -->hello

    *[hә'lәu]
    interj. 喂, 嘿

###绑定到vim中

我们的目的是想在vim中可以直接查单词，所以就需要将sdcv绑定到vim中。

vim中有一个可以设定的配置叫`keyworkprg`，默认是和man命令绑定。即在vim的普通模式下按`shift+k`就可以在man中查找光标所在单词对应的man手册。现在我们在~/.vimrc中添加如下行。

    set keywordprg=sdcv

这样我们就将sdcv绑定到shift+k这个快捷键上了。将光标移动到某一单词上，按`shift+k`，看看效果吧^_^

##全局搜索

想在vim中搜索当前目录及子目录的内容，使用vimgrep命令(可:help vimgrep 查看帮助)。

###基本使用

    :vimgrep /<关键词>/j **/*.[ch]

`**/*.[ch]`是表示搜索当前目录下任意深度的子目录中以c/h为后缀的文件。

执行`:cope`查看结果。

###映射快捷键

手动输入上面的命令太麻烦了，可将其绑定到快捷键。.vimrc中添加

    nmap <F10> yiw:vimgrep /<C-r>0/j **/*.[ch] <CR>:cope<CR>
    vmap <F10> y:vimgrep /<C-r>0/j **/*.[ch] <CR>:cope<CR>

然后在normal模式或者visual模式下就可以直接按F10搜索光标下的单词了。
