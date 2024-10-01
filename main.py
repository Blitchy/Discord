import os
import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
import asyncio

# Initialize Flask app
app = Flask(__name__)

# Initialize Discord bot without special intents
bot = commands.Bot(command_prefix=';')

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

async def main():
    # Start the Discord bot
    await bot.start(os.getenv('token'))

if __name__ == "__main__":
    # Start the Flask app in a separate thread
    port = int(os.environ.get("PORT", 5000))  # Use PORT from environment, default to 5000
    loop = asyncio.get_event_loop()
    
    # Start Flask app in a separate task
    loop.run_in_executor(None, app.run, '0.0.0.0', port)  # Run Flask app
    loop.run_until_complete(main())  # Run the Discord bot
