"""Cog For Predictor"""
import random

from discord.ext import commands
from discord.ext.commands import Context
import discord

from bot.helpers import check


class Predictor(commands.Cog):
    """Cog for predictor"""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="mines")
    @check.not_blacklisted()
    @discord.app_commands.describe(game_id="Your bloxflip game id")
    async def mines(self, context: Context, game_id):
        """
        Randomly predicts mines, Non random one coming soon..

        Parameters:
        - context (Context): The context of the command.
        - game_id (str): The game ID for prediction.

        Returns:
        - None
        """
        uuid = check.is_valid_uuid(uuid=game_id, context=commands.Context)
        if uuid is True:
            random.seed(game_id)
            grid = [
                "❌",
                "✅",
                "✅",
                "✅",
                "❌",
                "❌",
                "❌",
                "❌",
                "❌",
                "❌",
                "❌",
                "❌",
                "✅",
                "❌",
                "❌",
                "✅",
                "❌",
                "❌",
                "❌",
                "❌",
                "❌",
                "❌",
                "❌",
                "❌",
                "❌",
            ]
            simplified_grid = ""
            random.shuffle(grid)
            for i in range(25):
                simplified_grid += grid[i]
                if (i + 1) % 5 == 0:
                    simplified_grid += "\n"
            embed = discord.Embed(title="Minesweeper Grid", color=discord.Color.blue())
            embed.add_field(name="Grid", value=simplified_grid, inline=False)
            embed.set_footer(
                text="Created by Zayner | Source Code: https://github.com/ZaynerOffical/XenoFree | https://discord.gg/KRdp5w9S8U"
            )
            await context.send(embed=embed)
        elif uuid is False:
            embed = discord.Embed(title="Invalid Game ID", color=discord.Color.red())
            embed.add_field(name="Error", value="The provided game ID is invalid.")
            await context.send(embed=embed)


async def setup(bot):
    """Setups cog"""
    await bot.add_cog(Predictor(bot))
