Title: 关于XCTestCase
Date: 2014-02-23 18:12
Tags: iOS, unittest
Slug: about-xctestcase

Xcode自带的测试框架貌似没有给出任何文档，一些问题只能自己测试来确定了。

## `setUp`和`tearDown`在什么时候被执行

经过测试发现，类方法的`setUp`会在本Case第一执行测试方法执行执行一次。而实例方法的`setUp`会在每个测试方法执行的之前执行。`tearDown`也是一样。

    + (void)setUp
    {
        // called once
        [super setUp];
    }

    - (void)setUp
    {
        // called before every test functions
        [super setUp];
    }

## 测试方法的执行顺序

**更新：貌似这是我的错觉，无法控制各个方法的执行顺序**

如果我们想严格控制每个测试方法的执行顺序该怎么办呢？

经过测试发现，测试方法的执行顺序类似于`Python`的单元测试，根据方法名来决定执行顺序。

所以，我们可以这样定义方法名来定义执行顺序

    - (void)test10SomeWord
    {
        // some code
    }

    - (void)test11SomeWord
    {
        // some code
    }

    - (void)test20SomeWord
    {
        //some code
    }

    …..

