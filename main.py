import os
import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Initialize Discord bot with intents
intents = discord.Intents.default()
intents.members = True  # Enable if you need member-related data
intents.presences = True  # Enable if you need presence-related data

bot = commands.Bot(command_prefix=';', intents=intents)

@app.route('/')
def home():
    return "Discord Bot is running!"

@bot.event
async def on_ready():
    try:
        s = await bot.tree.sync()
        print(f'Synced {len(s)} commands')
    except Exception as e:
        print(f'Error syncing commands: {e}')

    print(f'Logged in as {bot.user.name}')

@bot.tree.command(name='hello', description='Hello World!')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message('Hello World!')

@bot.tree.command(name='ping', description='Display the latency of the bot!')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! ||{round(bot.latency * 1000)}ms||')

@bot.tree.command(name='say', description='I\'ll repeat what you want to say!')
@app_commands.describe(what_to_say='The message you want me to say!')
async def say(interaction: discord.Interaction, what_to_say: str):
    await interaction.response.send_message(f'{what_to_say} - **{interaction.user.display_name}**')

@bot.tree.command(name='defer_response', description='I\'ll reply after a period of time!')
async def defer_response(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send('Waiting...')
    await asyncio.sleep(10)  # Use asyncio.sleep for non-blocking delay
    await interaction.edit_original_response(content='Replying after 10 seconds!')

if __name__ == "__main__":
    # Start the bot and Flask app
    port = int(os.environ.get("PORT", 5000))  # Use PORT from environment, default to 5000
    bot.loop.create_task(app.run_task(host='0.0.0.0', port=port))  # Run Flask app
    bot.run(os.getenv('token'))  # Run the Discord bot
