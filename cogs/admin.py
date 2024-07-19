import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions
import os
import sys

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin Cog Loaded.")

    @commands.command()
    @has_permissions(administrator = True)
    async def clear(self, ctx, amount = 1):
        """ Deletes specified number of messages from channel """

        await ctx.channel.purge(limit = amount + 1)
    
    @commands.command()
    @has_permissions(administrator = True)
    async def rename(self, ctx, member: discord.Member, *, new_nickname):
        """ Changes a user's display name in the server """

        old_name = member.display_name
        await member.edit(nick = new_nickname)
        nickname_embed = discord.Embed(title = "Nickname Changed", description = f"{ctx.message.author.mention} changed {member.mention}'s nickname to **{new_nickname}** from **{old_name}**", color = 0xfc751b)
        await ctx.send(embed = nickname_embed)
    
    @commands.command()
    @has_permissions(administrator = True)
    async def give(self,ctx, member:discord.Member, role: discord.Role):
        """ Gives a role to the specified user """

        await member.add_roles(role)
        
        give_embed = discord.Embed(title = "Added Role", description = f'{ctx.message.author.mention} added {role.mention} to {member.mention}', color = 0x0bea2d)
        await ctx.send(embed = give_embed)

    @commands.command()
    @has_permissions(administrator = True)
    async def remove(self,ctx, member: discord.Member, role: discord.Role):
        """ Removes a role from the specified user """

        await member.remove_roles(role)

        rem_embed = discord.Embed(title = "Removed Role", description = f'{ctx.message.author.mention} removed {role.mention} from {member.mention}', color = 0xfc3b2d)
        await ctx.send(embed = rem_embed)
    
    @commands.command()   
    @has_permissions(administrator = True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        """ Kicks a given user from the server """

        await member.kick(reason=reason)

        kick_embed = discord.Embed(title="Kicked User", description=f'{ctx.message.author.mention} kicked {member.mention}', color = 0xfc3b2d)
        kick_embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=kick_embed)

    @commands.command()   
    @has_permissions(administrator = True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        """ Bans a given user from the server """

        await member.ban(reason=reason)
        ban_embed = discord.Embed(title="Banned User", description=f'{ctx.message.author.mention} banned {member.mention}', color = 0xfc3b2d)
        ban_embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=ban_embed)

    @commands.command(brief = "(admin) uban members")   
    @has_permissions(administrator = True)
    async def unban(self, ctx, *, username): 
        """ Unbans a given user from the server """

        bans = [entry async for entry in ctx.guild.bans()]

        for entry in bans:
            user = entry.user
            
            if (user.name == username):
                await ctx.guild.unban(user)
                unban_embed = discord.Embed(title="Unbanned User", description=f'{ctx.message.author.mention} unbanned {user.mention}', color = 0x0bea2d)
                await ctx.send(embed=unban_embed)
                break
    
    @commands.command()
    @has_permissions(administrator = True)
    async def whois(self, ctx, user: discord.User):
        """ Returns a users information """

        accent_color = 0x5865F2 if user.accent_color else user.accent_color
        banner = None if user.banner is None else user.banner
        print(user.accent_color, accent_color, user.color)
        print(user.public_flags.all())

        user_embed = discord.Embed(title=f'User Information for {user.name}', color=accent_color)
        
        if banner is not None:
            user_embed.set_thumbnail(url=user.avatar)
            user_embed.set_image(url=banner)
        else:
            user_embed.set_image(url=user.avatar)

        user_embed.add_field(name="Legacy username", value=f'{user.display_name}#{user.discriminator}', inline=False)
        user_embed.add_field(name="Username", value=user.name, inline=False)
        user_embed.add_field(name="Created at", value=f'{user.created_at}', inline=False)
        user_embed.add_field(name="User flags and badges", value=f'{user.public_flags.all()}')

        await ctx.send(embed=user_embed)
    
    @commands.command()
    @has_permissions(administrator = True)
    async def serverinfo(self, ctx):

        server = self.bot.get_guild(937243106967973919)

        server_embed = discord.Embed(title=f'{server.name}')
        server_embed.set_thumbnail(url=server.icon)
        server_embed.add_field(name="Member Count", value=server.member_count)
        server_embed.add_field(name="Online members", value=server.approximate_presence_count, inline=False)

        await ctx.send(embed=server_embed)
    
    @commands.command()
    @has_permissions(administrator = True)
    async def reboot(self, ctx):
        """ Restarts the bot with new changes """
        
        await ctx.send("Restarting...")
        python = sys.executable
        os.execl(python, python, *sys.argv, "-i", "bot.py")

async def setup(bot):
    await bot.add_cog(Admin(bot))
