### 漏洞信息

2021年1月15日，JumpServer官方发布了安全通告，其中修复了一处远程命令执行漏洞。由于 JumpServer 的某些接口未做授权限制，允许攻击者通过精心构造的请求获取日志文件等敏感信息，并能通过相关操作API执行任意命令。

### 漏洞危害

由于 JumpServer 的某些接口未做授权限制，允许攻击者通过精心构造的请求获取日志文件等敏感信息，并能通过相关操作API执行任意命令。

### 影响范围

```json
JumpServer < v2.6.2
JumpServer < v2.5.4
JumpServer < v2.4.5 
JumpServer = v1.5.9
```

### FOFA资产
[jumpserver站点](http://beta.unionpay.com/)

### 修复方案

JumpServer官方已经发布了解决上述漏洞的安全更新，建议受影响用户尽快升级到安全版本：

**安全版本:** 

```json
JumpServer >= v2.6.2
JumpServer >= v2.5.4
JumpServer >= v2.4.5 
JumpServer = v1.5.9 （版本号没变）
```

官方安全版本下载可以参考以下链接：

[https://github.com/jumpserver/jumpserver/releases/tag/v2.6.2](https://github.com/jumpserver/jumpserver/releases/tag/v2.6.2)

### 参考资料

[https://github.com/jumpserver/jumpserver/blob/master/README.md](https://github.com/jumpserver/jumpserver/blob/master/README.md)