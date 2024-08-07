My RefferalUrl: https://t.me/DejenDogBot?start=6f00f9c7

## Functionality
| Functional                                                     | Supported |
|----------------------------------------------------------------|:---------:|
| Multithreading                                                 |     ✅     |
| Binding a proxy to a session                                   |     ✅     |
| Auto get all tasks except telegram tasks                       |     ✅     |
| Retry request per claim                                        |     ✅     |
| Support tdata / pyrogram .session / telethon .session          |     ✅     |

## [Settings](https://github.com/JustPandaEver/DejendogBot/blob/main/.env-example)
| Setting                   | Description                                                                   |
|---------------------------|-------------------------------------------------------------------------------|
| **API_ID / API_HASH**     | Platform data from which to launch a Telegram session (stock - Android)       |
| **USE_PROXY_FROM_FILE**   | Whether to use proxy from the `bot/config/proxies.txt` file (True / False)    |

## Installation
You can download the [**Repository**](https://github.com/justpandaever/DejendogBot) by cloning it to your system and installing the necessary dependencies:
```shell
~ >>> git clone https://github.com/justpandaever/DejendogBot.git
~ >>> cd DejendogBot

# If you are using Telethon sessions, then clone the "converter" branch
~ >>> git clone https://github.com/justpandaever/DejendogBot.git -b converter
~ >>> cd DejendogBot

#Linux
~/DejendogBot >>> python3 -m venv venv
~/DejendogBot >>> source venv/bin/activate
~/DejendogBot >>> pip3 install -r requirements.txt
~/DejendogBot >>> cp .env-example .env
~/DejendogBot >>> nano .env # Here you must specify your API_ID and API_HASH, the rest is taken by default
~/DejendogBot >>> python3 main.py

#Windows
~/DejendogBot >>> python -m venv venv
~/DejendogBot >>> venv\Scripts\activate
~/DejendogBot >>> pip install -r requirements.txt
~/DejendogBot >>> copy .env-example .env
~/DejendogBot >>> # Specify your API_ID and API_HASH, the rest is taken by default
~/DejendogBot >>> python main.py
```

Also, for a quick launch, you can use arguments, for example:
```shell
~/DejendogBot >>> python3 main.py --action (1/2)
# Or
~/DejendogBot >>> python3 main.py -a (1/2)

#1 - Create session
#2 - Run clicker
```
