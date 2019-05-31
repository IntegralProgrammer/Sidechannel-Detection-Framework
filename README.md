# Sidechannel-Detection-Framework

Source code and examples from my MASc thesis **A Monitoring Framework For Side-Channel Information Leaks**.

## Running

To run the examples presented in the thesis and any of your own examples, first build the *data analysis* Docker container.

```bash
cd DataAnalysis
docker build -t sidechannel-analysis .
```

Then start the container.

```bash
docker run --rm -p 127.0.0.1:8000:8000 -it sidechannel-analysis
```

### Detecting Command Typed Over SSH

From within the running Docker container:

```bash
cd examples/ssh_bash_commands
python main.py
cd /www
python -m SimpleHTTPServer
```

Visit **http://127.0.0.1:8000/** to see the generated side-channel detection report.

### Detecting Webpage Loaded Over SSH

From within the running Docker container:

```bash
cd examples/https_web_browsing
python main.py
cd /www
python -m SimpleHTTPServer
```

Visit **http://127.0.0.1:8000/** to see the generated side-channel detection report.

### Detecting Key Typed Over SSH Protected VNC Session

From within the running Docker container:

```bash
cd examples/vnc_over_ssh
python main.py
cd /www
python -m SimpleHTTPServer
```

Visit **http://127.0.0.1:8000/** to see the generated side-channel detection report.

### Detecting Amount Of Correct Leading Symbols In Authentication String

From within the running Docker container:

```bash
cd examples/password_cpu_timing
python main.py
cd /www
python -m SimpleHTTPServer
```

Visit **http://127.0.0.1:8000/passcode_entropy.png** to see the generated side-channel detection report.

