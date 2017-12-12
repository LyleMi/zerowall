# zerowall

一款轻量级的防火墙

## 安装

```
$ sudo pip install tornado
$ sudo pip install sqlalchemy
```

## 运行

运行防火墙

```
usage: firewall.py [-h] [--webhost WEBHOST] [--webport WEBPORT]
                   [--srvhost SRVHOST] [--srvport SRVPORT]
                   [--log-level LOG_LEVEL]

Simple Python Application Firewall

optional arguments:
  -h, --help            show this help message and exit
  --webhost WEBHOST     Default: 127.0.0.1
  --webport WEBPORT     Default: 80
  --srvhost SRVHOST     Default: 127.0.0.1
  --srvport SRVPORT     Default: 8083
  --log-level LOG_LEVEL
                        DEBUG, INFO, WARNING, ERROR, CRITICAL
```

运行带查看HTTP日志和配置防火墙规则的Web Server

```
$ python server.py
```
### 功能

- 用户自定义过滤规则
    - ip
    - 子网
    - 端口
    - 协议
    - content
- 记录网络流量