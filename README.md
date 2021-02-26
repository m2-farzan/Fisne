# Fisne

**F**isne **i**s a **s**imple **n**etwork **e**mulator.

Fisne starts as a docker container. It implements the following functionalities:

1. Opening `<fisne-ip>:90` in a browser, will show a control panel in which network emulation parameters e.g. latency, jitter, etc. can be set.
2. All other packets sent to `<fisne-ip>` (that is, everything except TCP on port 90), will be forwarded back to `localhost`. So if your application is running on `127.0.0.1:80` you can test its performance with emulated network by calling `<fisne-ip>:80`.
3. Fisne can also route packets that are going to the outside world. You can set `<fisne-ip>` as gateway and call the remote IP. The final effect in this case would be a cumulative result of Fisne emulated effects and real world network effects.

Fisne control panel:

![Example Image](https://raw.githubusercontent.com/m2-farzan/fisne/main/preview.png)

## Features List

- [x] Lightweight GUI
- [x] Latency simulation
  - [x] Fixed Latency
  - [ ] Stationary random jitter with uniform/normal distribution profile
  - [ ] Non-stationary jitter based on experimental data
- [ ] Packet loss simulation
  - [ ] Stationary random packet loss with Poisson probability
  - [ ] Non-stationary packet loss (*bursts*), based on experimental data
- [ ] Packet reordering simulation (As a consequence of jitter)
- [ ] Packet duplication
  - [ ] Packet corruption simulation
- [ ] Bandwidth Limit

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/m2-farzan/fisne
   ```

2. Start Fisne:

   ```
   docker build . -t fisne
   docker run --cap-add=NET_ADMIN fisne
   ```

   Note: The container prints out its IP when it starts. It's going to be something like `172.20.0.5`. Use it for the next steps.

3. Head to Fisne dashboard, located at `http://<fisne-ip>:90/` to see status, setup network emulation parameters, e.g. latency, loss, etc.

4. Ping `<fisne-ip>` and verify that RTT is twice the latency defined in the previous step.

5. If you only want to use Fisne for local applications, no other steps are needed. Just call your application at `<protocol>://<fisne-ip>:<port-number>/`.

6. If you also want to route traffic to outside world via Fisne, just set `<fisne-ip>` as route for the desired IP. In Linux, the following command can be used:

   ```bash
   ip route add <target-ip> via <fisne-ip>
   ```

7. Ping the target IP and verify that RTT has increased about twice the latency defined in Fisne. Obviously RTT is going to be somewhat greater that twice latency due to physical network effects.

## Methods

Fisne internally uses the following tools:

- tc-netem: as network emulation core.
- iptables: to catch TCP over port 90 and bounce everything else back to host.
- flask: for the lightweight GUI.

## Design Philosophy

Make it radically simple. Fact: Many good, complex alternatives already exist out there.

## Afterthought

Here's an extremely simple, yet powerful alternative for Linux users. Note that `tc` is built in, so no installation is needed.

To emulate network effects for localhost:

```
tc qdisc replace dev lo root netem latency 500ms
```

To emulate network effects for remote packets:

```
tc qdisc replace dev <eth0/enp1s0/wlp2s0/...> root netem latency 500ms
```

More info:

```
man tc-netem
```

## Extra: Installing on VirtualBox

You might want to run Fisne over VB, rather than Docker. In that case, follow these steps:

1. Start with a plain Ubuntu (Ubuntu server will be lighter).

2. Go to virtual machine settings and configure network mode to *bridge*.

3. Install these packages:

   ```
   sudo apt-get install iproute2 iputils-ping python3 python3-flask iptables
   ```

4. Clone Fisne into the virtual machine. Switch to virtualbox branch:

   ```
   git clone --branch virtualbox https://github.com/m2-farzan/fisne
   ```

5. Run the GUI:

   ```
   sudo python3 main.py
   ```

   