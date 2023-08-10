"""
Copyright 2023 Gauthydev  <https://replit.com/@Gauthydev>

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

4. You are not allowed to claim this code as your own.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import discord
from discord.ext import commands
from bot.helpers import check
from discord.ext.commands import Context


class Utils(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="stats")
    @check.not_blacklisted()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def stats_command(self, context: Context) -> None:
        """
        Displays server and shard statistics.
        """
        server_count = len(self.bot.guilds)
        shard_count = self.bot.shard_count
        total_member_count = sum(guild.member_count for guild in self.bot.guilds)
        response_time = round(self.bot.latency * 1000, 2)
        embed = discord.Embed(title="Bot Statistics", color=discord.Color.blue())
        embed.add_field(name="Server Count", value=server_count)
        embed.add_field(name="Shard Count", value=shard_count)
        embed.add_field(name="Total Members", value=total_member_count)
        embed.add_field(name="Response Time", value=f"{response_time}ms")
        embed.add_field(name="View Source Code", value="https://github.com/ZaynerOffical/XenoFree")
        embed.set_footer(text="Author: Zayner | https://discord.gg/KRdp5w9S8U")
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Utils(bot))
