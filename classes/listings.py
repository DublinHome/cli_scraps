import hashlib
import json
from bs4 import BeautifulSoup
from daftlistings import Daft, SearchType, SortType
import requests
from classes.utils import Utils
from loguru import logger
from model.sqlmodel import DaftListing, Image
import re


class Listings:
    def __init__(self):
        raise NotImplementedError()

    def search(self):
        raise NotImplementedError()
    
    def listing_detail(self):
        raise NotImplementedError()


class DaftListings(Listings):
    def __init__(self):
        self.min_price = 1000
        self.max_price = 2000

    def search(self, min_price:int = None, max_price:int = None):
        if min_price is None:
            min_price = self.min_price
        if max_price is None:
            max_price = self.max_price
        daft = Daft()
        daft.set_location("Dublin City")

        daft.set_search_type(SearchType.RESIDENTIAL_RENT)

        daft.set_min_price(min_price)
        daft.set_max_price(max_price)

        daft.set_sort_type(SortType.PUBLISH_DATE_DESC)
        listings = daft.search()
        result_items = []
        for listing in listings:
            logger.trace(listing)
            d = {
                "url": Utils.get_attr_try(listing, "daft_link"),
                "title": Utils.get_attr_try(listing, "title"),
                "latitude": Utils.get_attr_try(listing, "latitude"),
                "longitude": Utils.get_attr_try(listing, "longitude"),
                "bedrooms": Utils.get_attr_try(listing, "bedrooms"),
                "bathrooms": Utils.get_attr_try(listing, "bathrooms"),
                "publish_date": Utils.get_attr_try(listing, "publish_date"),
                "category": Utils.get_attr_try(listing, "category"),
                "featured_level": Utils.get_attr_try(listing, "featured_level"),
                "sections": Utils.get_attr_try(listing, "sections"),
                "source_code": Utils.get_attr_try(listing, "shortcode"),
                "monthly_price": (
                    Utils.str_to_float(Utils.get_attr_try(listing, "monthly_price"))
                    or -1
                ),
            }
            logger.info(d)

    def listing_detail(self, url):
        response = requests.get(url)

        if(response.status_code == 200):
            html = requests.get(url).text
        else:
            raise ReferenceError('The request didn`t run correctly')

        soup = BeautifulSoup(html, 'html.parser')
        data = json.loads(soup.find(id="__NEXT_DATA__").text)
        pageProps = data['props']['pageProps']
        if "listing" not in pageProps:
            logger.error(f"URL without Listing: {url}")
            return None
        listing = pageProps['listing']
        # print(listing)
        with open(f"./logs/json/{listing.get('id', '')}_raw.json", 'w') as f:
            json.dump(listing, f, indent=2)
            
        result = DaftListing(
            id=listing.get('id', ''),
            title=listing.get('title', ''),
            seo_title=listing.get('seoTitle', ''),
            sections=listing.get('sections', ''),
            featured_level=listing.get('featuredLevel', ''),
            updated_at=Utils.parse_date(listing.get('lastUpdateDate', None)),
            bedrooms=Utils.int_from_str(listing.get('numBedrooms', '0')),
            bathrooms=Utils.int_from_str(listing.get('numBathrooms', '0')),
            property_type=listing.get('propertyType', ''),
            daft_shortcode=listing.get('daftShortcode', ''),


            ber=str(listing.get('ber', '')),
            seo_path=listing.get('seoFriendlyPath', ''),
            category=listing.get('category', ''),
            state=listing.get('state', ''),
            premier_partner=listing.get('premierPartner', ''),
            description=listing.get('description', ''),
            facilities=[x['name'] for x in listing.get('facilities', [])],
            overview=[
                f"{x['label']}: {x['text']}" for x in listing.get('propertyOverview', [])],
            views=Utils.int_from_str(str(pageProps.get('listingViews', '0'))),
        )

        if('media' in listing):
            media = listing['media']
            result.image_count = media.get('totalImages', '')
            result.has_video = media.get('hasVideo', '')
            result.has_virtual_tour = media.get('hasVirtualTour', '')
            result.has_brochure = media.get('hasBrochure', '')

            result.images = []
            for image_block in media.get('images', []):

                url_600 = None
                for key, val in image_block.items():
                    print(key, val)
                    digit_groups = re.findall("\d+", key)
                    if((len(digit_groups) > 0) and (int(re.findall("\d+", key)[0]) <= 600) and val.startswith('http')):
                        url_600 = val
                        break
                result.images.append(
                    Image(
                        url=next(filter(lambda y: y.startswith('http'), image_block.values())),
                        url_600=url_600
                    )
                )

        # Price
        if('nonFormatted' in listing and 'price' in listing['nonFormatted']):
            result.price = listing['nonFormatted']['price']
        elif('dfpTargetingValues' in pageProps and 'price' in listing['nonFormatted']):
            result.price = pageProps['dfpTargetingValues']['price']

        result.hash_version = Utils.md5(f"{result.totalImages}{result.description}{result.price}")


        # with open(f"./logs/json/{listing.get('id', '')}.json", 'w') as f:
        #     json.dump(data, f, indent=2)

        return result