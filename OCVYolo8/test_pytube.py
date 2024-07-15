from pytube import YouTube
SAVE_PATH = "/home/user77/Desktop/my_opencv/OCVYolo8/data"
link = "https://www.youtube.com/watch?v=OgviTn4zW9c"

yt = YouTube(link)


# stream = yt.streams.filter(res="480p").first()
# stream.download(SAVE_PATH)

# mp4_streams = yt.streams.get_highest_resolution()
# mp4_streams.download(output_path=SAVE_PATH)


# yt.streams.filter(file_extension='mp4', res="720p").first().download()

yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

# YouTube(link).streams.first().download()
