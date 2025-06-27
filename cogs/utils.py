import discord
from discord.ext import commands

class MemberEvents(commands.Cog):
    # Welcome message
    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            title="Welcome! 🤓",
            description=f"{member.mention} joined the server",
            color=0xF1C40F
        )
        embed.set_thumbnail(
            url = member.avatar.url if member.avatar else None
        )
        
    # On leave message
    @commands.Cog.listener()
    async def on_member_leave(self, member):
        embed = discord.Embed(
            title="Sayonara, member-san 😣!",
            description=f"{member.mention} left the server",
            color=0x7FFFD4
        )
        embed.set_thumbnail(
            url = member.avatar.url if member.avatar else None
        )
    
    
async def setup(bot):
    await bot.add_cog(bot)