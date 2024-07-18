from pytube import YouTube
SAVE_PATH = "/home/user77/Desktop/my_opencv/OCVYolo8/data"
link = "https://www.youtube.com/watch?v=I_Pd_hFNmB0"
# link = "https://rr3---sn-4g5ednly.googlevideo.com/videoplayback?expire=1721096280&ei=-IOVZtXiJK6-v_IPuJSsyAU&ip=128.0.129.250&id=o-APNHrYzzfERcUddF_w85rQ_AbbdBnYn-JJyVhTnMauoa&itag=315&aitags=133%2C134%2C135%2C136%2C160%2C242%2C243%2C244%2C247%2C278%2C298%2C299%2C302%2C303%2C308%2C315%2C394%2C395%2C396%2C397%2C398%2C399%2C400%2C401&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&bui=AXc671IhA8LSrwUI3s6eMK9-svG4SCGwFCFPHkL3QMYn-kDlZpz5qpKjNN2vBA7f_cmMFrEBvgzX7raJ&spc=NO7bAeISeZtoBDsr0w39XZedTgJTdneYcb3dsxSnbVdENsEp19_5qA0nAPy7&vprv=1&svpuc=1&mime=video%2Fwebm&ns=wNH32ufFB23gRC6g76PZ9d8Q&rqh=1&gir=yes&clen=2614351754&dur=818.440&lmt=1716542188117683&keepalive=yes&c=WEB&sefc=1&txp=5432434&n=cx12Dn3qKZK7XQ&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AJfQdSswRgIhAOLxrjZElIwd36xna6YciBvRRdmtOoGQfQ8dXH0wovGnAiEAuzjAKSNSn8LQfIiN12ctymhEsSjswPbjikacZC2qGxk%3D&rm=sn-jvhnu5g-c35e7s,sn-jvhnu5g-n8ve77e,sn-n8vryek&rrc=79,79,104&fexp=24350515&req_id=7e09cb55d4aaa3ee&cmsv=e&redirect_counter=3&cms_redirect=yes&ipbypass=yes&mh=Sx&mip=176.9.113.53&mm=30&mn=sn-4g5ednly&ms=nxu&mt=1721078200&mv=m&mvi=3&pl=25&lsparams=ipbypass,mh,mip,mm,mn,ms,mv,mvi,pl&lsig=AHlkHjAwRgIhAIqp790Ezu0yvVcp-W2tt6MejMh6IQ_gzUhz8zyZG1f2AiEAwzr_jedLd-NnzRotL4QtsNAKXnXNr6aXDKp0W1EKkLE%3D"
yt = YouTube(link)


# stream = yt.streams.filter(res="480p").first()
# stream.download(SAVE_PATH)

# mp4_streams = yt.streams.get_highest_resolution()
# mp4_streams.download(output_path=SAVE_PATH)


print(f"{yt.streams=}")

# yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

# YouTube(link).streams.first().download()
