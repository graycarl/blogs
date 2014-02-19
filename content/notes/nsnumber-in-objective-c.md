Title: 关于NSNumber
Date: 2014-02-19 14:05
Tags: ios, objective-c
Slug: nsnumber-in-objective-c

由于半路杀进来，一直对OC对C基本数据类型的封装感到困惑，使用的时候也很心虚。仔细看了一遍官方文档，终于理清了。

这类类型有三个：`NSNumber`、`NSDecimalNumber`、`NSNull`。其中`NSNull`是一个单例，可以直接使用`==`来比较。

下面着重说一下`NSNumber`。

## 结构

`NSNumber`中保存的是实际数据的指针和类型，实际数据可以是各种类型，如(int, float, bool, struct, …)。

把实际数据取出来用

    [nsNumber intValue]

取数据的时候会做默认的类型转换。

## 比较

`NSNumber`中有

    - (BOOL)isEqualToNumber:(NSNumber *)aNumber

该函数使用C中的比较方式来比较大小。

而对于`isEqual`，看代码就知道了：

    -(BOOL)isEqual:other {
       if(self==other)
        return YES;

       if(![other isKindOfClass:objc_lookUpClass("NSNumber")])
        return NO;

       return [self isEqualToNumber:other];
    }
