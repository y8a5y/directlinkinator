FROM python:3.13-alpine

WORKDIR /usr/src/app

RUN apk add ffmpeg && \
	wget -P /usr/bin https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp && \
	chmod a+rx /usr/bin/yt-dlp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "./bot.py" ]
