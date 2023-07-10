# PingBot

A simple Telegram bot to ping a server over ICMP or TCP protocol.

[![Docker Image CI](https://github.com/chitang233/PingBot/actions/workflows/docker-ci.yaml/badge.svg)](https://github.com/chitang233/PingBot/actions/workflows/docker-ci.yaml)

## Installation

### Docker

```shell
docker run -d \
  -e API_TOKEN= \
  -e PROXY_URL= \
  -e SHOW_PUBLIC_IP=1 \
  -e ALICLOUD_APPCODE= \
  --name pingbot \
  chitang233/pingbot
```

To learn about the environment variables, see [Configuration](#configuration).

### Local

First, you need to install these packages in your system:

- Python 3.6+
- Python pip

Then, clone the repo and install the requirements:

```shell
git clone https://github.com/chitang233/PingBot
cd PingBot
pip install -r requirements.txt
```

After [configuration](#configuration), run it:

```shell
python main.py
```

## Configuration

Edit `.env`

- `API_TOKEN` - Your Telegram Bot token.(Get it from [@BotFather](https://t.me/BotFather))
- `PROXY_URL` - Optional. Your proxy URL. Support HTTP and SOCKS5. *e.g. `http://host:port`, `socks5://host:port`*
- `ALICLOUD_APPCODE` - Optional. Your AlibabaCloud AppCode.
- `SHOW_PUBLIC_IP` - Show your machine's public IP address and country in `/start` command if set to `1`.

## Commands

```
help - Show help message
icmp - Ping a server over ICMP protocol
tcp - Ping a server over TCP protocol, port required
trace - Show the route to a server
dns - Resolve a domain name
whois - Get whois information of a domain
ip - Get IP address of a domain
ip_alicloud - Get IP information using AlibabaCloud API
```
