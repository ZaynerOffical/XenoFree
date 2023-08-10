from discord.ext import commands
from discord.ext.commands import Context
import discord

from typing import Optional

from bot.helpers import db_helper
from bot.helpers import check


class Owner(commands.Cog):
    """Cog for owner"""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="blacklist")
    @check.is_user_owner()
    @discord.app_commands.describe(
        user="The user to blacklist",
        reason="Why to blacklist"
    )
    async def blacklist(
        self,
        context: Context,
        user: discord.Member,
        reason: Optional[str]
    ):
        """
        Blacklists a user using the database.

        Parameters:
        - context (Context): The context of the command.
        - user (discod.Member): The member to blacklist.
        - reason (optional str): The reason for blacklisting the user.

        Returns:
        - None
        """

        try:
            user_id = user.id            
            if db_helper.is_prohibited(user_id):
                embed = discord.Embed(
                    description=f"**{user.name}** is already in the blacklist.",
                    color=0xE02B2B,
                )
                await context.send(embed=embed)
                return

            total = db_helper.add_user_to_blacklist(user_id)
            embed = discord.Embed(
                description=f"**{user.name}** has been successfully added to the blacklist",
                color=0x9C84EF,
            )
            embed.set_footer(
                text=f"There {'is' if total == 1 else 'are'} now {total} {'user' if total == 1 else 'users'} in the blacklist | https://github.com/ZaynerOffical/XenoFree"
            )
            await user.send(embed=discord.Embed(
                title="You've been blacklisted",
                color=discord.Color.random()
            ))
            await context.send(embed=embed)

        except Exception as e:
            await context.send(e)
            print(e)

    @commands.hybrid_command(name="blacklist_remove")
    @check.is_user_owner()
    @discord.app_commands.describe(
        user="The user to remove",
        reason="Why to remove blacklist"
    )
    async def blacklist_remove(
        self,
        context: Context,
        user: discord.Member,
        reason: Optional[str]
    ):
        """
        Removes a Blacklists user using the database.

        Parameters:
        - context (Context): The context of the command.
        - user (discord.Member): The member to un-blacklist.
        - reason (optional str): The reason for un-blacklisting the user.

        Returns:
        - None
        """

        try:
            user_id = user.id            
            if not db_helper.is_prohibited(user_id):
                embed = discord.Embed(
                    description=f"**{user.name}** not blacklisted.",
                    color=0xE02B2B,
                )
                await context.send(embed=embed)
                return

            total = db_helper.remove_user_from_blacklist(user_id)
            embed = discord.Embed(
                description=f"**{user.name}** has been successfully removed from blacklist db",
                color=0x9C84EF,
            )
            embed.set_footer(
                text=f"There {'is' if total == 1 else 'are'} now {total} {'user' if total == 1 else 'users'} in the blacklist | https://github.com/ZaynerOffical/XenoFree"
            )
            await context.send(embed=embed)

        except Exception as e:
            await context.send(e)
            print(e)


async def setup(bot):
    """Setups cog"""
    await bot.add_cog(Owner(bot))
