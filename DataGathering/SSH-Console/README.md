# SSH-Console

Generates a PCAP file of encrypted SSH traffic on TCP port 22 tagged with UDP labels on port 5006.

## Usage

### Create a new Docker network

```bash
docker network create --subnet 172.19.0.0/16 sidechannel
```

### Build and start RemoteContainer

```bash
cd RemoteContainer
docker build -t ssh-remote .
docker run --rm --name server_container --network sidechannel --ip 172.19.0.2 -it ssh-remote
```

### Build and start ClientContainer

```bash
cd ClientContainer
docker build -t ssh-client .
docker run --rm --name client_container --network sidechannel --ip 172.19.0.3 -it ssh-client
```

### Capturing traffic

On the console to *server_container*, capture traffic from
the **eth0** network interface:

```bash
tcpdump -i eth0 -w ssh_tagged.pcap
```

From the *client_container*, login to the *server_container* over SSH.

```bash
ssh ubuntu@172.19.0.2
```

The login password is **ubuntu**.

After logging in over SSH, start the UDP logging shell.

```bash
python /logging_shell.py
```
