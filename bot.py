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
	print("# at {} user {} used /download url={}".format(at, by, url))

	if not validators.url(url):
		error_msg = "Sorry, not a valid url."
		print("error_msg: " + error_msg, file=stderr)
		await ctx.respond(error_msg)
		return

	await ctx.defer()

	command_1 = "yt-dlp -f bv[filesize<8M]+ba[filesize<2M] --print after_move:filepath --force-overwrites " + url
	ytdlp_run_1 = run(command_1.split(), stdout=PIPE, stderr=PIPE)
	if ytdlp_run_1.returncode == 0:
		filepath = ytdlp_run_1.stdout.decode().strip()
	else:
		command_2 = "yt-dlp -S size:10M -O %(filesize,filesize_approx)s " + url
		ytdlp_run_2 = run(command_2.split(), stdout=PIPE, stderr=PIPE)
		if ytdlp_run_2.returncode != 0 or int(ytdlp_run_2.stdout.decode().strip()) > 10_000_000: # >10Mo
			error_msg = "Sorry, something went wrong. Video may be too big (>10Mo)."
			print("error_msg: " + error_msg)
			print("command_1: {}\ncommand_1.stderr:\n{}".format(command_1, ytdlp_run_1.stderr.decode()).rstrip(), file=stderr)
			print("command_2: {}\ncommand_2.stderr:\n{}".format(command_2, ytdlp_run_2.stderr.decode()), file=stderr)
			await ctx.respond(error_msg)
			return
		filepath = ytdlp_run_2.stdout.decode().strip()

	await ctx.send_followup(file=discord.File(filepath))
	if os.path.exists(filepath):
		os.remove(filepath)

@bot.event
async def on_ready():
	print(f"logged in as {bot.user}")

dotenv.load_dotenv()
bot.run(os.getenv("DISCORD_TOKEN"))
