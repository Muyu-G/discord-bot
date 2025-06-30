import discord
from discord.ext import commands
from datetime import timedelta
from database import add_warning, get_warning

class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        #say command
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def say(self, ctx, *, message):
        await ctx.send(message)

        #warn command
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        add_warning(member.id, ctx.guild.id, reason or "No reason provided")
        embed = discord.Embed(
            title="User warned",
            description=f"{member.mention} was wanned",
            color=0xFFCC4D
        )
        embed.add_field(name="Reason",value=reason or "No reason provided", inline=False)
        await ctx.send(embed=embed)

        #warnings command - get user warnings
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warnings(self, ctx, member: discord.Member = None):
        warnings = get_warning(member.id, ctx.guild.id)
        embed = discord.Embed(
            title=f"Warnings for {member.mention}",
            color=0x00ff00
        )
        if warnings:
            for i, (reason, timestamp) in enumerate(warnings, 1):
                embed.add_field(name=f"Warning {i}", value=f"Reason: {reason}\nTime: {timestamp}", inline=False)
        else:
            embed.description = "No warnings found."
        await ctx.send(embed=embed)

        #ban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        await member.ban(reason=reason)

        embed = discord.Embed(
            title="Member banned 🔨", 
            description=f"{member.mention} was banned from the guild", 
            color=0xE74C3C
            )
        
        embed.add_field(
        name="Reason", 
        value=reason or None, 
        inline=False
            )

        await ctx.send(embed=embed)

        #unban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, *, reason = None):
        user = await self.bot.fetch_user(user_id) #fetching the banned user id
        await ctx.guild.unban(user, reason=reason)

        embed = discord.Embed(
            title="User unbanned 🔨", 
            description=f"{user.name} was unbanned", 
            color=0x43B581
            )
        
        embed.add_field(name="Reason", 
        value=reason or None, 
        inline=False
            )

        await ctx.send(embed=embed)

        #kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        await member.kick(reason=reason)

        embed = discord.Embed(
            title="Member kicked", 
            description=f"{member.mention} was kicked from the guild", 
            color=0xF04747
            )
        
        embed.add_field(
            name="Reason", 
            value=reason or None, 
            inline=False
            )
        
        await ctx.send(embed=embed)

        #mute command
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, *, minutes: int, reason = None):
        duration = timedelta(minutes=minutes) # timeout in minutes
        await member.timeout(duration, reason=reason)

        embed = discord.Embed(
            title="Member muted 🔇", 
            description=f"{member.mention} was muted", 
            color=0x747F8D
            )
        
        embed.add_field(
            name="Reason", 
            value=reason or None, 
            inline=False
            )
        
        await ctx.send(embed=embed)

        #clear command
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount: int):
        if amount <= 0 or amount > 100: #avaoiding discord rate-limiting
            embed = discord.Embed(
                title="Purge error (´。＿。｀)", 
                description="Please provide a valid amount of messages to purge (1 - 100)", 
                color=0xFAA61A
                )
            
            await ctx.send(embed=embed)

        else:
            await ctx.channel.purge(limit = amount + 1) #bot message included
            embed = discord.Embed(
                title="Message purge success ✅", 
                description=f"Deleted {amount} messages", 
                color=0xFAA61A
                )
            
            await ctx.send(embed=embed, delete_after=5)

        #lock channel command - to lock channels
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.set_permission(ctx.guild.default_role, send_messages=False) #ctx.guild.default_role = @everyone role
        await ctx.send("Channel locked successfully", delete_after=5)
        
        #unlock channel command
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permission(ctx.guild.default_role, send_messages=True)
        await ctx.send("Channel unlocked successfully", delete_after=5)
        
        #addrole command
    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member, role: discord.Role, reason=None):
        await member.add_roles(role, reason=reason)
        if reason:
            await ctx.send(f"{member.name} was given {role.name}, reason {reason}")
        await ctx.send(f"{member.name} was given {role.name}")
        
        #remove command
    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def removerole(self, ctx, member: discord.Member, role: discord.Role, reason=None):
        await member.remove_roles(role, reason=reason)
        if reason:
            await ctx.send(f"{member.name} was given {role.name}, reason {reason}")
        await ctx.send(f"{member.name} was given {role.name}")

    
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You don't have the permission to use this command", ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Provide the required amount please")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Provide a valid number!")
        else:
            await ctx.send(f"An error occurred: {error}")

    
async def setup(bot):
    await bot.add_cog(ModCommands(bot))