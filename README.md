# zerowall

lightweight firewall

## install

```
$ sudo pip install tornado
$ sudo pip install sqlalchemy
```

## run

run firewall

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

run Web Server for review HTTP logs and config firewall rule

```
$ python server.py
```

## feature

- defined filter rule
    - ip
    - subnet
    - port
    - protocol
    - http content
- record network