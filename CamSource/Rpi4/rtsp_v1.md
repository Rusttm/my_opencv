to run rtsp on rpi4
from https://kevinsaye.wordpress.com/2018/10/17/making-a-rtsp-server-out-of-a-raspberry-pi-in-15-minutes-or-less/


3. update the system and install git and cmake

$ apt update && apt install git cmake

4. download the source for v412rtspserver

$ git clone https://github.com/mpromonet/v4l2rtspserver.git

5. make and install the code (~5 minutes)

$ cd v4l2rtspserver && cmake . && make && make install

6. add the following command to your /etc/rc.local

$ v4l2rtspserver /dev/video0 &

7. in VLC, open network stream to:  rtsp://192.168.1.69:8554/unicast

start v4l2rtspserver.service:
$ systemctl start v4l2rtspserver.service
allow firewall:
$ sudo ufw allow 8554
$ sudo ufw allow 8554/udp
