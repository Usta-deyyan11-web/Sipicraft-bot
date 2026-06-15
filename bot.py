import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Configuration
MINECRAFT_SERVER_IP = os.getenv("MINECRAFT_SERVER_IP", "localhost:25565")
MINECRAFT_SERVER_HOST = MINECRAFT_SERVER_IP.split(":")[0]
MINECRAFT_SERVER_PORT = int(MINECRAFT_SERVER_IP.split(":")[1]) if ":" in MINECRAFT_SERVER_IP else 25565

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="ip", description="Get the Minecraft server IP")
async def ip_command(interaction: discord.Interaction):
    """Send the Minecraft server IP"""
    embed = discord.Embed(
        title="🎮 Minecraft Server IP",
        description=f"`{MINECRAFT_SERVER_IP}`",
        color=discord.Color.green()
    )
    embed.set_footer(text="Copy and paste this into your Minecraft client to join!")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="status", description="Check the Minecraft server status")
async def status_command(interaction: discord.Interaction):
    """Check the Minecraft server status"""
    await interaction.response.defer()
    
    try:
        from mcstatus import JavaServer
        
        server = JavaServer.lookup(MINECRAFT_SERVER_IP)
        status = server.status()
        
        embed = discord.Embed(
            title="🟢 Server Status: Online",
            color=discord.Color.green()
        )
        embed.add_field(name="Players Online", value=f"{status.players.online}/{status.players.max}", inline=False)
        embed.add_field(name="Server IP", value=f"`{MINECRAFT_SERVER_IP}`", inline=False)
        embed.add_field(name="Latency", value=f"{status.latency:.0f}ms", inline=False)
        
        if status.players.sample:
            player_names = "\n".join([player.name for player in status.players.sample])
            embed.add_field(name="Players Online", value=player_names, inline=False)
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        embed = discord.Embed(
            title="🔴 Server Status: Offline",
            description=f"Could not reach the server at `{MINECRAFT_SERVER_IP}`",
            color=discord.Color.red()
        )
        embed.add_field(name="Error", value=str(e), inline=False)
        await interaction.followup.send(embed=embed)

# Run the bot
if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise ValueError("DISCORD_BOT_TOKEN not found in .env file")
    bot.run(token)
