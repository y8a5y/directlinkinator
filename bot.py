import os, dotenv, discord, datetime
from sys import stderr

from src.utils import validate_url, download_audio, download_best

intents = discord.Intents.default()
intents.message_content = (True)

bot = discord.Bot(intents=intents)

@bot.command(description="Tries to download and send the original video from the given url")
@discord.option("url", type=str, description="the url to download from")
#@discord.option("audio_only", type=bool, required=False, default=False, description="is the media audio only?")
async def download(ctx: discord.ApplicationContext, url: str):
	audio_only = False # for now

	# some simple info to log
	now = datetime.datetime.now().isoformat(timespec="seconds")
	name = ctx.author.name
	print(f"# at {now} user {name} used /download url={url} audio_only={audio_only}")

	try:
		await validate_url(ctx, url)
		await ctx.defer()

		if audio_only:
			filepath = await download_audio(ctx, url)
		else:
			filepath = await download_best(ctx, url)

		await ctx.send_followup(file=discord.File(filepath))

		if os.path.exists(filepath):
			os.remove(filepath)

	except SystemExit:
		return

@bot.event
async def on_ready():
	print(f"logged in as {bot.user}")

dotenv.load_dotenv()
bot.run(os.getenv("DISCORD_TOKEN"))
