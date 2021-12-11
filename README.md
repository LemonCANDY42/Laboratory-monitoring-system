# Laboratory-monitoring-system
A monitoring system for the working status of laboratory equipment, which can send the working status of the equipment by email.

Thank you my friend **Lindi Jiao** for your inspiration!


1. https://qengineering.eu/install-64-os-on-raspberry-pi-zero-2.html
1. https://qengineering.eu/install-raspberry-64-os.html
1. [换源](https://blog.csdn.net/qq_41071754/article/details/113731699)
1. 

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