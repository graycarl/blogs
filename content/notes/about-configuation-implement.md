Title: 关于项目配置文件的实现
Date: 2014-01-26 11:00
Tags: config, python
Slug: about-configuation-implement

之前写代码的时候还有一个纠结点就是如何分开项目在**单元测试**、**DEBUG**及**线上环境**的配置文件。尝试了各种方法，考虑了具体运行环境的配置不应该被包含到源码仓库，最终选定了`~/.config`的形式。

## 读取指定路径的配置

    def _get_module_from_file(filename):
        filename = os.path.abspath(filename)
        d = imp.new_module('config')
        d.__file__ = filename
        try:
            with open(filename) as config_file:
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        return d

## 获取`HOME`下文件路径

    import os
    init_config(os.path.expanduser(“~/.config”))
