from dotenv import load_dotenv

load_dotenv()

import click
import os
from loguru import logger
from model.sqlmodel import TelegramMessage, ImageUrl
from classes.messenger import TelegramMessenger


@click.group()
def cli():
    pass

images = [
    ImageUrl(url="https://www.educationcorner.com/images/featured-improve-test-taking.jpg"),
    ImageUrl(url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Test-Logo.svg/783px-Test-Logo.svg.png"),
    ImageUrl(url="https://resources.finalsite.net/images/f_auto,q_auto,t_image_size_3/v1645721429/rdaleorg/qblyqgwortzxvb3q4wct/testing.jpg"),
]
dummy_message = TelegramMessage(
    title="title", body="<b>bold</b> body", method="telegram", # to_=os.getenv("TG_ADMIN_CHAT_ID"),
    images=images
)


@logger.catch(reraise=True)
@cli.command()
def dummy():
    """run the command that I'm (the develoepr) working on :)"""
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
