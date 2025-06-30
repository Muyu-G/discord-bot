import discord
from discord.ext import commands

class MemberEvents(commands.Cog):
    # Welcome message
    # This method listens for "member joins the server"
    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            title="Welcome! 🤓",
            description=f"{member.mention} joined the server",
            color=0xF1C40F
        )
        
        embed.set_thumbnail(
            url = member.avatar.url if member.avatar else member.default_avatar.url
        )
        # Loop through all text channels in the server
        for channel in member.guild.text_channels:
            # Check if the bot has permission to send messages in this channel
            if channel.permissions_for(member.guild.me).send_messages:
                await channel.send(embed=embed)  # Send welcome message
                break  # Stop after the first channel that allows messages
        
    # On leave message
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(
            title="Sayonara, member-san 😣!",
            description=f"{member.mention} left the server",
            color=0x7FFFD4
        )
        
        embed.set_thumbnail(
            url = member.avatar.url if member.avatar else None
        )
        for channel in member.guild.text_channels:
            # Check if the bot has permission to send messages in this channel
            if channel.permissions_for(member.guild.me).send_messages:
                await channel.send(embed=embed)  # Send welcome message
                break  # Stop after the first channel that allows messages

    
    
async def setup(bot):
    await bot.add_cog(MemberEvents(bot))