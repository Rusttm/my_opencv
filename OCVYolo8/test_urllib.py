import urllib.request
url_link = 'http://example.com/video.mp4'  # replace with your actual video url
filename = 'video_name.mp4'
urllib.request.urlretrieve(url_link, filename)






import requests
def download_video(url, filename):
    r = requests.get(url)

    with open(filename, 'wb') as f:
        f.write(r.content)


# replace 'url' and 'filename'
download_video('http://example.com/video.mp4', 'video.mp4')


import urllib2
# video link and filename
dwn_link = 'https://class.coursera.org/textanalytics-001/lecture/download.mp4?lecture_id=73'
file_name = 'trial_video.mp4'
# download and save the video
rsp = urllib2.urlopen(dwn_link)
with open(file_name,'wb') as f:
    f.write(rsp.read())
# if Basic HTTP Authentication is required
password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
top_level_url = "http://class.coursera.org/"
password_mgr.add_password(None, top_level_url, username, password)
handler = urllib2.HTTPBasicAuthHandler(password_mgr)
# create "opener" (OpenerDirector instance)
opener = urllib2.build_opener(handler)
# use the opener to fetch a URL
opener.open(dwn_link)