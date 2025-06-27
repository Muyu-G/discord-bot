import discord
from discord.ext import commands

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #ping command
    @commands.hybrid_command(name="ping", description="Bot latency")
    async def ping(self, ctx):
        embed = discord.Embed(
            title="Bot Latency",
            color=0x77B255,
            description=f"🏓 Pong! Latency: {round(self.bot.latency * 1000)}ms"  #converting to ms the rounding
            )
        
        await ctx.send(embed=embed)

    #userinfo command
    @commands.hybrid_command(name="userinfo", description="Displays a user info")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title=f"{member.display_name}'s Info", 
            color= 0x9B59B6
            )
        
        embed.add_field(
            name="Username", 
            value=member.name, 
            inline=False
            )
        
        embed.add_field(
            name="User ID", 
            value=member.id, 
            inline=False
            )
        
        embed.add_field(
            name="Joined Server", 
            value=member.joined_at.strftime("%d/%m/%Y"), 
            inline=False
            )
        
        embed.set_footer(
            text="Requested by "+ ctx.author.name, 
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
            )
        
        embed.set_thumbnail(
            url=member.avatar.url if member.avatar else discord.Embed.Empty
            )
        
        await ctx.send(embed=embed)

    #botinfo command
    @commands.hybrid_command(name="botinfo", description="Displays bot info")
    async def botinfo(self, ctx):
        bot_user = self.bot.user
        embed = discord.Embed(
            title=f"{bot_user}'s Info",
            color=0x5865F2
        )

        embed.add_field(
            name="Name", 
            value=bot_user, 
            inline=False
            )
        
        embed.add_field(
            name="Bot ID", 
            value=bot_user.id, 
            inline=False
            )
        
        embed.add_field(
            name="Latency",
            value=f"{round(self.bot.latency * 1000)} ms",
            inline=False
        )

        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )

        embed.set_thumbnail(
            url=bot_user.avatar.url if bot_user.avatar else None
        )
        await ctx.send(embed=embed)
        
    #serverinfo command
    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(
            title=f"{guild.name}'s info",
            color=0xA17FE0
        )
        
        embed.add_field(
            name="Members: ", 
            value=guild.member_count, 
            inline=True
        )

        embed.add_field(
            name="Channels: ",
            value=len(guild.channels),
            inline=True
        )
        
        embed.add_field(
            name="Server ID: ",
            value=guild.id,
            inline=True
        )
                
        embed.add_field(
            name="Created on: ",
            value=guild.created_at.strftime("%d/%m/%Y"),
            inline=True
        )
        
        embed.set_thumbnail(
            url=guild.icon.url if guild.icon else discord.Embed.Empty
        )
        
        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UserInfo(bot))