# PingBot

A simple Telegram bot to ping a server over ICMP or TCP protocol.

[![Docker Image CI](https://github.com/chitang233/PingBot/actions/workflows/docker-ci.yaml/badge.svg)](https://github.com/chitang233/PingBot/actions/workflows/docker-ci.yaml)

## Installation

### Docker

First, clone the repo

```shell
git clone https://github.com/chitang233/PingBot
cd PingBot
```

After [configuration](#configuration), run it:

```shell
docker compose up -d
```

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

Edit `config.py`

- `API_TOKEN` - Your Telegram Bot token.(Get it from [@BotFather](https://t.me/BotFather))
- `PROXY_URL` - Optional. Your proxy URL. Support HTTP and SOCKS5. *e.g. `http://host:port`, `socks5://host:port`*
- `SHOW_PUBLIC_IP` - Show your machine's public IP address and country in `/start` command if set to `True`. Default is `False`.

## Commands

```
help - Show help message
icmp - Ping a server over ICMP protocol
tcp - Ping a server over TCP protocol, port required
```
