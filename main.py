import discord, os, json
from discord.ext import commands
from datetime import datetime

def run(token):
    client = commands.Bot(command_prefix="!", help_command=None, intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f"{client.user.name}({client.user.id}) est lancé.")
        print("--------------------------")
        if not os.path.exists("assets"):
            os.mkdir("assets")

    @client.command()
    @commands.has_permissions(administrator=True)
    async def clear(ctx, nombre:int):
        messages = await ctx.channel.history(limit=nombre+1).flatten()
        for message in messages:
            await message.delete()

    @client.command()
    @commands.has_permissions(administrator=True)
    async def kick(ctx, user: discord.User, *reason):
        if not os.path.exists(f"assets/{ctx.guild.id}/kick"):
            os.mkdir(f"assets/{ctx.guild.id}/kick")
        reason = " ".join(reason)
        await ctx.guild.kick(user, reason=reason)

    @client.command()
    @commands.has_permissions(administrator=True)
    async def ban(ctx, user : discord.User, *reason, delete_message_days=7, member):
        if not os.path.exists(f"assets/{ctx.guild.id}/ban"):
            os.mkdir(f"assets/{ctx.guild.id}/ban")
        reason = " ".join(reason)
        await ctx.guild.ban(user, reason=reason, delete_message_days=delete_message_days)
        embed = discord.Embed(title="Banned !", description=f"{member} as ban !.", color=discord.Color.green())
        await ctx.send(embed=embed)
        with open(f"assets/{ctx.guild.id}/latest.log", "a+") as file:
            file.write(f"{ctx.member} ({ctx.member.id}) as banned by {ctx.message.author} ({ctx.message.author.id}) at {datetime.now()}")


    @client.command()
    @commands.has_permissions(administrator=True)
    async def unban(ctx, *, member):
        if not os.path.exists(f"assets/{ctx.guild.id}/unban"):
            os.mkdir(f"assets/{ctx.guild.id}/unban")
        if ctx.message.author.bot == False:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    embed = discord.Embed(title="Validation", description=f"{member} as unban.", color=discord.Color.green())
                    await ctx.send(embed=embed)
        for member in ctx.guild.members:
            unban = {
                "name": member.name,
                "discriminator": member.discriminator,
                "id": member.id,
                "bot": member.bot,
                "pdp": str(member.avatar_url),
            }
            with open(f"assets/{ctx.guild.id}/info/{member.id}.json", "w+") as file:
                json.dump(unban, file, indent=2)

    @client.command()
    @commands.has_permissions(administrator=True)
    async def info(ctx):
        if not os.path.exists(f"assets/{ctx.guild.id}"):
            os.mkdir(f"assets/{ctx.guild.id}")
        if not os.path.exists(f"assets/{ctx.guild.id}/info"):
            os.mkdir(f"assets/{ctx.guild.id}/info")
        for member in ctx.guild.members:
            info = {
                "name": member.name,
                "discriminator": member.discriminator,
                "id": member.id,
                "bot": member.bot,
                "pdp": str(member.avatar_url),
            }
            with open(f"assets/{ctx.guild.id}/info/{member.id}.json", "w+") as file:
                json.dump(info, file, indent=2)

    client.run(token)