import discord
from discord.ext import commands
import aiohttp

class JokeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.joke_api_url = "https://v2.jokeapi.dev/joke/Any"

    @commands.hybrid_command(name="joke", description="Get a random joke")
    async def joke_command(self, ctx):
        """Fetch and display a random joke"""
        await ctx.defer()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.joke_api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        embed = discord.Embed(
                            title="😂 Random Joke",
                            color=discord.Color.yellow()
                        )
                        
                        if data["type"] == "single":
                            embed.description = data["joke"]
                        else:
                            embed.add_field(name="Setup", value=data["setup"], inline=False)
                            embed.add_field(name="Punchline", value=data["delivery"], inline=False)
                        
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("❌ Failed to fetch a joke. Please try again later.")
        
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Could not fetch joke: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(JokeCog(bot))
