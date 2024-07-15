from __future__ import unicode_literals
import youtube_dl

ydl_opts = {}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=rgiQw0jp4aY'])

    # $ yt-dlp -vU  -f "bv*+ba" https://www.youtube.com/watch?v=I_Pd_hFNmB0