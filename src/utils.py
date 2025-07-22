import validators, discord
from sys import stderr, exit
from subprocess import run, PIPE

async def validate_url(ctx: discord.ApplicationContext, url: str):
	if not validators.url(url):
		error_msg = "Sorry, not a valid url."
		print_error("! error_msg: " + error_msg)
		await ctx.respond(error_msg)
		exit(1)

async def download_best(ctx: discord.ApplicationContext, url: str):
	command_best = "yt-dlp -f bv[filesize<8M]+ba[filesize<2M] --print after_move:filepath --force-overwrites " + url
	ytdlp_run_best = run(command_best.split(), stdout=PIPE, stderr=PIPE)

	if ytdlp_run_best.returncode != 0:
		error_msg = "Sorry, something went wrong. Video may be too big (>10Mo)."
		print_error("! error_msg: " + error_msg)
		print_error("! command_best: " + command_best)
		print_error("! command_best.stderr:\n" + ytdlp_run_best.stderr.decode().rstrip())
		await ctx.respond(error_msg)
		exit(ytdlp_run_best.returncode)

	return ytdlp_run_best.stdout.decode().strip()

async def download_audio(ctx: discord.ApplicationContext, url: str):
#	command_2 = "yt-dlp -S size:10M -O %(filesize,filesize_approx)s " + url
#	ytdlp_run_2 = run(command_2.split(), stdout=PIPE, stderr=PIPE)
#	if ytdlp_run_2.returncode != 0 or int(ytdlp_run_2.stdout.decode().strip()) > 10_000_000: # >10Mo
#		error_msg = "Sorry, something went wrong. Video may be too big (>10Mo)."
#		print("error_msg: " + error_msg)
#		print("command_2: {}\ncommand_2.stderr:\n{}".format(command_2, ytdlp_run_2.stderr.decode()), file=stderr)
#		await ctx.respond(error_msg)
#	filepath = ytdlp_run_2.stdout.decode().strip()
	exit(1)

def print_error(error: str):
	print(error, file=stderr)
