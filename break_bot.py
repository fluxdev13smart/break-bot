import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
TOKEN = os.getenv('MTI5ODY3OTk2MDI4NjAwNzM0OQ.GgBmEi.mQ95_n_h-l6C3QmdS_Wl-TisIzuCxMdP1g4aLg')

# Set intents
intents = discord.Intents.default()
intents.members = True

# Create bot instance
bot = commands.Bot(command_prefix='/', intents=intents)

# Store break users and the designated break channel
break_users = []
break_channel_id = None  # This will hold the ID of the break channel

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command()
@commands.has_permissions(administrator=True)
async def setbreakchannel(ctx, channel: discord.TextChannel):
    """Set the channel for the /break command."""
    global break_channel_id
    break_channel_id = channel.id
    await ctx.send(f'The break channel has been set to: {channel.mention}')

@bot.command()
async def break(ctx):
    """Put the user on break."""
    if break_channel_id is None:
        await ctx.send('The break channel has not been set. Use /setbreakchannel to set it.')
        return

    if ctx.channel.id == break_channel_id:  # Check if the command is used in the designated channel
        user = ctx.author
        if user.id not in break_users:
            break_users.append(user.id)
            await ctx.send(f'{user.mention} is now on a break!')
        else:
            await ctx.send(f'{user.mention}, you are already on a break!')
    else:
        await ctx.send('You can only use this command in the designated break channel.')

@bot.command()
@commands.has_permissions(administrator=True)
async def breaklist(ctx):
    """List all users on break. Admins only."""
    if break_users:
        break_mentions = [ctx.guild.get_member(user_id).mention for user_id in break_users if ctx.guild.get_member(user_id)]
        await ctx.send('Users on break: ' + ', '.join(break_mentions))
    else:
        await ctx.send('No users are currently on break.')

@breaklist.error
async def breaklist_error(ctx, error):
    """Error handling for breaklist command."""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")

bot.run(TOKEN)
