import asyncio
import os

import telegram
from loguru import logger
from telegram.constants import ParseMode

from model.sqlmodel import TelegramMessage


class Messenger:
    def __init__(self,) -> None:
        pass
    
    def send_message() -> None:
        raise NotImplementedError()

class TelegramMessenger(Messenger):
    def __init__(self,) -> None:
        self.bot = telegram.Bot(token=os.getenv('TG_BOT_TOKEN'))
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def send_message(self, message: TelegramMessage) -> bool:
        ret_ = []
        logger.info(f"to:{message.to_}")
        main_msg = self.loop.run_until_complete(self.bot.send_message(
            chat_id=message.to_,
            text=message.body,
            parse_mode=telegram.constants.ParseMode.HTML,
            # timeout=message.timeout,
            disable_web_page_preview=message.disable_web_page_preview,
        ))
        # ret_.append(main_msg.to_dict())
        if(message.images):
            media_array = []
            

            for image in message.images:
                media_array.append(telegram.InputMediaPhoto(
                    image.url,
                    caption=image.caption
                ))

            media_array_split = [media_array[i:i + 10]
                                for i in range(0, len(media_array), 10)]

            for small_array in media_array_split:
                # media_msg = asyncio.run(self.bot.send_media_group(
                #     reply_to_message_id=main_msg['message_id'],
                #     chat_id=message.to_,
                #     media=small_array,
                # ))
                media_msg = self.loop.run_until_complete(self.bot.send_media_group(
                    reply_to_message_id=main_msg['message_id'],
                    chat_id=message.to_,
                    media=small_array,
                ))

                # ret_.append([x.to_dict() for x in media_msg])

        return ret_
        