import os
from typing import List, Optional
import datetime

from pydantic import BaseModel


# class TelegramImageUrl(BaseModel):
#     url: str
#     caption: str = ''


# class TelegramMessage(BaseModel):
#     message: str
#     chat_id: str = os.getenv('TG_ADMIN_CHAT_ID')
#     timeout: int = 10
#     
#     images: Optional[List[TelegramImageUrl]]

class Message(BaseModel):
    title: str
    body: str
    from_: Optional[str]
    to_: str
    method: str

class ImageUrl(BaseModel):
    url: str
    caption: str = ''

class TelegramMessage(Message):
    to_: str = os.getenv("TG_ADMIN_CHAT_ID")
    disable_web_page_preview: bool = True
    images: Optional[List[ImageUrl]]