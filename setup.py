# Copyright 2023 Gauthydev

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# 4. You are not allowed to claim this code as your own.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context, Bot

from pretty_help import PrettyHelp

from bot.exceptions import errors
from bot.helpers import keep_alive

import asyncio

from random import choice

import platform

bot = Bot(
    command_prefix=commands.when_mentioned_or("?"),
    intents=discord.Intents.all(),
    help_command=PrettyHelp(),
    description="Version 1 of the free predictor, May be open source",
)

@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Setup the game status task of the bot.
    """
    statuses = ["Bloxflip", "Predicting", "With you"]
    await bot.change_presence(activity=discord.Game(choice(statuses)))


async def load_cogs() -> None:
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/bot/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"bot.cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


@bot.event
async def on_ready() -> None:
    """
    The code in this event is executed when the bot is ready.
    """
    print(f"Logged in as {bot.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()
    await bot.tree.sync()




@bot.event
async def on_command_error(context: Context, error) -> None:
    if isinstance(error, errors.UserBlacklisted):
        embed = discord.Embed(
            description="You are blacklisted from using the bot / predictor!",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
        if context.guild:
            print(
                f"{context.author} (ID: {context.author.id}) tried to run a command in the guild {context.guild.name} (ID: {context.guild.id}), but the user is blacklisted from using the bot."
            )
        else:
            print(
                f"{context.author} (ID: {context.author.id}) tried to run a command in the bot's DMs, but the user is blacklisted from using the bot."
            )
    elif isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            description=f"Slow Down Mate! You can use this command in {error.retry_after}",
            color=discord.Color.red(),
        )
        await context.send(embed=em)


if __name__ == "__main__":
    asyncio.run(load_cogs())
    keep_alive.keep_alive()
    bot.run("TOKEN HERE")
