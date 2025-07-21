import os, re, dotenv, discord
from discord import option, ApplicationContext as Context, Message
from subprocess import run, PIPE

intents = discord.Intents.default()
intents.message_content = (True)

bot = discord.Bot(intents=intents)

@bot.command(description="Tries to download and send the original video from the given url")
@discord.option("url", type=str, description="the url to download from")
async def download(ctx: discord.ApplicationContext, url: str):
	await ctx.defer()

	filesize_run = run(["yt-dlp", "-f", "bv[filesize<8M]+ba[filesize<2M]", "-O", "%(filesize,filesize_approx)s", url], stdout=PIPE, stderr=PIPE)
	if filesize_run.returncode != 0 or int(filesize_run.stdout.decode().strip()) > 10_000_000: # >10Mo
		await ctx.respond("Sorry, the given video seems to be too big (>10Mo).", ephemeral=True)
		return

	filepath_run = run(["yt-dlp", "-f", "bv[filesize<8M]+ba[filesize<2M]", "--print", "after_move:filepath", "--force-overwrites", url], stdout=PIPE, stderr=PIPE)
	if filepath_run.returncode != 0:
		await ctx.respond("Sorry, something went wrong.", ephemeral=True)
		return
	filepath = filepath_run.stdout.decode().strip()
	await ctx.respond(file=discord.File(filepath))
	if os.path.exists(filepath):
		os.remove(filepath)

@bot.event
async def on_ready():
	print(f"logged in as {bot.user}")

dotenv.load_dotenv()
bot.run(os.getenv("DISCORD_TOKEN"))
