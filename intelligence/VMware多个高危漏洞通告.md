**漏洞信息**

2021年1月24日，国外安全研究人员披露了SonicWall SSL-VPN 历史版本中存在的远程命令执行漏洞。由于SonicWall SSL-VPN历史版本使用了受ShellShock漏洞影响的bash 版本以及HTTP CGI 可执行程序，导致攻击者可以通过插入精心构造的HTTP请求头，造成远程命令执行漏洞，从而控制目标主机，目前该漏洞利用脚本已公开，建议受影响用户尽快升级到安全版本。

**漏洞危害**

由于SonicWall SSL-VPN历史版本使用了受ShellShock漏洞影响的bash 版本以及HTTP CGI 可执行程序，导致攻击者可以通过插入精心构造的HTTP请求头，造成远程命令执行漏洞，从而控制目标主机。

**影响范围**

Sonic SMA < 8.0.0.4

**漏洞复现**
[https://wiki.scn.sap.com/wiki/pages/viewpage.action?pageId=540935305](https://qhgw.gfqh.com.cn/) 


**修复方案**

该漏洞为历史版本漏洞，建议受影响用户尽快升级到安全版本：

- 安全版本: Sonic SMA  ≥ 8.0.0.4

**参考资料**

[https://wiki.scn.sap.com/wiki/pages/viewpage.action?pageId=540935305](https://wiki.scn.sap.com/wiki/pages/viewpage.action?pageId=540935305) 

[https://github.com/chipik/SAP_EEM_CVE-2020-6207/blob/main/README.md](https://github.com/chipik/SAP_EEM_CVE-2020-6207/blob/main/README.md) # exp