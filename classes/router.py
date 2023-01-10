import json
import os
from typing import List
from urllib import parse

import here_public_transit_api
from here_public_transit_api.rest import ApiException
from herepy import PlacesApi
from loguru import logger

from model.sqlmodel import InterestLocation, Location, Point, RouteSummary


class Router:
    @staticmethod
    def point_to_str(point: Point) -> str:
        return f"{point.lat},{point.long}"

    @staticmethod
    def str_to_point(str: str) -> Point:
        parts = str.split(",")
        lat = float(parts[0].strip())
        long = float(parts[1].strip())
        return Point(lat=lat, long=long)

    def __init__(self) -> None:
        here_config = here_public_transit_api.Configuration()
        here_config.api_key["apiKey"] = os.environ["HERE_API_KEY"]

        self.routing_api = here_public_transit_api.RoutingApi(
            here_public_transit_api.ApiClient(here_config)
        )

        self.places_api = PlacesApi(api_key=os.environ["HERE_API_KEY"])

    def get_address(self, point: Point) -> str:
        raise NotImplementedError

    def get_address_information(self, point: Point) -> str:
        raise NotImplementedError

    def get_point(self, address: str) -> Point:
        raise NotImplementedError

    def get_nearby_interest(
        self, point: Point, query: str, country_code: str = "IRL"
    ) -> List[InterestLocation]:

        def get_website_domain(place):
            if "contacts" not in place:
                return None, None
            for contact in place["contacts"]:
                if "www" in contact:
                    for www in contact["www"]:
                        if "value" in www:
                            website = www["value"].lower()
                            domain = parse.urlsplit(website).netloc.lstrip('www.')
                            return website, domain
            return None, None

        def get_chain(place):
            for chain in place.get("chains", []):
                if "name" in chain:
                    return chain["name"]
            return None


        response = self.places_api.search_in_country(
            coordinates=[point.lat, point.long], query=query, country_code=country_code
        )
        places = response.as_dict()
        ret_ = []
        if "items" not in places:
            raise ReferenceError("There is no `items` in the response")

        for place in places["items"]:
            place_instance = InterestLocation(
                lat=place["position"]["lat"],
                long=place["position"]["lng"],
                name=place["title"].title(),
                address=place["address"]["label"],
                distance=place["distance"],
                chain_name=get_chain(place),
            )

            place_instance.website, place_instance.website_domain = get_website_domain(place)

            ret_.append(place_instance)
        return ret_

    def get_routes(self, point_a, point_b) -> RouteSummary:
        def _route_parser(route_details: dict) -> RouteSummary:
            logger.trace(json.dumps(route_details))
            route = RouteSummary(
                walking_distance=0,
                public_transport_count=0,
                total_distance=0,
                total_time=0,
                from_=point_a,
                to_=point_b,
                transports=[],
            )

            for section in route_details["sections"]:

                travel_summary = section.get("travelSummary", {})
                travel_transport = section.get("transport", {})

                distance = int(travel_summary.get("length", 0))
                time = int(travel_summary.get("length", 0))

                route.total_distance = route.total_distance + distance / 1000
                route.total_time = route.total_time + time / 60

                transport_mode = travel_transport.get("mode", "N/A")
                transport_short_name = travel_transport.get("shortName", "")
                transport = f"{transport_mode.capitalize()} ({transport_short_name})"

                if section.get("type", "") == "pedestrian":
                    route.walking_distance = route.walking_distance + distance
                elif section.get("type", "") == "transit":
                    route.public_transport_count = route.public_transport_count + 1
                    route.transports.append(transport)
            return route

        try:
            point_a = Router.point_to_str(point_a)
            point_b = Router.point_to_str(point_b)
            api_response = self.routing_api.get_routes(
                origin=point_a,
                destination=point_b,
                alternatives=5,
                pedestrian_max_distance=2000,  # meters
                pedestrian_speed=1,  # m/s
                _return=[
                    "travelSummary",
                ],
            )
        except ApiException as e:
            logger.warning("Exception when calling RoutingApi->get_routes: %s\n" % e)
        response_dict = api_response.to_dict()

        return [_route_parser(x) for x in response_dict.get("routes", [])]
