# Firefox-Traffic-Tagging

Adds UDP packets (destination port 5005) marking the beginnings and endings of web page loads.

## Usage

### Build and start the container

```bash
docker build -t docker-firefox .
docker run --rm -p 127.0.0.1:5900:5900 -it docker-firefox
```

### Connecting

Open a VNC client and connect to **127.0.0.1:5900**. The password is **123456**

### Installing the addon

From within the VNC session, point Firefox to **about:debugging**. Click
**Load Temporary Add-on** and select the file `/Addon/manifest.json`.

### Capturing data

Capture data by running the command `tcpdump -i eth0 -w packets.pcap 'dst port not 5900 and src port not 5900`
*inside* the Docker container. UDP packets with a destination of **5005**
denote the beginnings and ending of web page loads.
