import datetime
import os
from typing import List, Optional

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

class Image(BaseModel):
    url: str
    caption: str = ''

class TelegramMessage(Message):
    to_: str = os.getenv("TG_ADMIN_CHAT_ID")
    disable_web_page_preview: bool = True
    images: Optional[List[ImageUrl]]


class Point(BaseModel):
    lat: float
    long: float

class Location(Point):
    name: str
    address: Optional[str]
    tags: Optional[List[str]]

class InterestLocation(Location):
    website: Optional[str]
    website_domain: Optional[str]
    chain_name: Optional[str]

class RouteSummary(BaseModel):
    walking_distance: int
    total_distance: int
    total_time: int
    public_transport_count: int
    transports: Optional[List[str]]
    from_: Optional[Point]
    to_: Optional[Point]

# ########################################
class Property(BaseModel):
    location: Location
    bedrooms: str = None
    bathrooms: str = None

class Listing(Property):
    monthly_price: float
    url: str
    title: Optional[str]
    publish_date: Optional[datetime.datetime]

class DaftListing(Listing):
    category: str = None
    featured_level: str = None
    sections: List[str]
    source_code: str


class DaftSearchList(BaseModel):
    results_count: int
    search_rules: dict
    result_list: List[DaftListing]

class DaftSearchItem(BaseModel):
    results_count: int
    search_rules: dict
    result_list: List[DaftListing]


class DaftImage(Image):
    url_600: Optional[str]
