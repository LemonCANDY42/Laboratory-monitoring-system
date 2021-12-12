# Laboratory-monitoring-system
A monitoring system for the working status of laboratory equipment, which can send the working status of the equipment by email.

Thank you my friend **Lindi Jiao** for your inspiration!


1. https://qengineering.eu/install-64-os-on-raspberry-pi-zero-2.html
1. https://qengineering.eu/install-raspberry-64-os.html
1. [换源](https://blog.csdn.net/qq_41071754/article/details/113731699)
1. 
bcm2710-rpi-zero-2.dtb and bcm2710-rpi-zero-2-w.dtb



moba-xterm > settings > x11 Settings > "Unix-compatible keyboard" 的复选框不要勾选，然后按照提示会自动重启x server，重新在pycharm运行代码就可以了

https://blog.csdn.net/qxqxqzzz/article/details/104942021

https://blog.csdn.net/qq_43765237/article/details/106032728

https://zhuanlan.zhihu.com/p/51464024

Run vlc streaming on raspberrypi

`raspivid -o - -t 0 -n -w 600 -h 400 -fps 12 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8081/}' :demux=h264`

``` shell
#!/bin/bash
raspivid -o - -t 0 -n -w 600 -h 400 -fps 12 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8081/}' :demux=h264

```

(树莓派走代理)[https://www.cxyzjd.com/article/eininbebop/109139536]
Code:

sudo nano /etc/environment
envirinment内输入：

export http_proxy="http://username:password@proxyipaddress:proxyport"
export https_proxy="http://username:password@proxyipaddress:proxyport"
export no_proxy="localhost, 127.0.0.1"
用代理的IP地址和端口替换proxyipaddress和proxyport。

export http_proxy="http://10.60.190.10:7890"
export https_proxy="http://10.60.190.10:7890"
export no_proxy="localhost, 127.0.0.1"
接下来

sudo visudo
将下面的行添加到文件中，这样sudo将使用您刚刚创建的环境变量:

Defaults env_keep+="http_proxy https_proxy no_proxy"
之后reboot就可以了

代理 https://blog.csdn.net/weixin_41010198/article/details/87929622

遇到  gnutls_handshake() failed: The TLS connection was non-properly terminated.
关闭vpn，然后ssl设置false

Add this to your run command:

-v /etc/hosts:/etc/hosts

fuck https://google-coral.github.io/py-repo/tflite-runtime/