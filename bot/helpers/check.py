import os
import json
import re
from typing import Callable, TypeVar
from discord.ext import commands
from bot.exceptions import errors
from bot.helpers import db_helper
from better_profanity import profanity

T = TypeVar("T")


def is_user_owner() -> Callable[[T], T]:
    def predicate(context: commands.Context) -> bool:
        with open("config.json") as file:
            data = json.load(file)
        if context.author.id != int(data["owner_id"]):
            raise errors.UserNotOwner
        return True

    return commands.check(predicate)


def not_blacklisted() -> Callable[[T], T]:
    def predicate(context: commands.Context) -> bool:
        if db_helper.is_prohibited(context.author.id):
            raise errors.UserBlacklisted
        return True
    return commands.check(predicate)


def is_valid_uuid(uuid: str, context: commands.Context) -> bool:
    pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    if not re.match(pattern, uuid) or profanity.contains_profanity(uuid):
        return False
    return True
