from dotenv import load_dotenv

load_dotenv()

import os
import pprint

import click
from loguru import logger

from classes.messenger import TelegramMessenger
from classes.router import Router
from model.sqlmodel import ImageUrl, TelegramMessage

pp = pprint.PrettyPrinter(indent=4)

@click.group()
def cli():
    pass

@cli.command()
@logger.catch(reraise=True)
def dummy():
    """run the command that I'm (the develoepr) working on :)"""
    logger.info("Dummy dummy work!")

    p1 = Router.str_to_point("53.34545621516955,-6.231801040391591") #Indeed
    p2 = Router.str_to_point("53.34347027177946,-6.276045630904159") #BankHouse
    
    r = Router()
    places = r.get_nearby_interest(p2, "market")
    logger.info(pprint.pformat(places, indent=4))
    logger.info("Get out of here!")


@logger.catch(reraise=True)
@cli.command()
def here_route_to_home():
    logger.info("Dummy dummy work!")

    p1 = Router.str_to_point("53.34545621516955,-6.231801040391591") #Indeed
    p2 = Router.str_to_point("53.34347027177946,-6.276045630904159") #BankHouse
    
    r = Router()
    routes = r.get_routes(p1, p2)
    logger.info(pprint.pformat(routes, indent=4))
    logger.info("Get out of here!")


@logger.catch(reraise=True)
@cli.command()
def tg_send_dummy():
    """run the command that I'm (the develoepr) working on :)"""

    images = [
        ImageUrl(url="https://thumbs.dreamstime.com/z/dog-golden-retriever-jumping-autumn-leaves-autumnal-sunlight-77861618.jpg"),
        ImageUrl(url="https://thumbs.dreamstime.com/z/happy-family-two-children-running-dog-together-happy-family-two-children-running-dog-together-autumn-119764842.jpg"),
        ImageUrl(url="https://thumbs.dreamstime.com/z/cat-dog-near-christmas-tree-pets-under-red-blanket-home-friends-133328305.jpg"),
    ]
    dummy_message = TelegramMessage(
        title="title", body="<b>bold</b> body", method="telegram", # to_=os.getenv("TG_ADMIN_CHAT_ID"),
        images=images
    )

    logger.info("hello world!")
    tm = TelegramMessenger()
    tm.send_message(dummy_message)
    logger.info("Get out of here!")


# @cli.command()
# def cmd1():
#     """Command on cli1"""
# @cli.command()
# def cmd2():
#     """Command on cli1"""

# @click.group()
# def cli2():
#     pass

# @cli2.command()
# def cmd_cli2():
#     """Command on cli2"""

cli = click.CommandCollection(sources=[cli])

if __name__ == "__main__":
    cli()
