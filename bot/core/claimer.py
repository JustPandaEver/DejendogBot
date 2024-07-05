import asyncio, random
from time import time
from datetime import datetime
from urllib.parse import unquote

import aiohttp
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered
from pyrogram.raw.functions.messages import RequestWebView

from bot.config import settings
from bot.utils import logger
from bot.exceptions import InvalidSession
from .headers import headers


class Claimer:
    def __init__(self, tg_client: Client):
        self.session_name = tg_client.name
        self.tg_client = tg_client

    async def get_tg_web_data(self, proxy: str | None) -> str:
        if proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            if not self.tg_client.is_connected:
                try:
                    await self.tg_client.connect()
                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)

            web_view = await self.tg_client.invoke(RequestWebView(
                peer=await self.tg_client.resolve_peer('DejenDogBot'),
                bot=await self.tg_client.resolve_peer('DejenDogBot'),
                platform='android',
                from_bot_menu=True,
                url='https://api.djdog.io/'
            ))

            auth_url = web_view.url

            tg_web_data = unquote(
                string=auth_url.replace('#tgWebAppData=', 'telegram/login?')).replace("&tgWebAppVersion=6.7&tgWebAppPlatform=android&tgWebAppSideMenuUnavail=1", "")
            #print(tg_web_data)
            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return tg_web_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error during Authorization: {error}")
            await asyncio.sleep(delay=3)

    async def login(self, http_client: aiohttp.ClientSession, tg_web_data) -> dict[str]:
        try:
            responses = await http_client.get(url=tg_web_data)
            responses.raise_for_status()
            responses_json = await responses.json()
            return responses_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Access Token: {error}")
            await asyncio.sleep(delay=3)

    async def levels(self, http_client: aiohttp.ClientSession) -> dict[str]:
        try:
            responses = await http_client.get('https://api.djdog.io/pet/information')
            responses.raise_for_status()
            response = await http_client.get('https://api.djdog.io/pet/barAmount')
            response.raise_for_status()
            response_json = await response.json()
            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when getting Level Data: {error}")
            await asyncio.sleep(delay=3)

    async def claim(self, http_client: aiohttp.ClientSession, click: str) -> str:
        try:
            response = await http_client.post(url="https://api.djdog.io/pet/collect?clicks="+click)
            response.raise_for_status()
            response_json = await response.json()
            return response_json

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while claim task: {error}")
            await asyncio.sleep(delay=3)


    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy) -> None:
        try:
            response = await http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
            ip = (await response.json()).get('origin')
            logger.info(f"{self.session_name} | Proxy IP: {ip}")
        except Exception as error:
            logger.error(f"{self.session_name} | Proxy: {proxy} | Error: {error}")

    async def run(self, proxy: str | None) -> None:
        access_token_created_time = 0
        available = False

        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        async with aiohttp.ClientSession(headers=headers, connector=proxy_conn) as http_client:
            if proxy:
                await self.check_proxy(http_client=http_client, proxy=proxy)

            while True:
                try:
                        tg_web_data = await self.get_tg_web_data(proxy=proxy)
                        login_data = await self.login(http_client=http_client, tg_web_data=tg_web_data)
                        http_client.headers["Authorization"] = f"{login_data['data']['accessToken']}"
                        headers["Authorization"] = f"{login_data['data']['accessToken']}"
                        levels_data = await self.levels(http_client=http_client)
                        logger.info(f"{self.session_name} | Level: {levels_data['data']['level']}")
                        logger.info(f"{self.session_name} | Balance: {levels_data['data']['goldAmount']} Point")
                        clicknum = int(levels_data['data']['availableAmount']/levels_data['data']['level'])
                        logger.info(f"{self.session_name} | Remaining Click: {clicknum}")
                        if(clicknum < 1):
                            logger.info(f"{self.session_name} | No More click")
                            retry = random.randint(200, 400)
                            logger.info(f"{self.session_name} | Sleep {retry} Seconds")
                            await asyncio.sleep(delay=retry)
                        else:
                            claiming = await self.claim(http_client=http_client, click=str(clicknum))
                            logger.info(f"{self.session_name} | Claiming: {claiming['data']['amount']} Point")
                            retry = random.randint(200, 400)
                            logger.info(f"{self.session_name} | Sleep {retry} Seconds")
                            await asyncio.sleep(delay=retry)
                except InvalidSession as error:
                    raise error

                except Exception as error:
                    logger.error(f"{self.session_name} | Unknown error: {error}")
                    await asyncio.sleep(delay=3)


async def run_claimer(tg_client: Client, proxy: str | None):
    try:
        await Claimer(tg_client=tg_client).run(proxy=proxy)
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")
