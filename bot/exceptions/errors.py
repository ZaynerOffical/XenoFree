from discord.ext import commands


class UserBlacklisted(commands.CheckFailure):
    def __init__(self, message="User is baned!"):
        self.message = message
        super().__init__(self.message)


class NotUUID(commands.CheckFailure):
    def __init__(self, message="Invalid UUID"):
        self.message = message
        super().__init__(self.message)


# i wont use this cause its dumb :)


class UserNotOwner(commands.CheckFailure):
    def __init__(self, message="User is not owner!"):
        self.message = message
        super().__init__(self.message)
