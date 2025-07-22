import os, re, dotenv, discord, validators, datetime
from discord import option, ApplicationContext as Context, Message
from subprocess import run, PIPE
from sys import stderr

intents = discord.Intents.default()
intents.message_content = (True)

bot = discord.Bot(intents=intents)

@bot.command(description="Tries to download and send the original video from the given url")
@discord.option("url", type=str, description="the url to download from")
async def download(ctx: discord.ApplicationContext, url: str):
	at = datetime.datetime.now().isoformat(timespec="seconds")
	by = ctx.author.name
	base_log = "# at {} user {} used /download url={}".format(at, by, url)

	if not validators.url(url):
		error_msg = "Sorry, not a valid url."
		print(base_log + "\nerror_msg: " + error_msg, file=stderr)
		await ctx.respond(error_msg)
		return

	await ctx.defer()

#	filesize_run = run(["yt-dlp", "-f", "bv[filesize<8M]+ba[filesize<2M]", "-O", "%(filesize,filesize_approx)s", url], stdout=PIPE)
#	if filesize_run.returncode != 0 or int(filesize_run.stdout.decode().strip()) > 10_000_000: # >10Mo
#		await ctx.respond("Sorry, the given video seems to be too big (>10Mo).", ephemeral=True)
#		return

	command = "yt-dlp -f bv[filesize<8M]+ba[filesize<2M] --print after_move:filepath --force-overwrites " + url
	filepath_run = run(command.split(), stdout=PIPE, stderr=PIPE)
	if filepath_run.returncode != 0:
		error_msg = "Sorry, something went wrong. Video may be too big (>10Mo)."
		print(base_log + "\nerror_msg: {}\ncommand: {}\ncommand.stderr:\n{}".format(error_msg, command, filepath_run.stderr.decode()), file=stderr)
		await ctx.respond(error_msg)
		return

	filepath = filepath_run.stdout.decode().strip()
	print(base_log)
	await ctx.send_followup(file=discord.File(filepath))
	if os.path.exists(filepath):
		os.remove(filepath)

@bot.event
async def on_ready():
	print(f"logged in as {bot.user}")

dotenv.load_dotenv()
bot.run(os.getenv("DISCORD_TOKEN"))
