import discord
import requests
from discord.ext import commands, tasks

TOKEN = 'MTE0MDk0MTU3OTI5Nzc1MTEwMQ.GDrBl7.5Oyo7L13PWy2SnvR3JTiX0Hf3mhEQbdMJSvzYc'
GUILD_ID = '1125059874812874752'
CHANNEL_ID = '1125563891838107668'
SERVER_IP = '119.195.205.75'
SERVER_PORT = '7783'

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@tasks.loop(minutes=5)
async def check_server():
    try:
        response = requests.get(f'http://{SERVER_IP}:{SERVER_PORT}/info/basic')
        data = response.json()
        player_count = data.get('players')
        channel = bot.get_guild(int(GUILD_ID)).get_channel(int(CHANNEL_ID))
        await channel.send(f"Current player count: {player_count}")
    except Exception as e:
        print(e)

@bot.command()
async def start_check(ctx):
    check_server.start()
    await ctx.send("Server checking started!")

@bot.command()
async def stop_check(ctx):
    check_server.stop()
    await ctx.send("Server checking stopped!")

bot.run(TOKEN)
