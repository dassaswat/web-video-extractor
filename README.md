
# MAGOOSH-GRE-VIDEO-EXTRACTOR

Its a project that I have built to extract video from the magoosh website using the Request, BeautifulSoup, and Selenium libraries. The project is made with no illegal infringement motives. I wanted to teach myself about data extarction through webscraping and I found the website to be an ideal choice. I have a subscription for GRE and anyone using the code file must have a valid subscription and must not violate magoosh's policies. I am making repo public just with a trust that people won't infringe rather go through the code for learning purpose.


## Features

- Download Video Either in WEBM format or MP4
- It automatically organises the videos by making directories.



  
## Installation

We need to install a few packages. First clone the repo

```bash
git clone https://github.com/dassaswat/web-video-extractor.git
```

Change the Directory

```bash
cd web-video-extractor
```

Create and start a Virtual Env

```bash
python -m venv {virtual-env name}
source {virtual-env name}/bin/activate
```

Install the required packages

```bash
pip install -r requirements.txt
```

Create a new config file in the same directory (Name of the file must be ""config.py")

```python
username = 'YOUR MAGOOSH USERNAME'
password = 'YOUR MAGOOSH PASSWORD'
```

Create a new python file. Set the path to where you would like to save you files. (Windows machines not tested if any bugs please do report!)
```python
from downloader import VideoDownloader

video_downloader = VideoDownloader(path = path, log_to_file=False, convert_to_mp4= False)
video_downloader.create_folders_and_download_data()
```

```
Now! the system will redirect you to Magoosh's website. Be patient it will fill in the login credential as provided.
Captcha verification might appear and if it appears please verify.Once done sit back and it will parse all the lesson
pages for the video urls. It might take around 30mins. Generally depends on your internet speed.

Once done you will have a json file and the downloads will soon begun. (As of now there are around 299 videos. So have a faster internet speed!)
```

You can set the logging feature either to console log or log in a file. Finally you can also setup if you want your videos to be in mp4 rather than webm.

```python
#If you want to log into file defaults to console log
video_downloader = VideoDownloader(path = path, log_to_file=True, convert_to_mp4= False) 

#To convert to mp4 set the (Conversion to mp4 requires ffmpeg to be installed on your local machine! Links for the installation tutorials are below!) 
convert_to_mp4 = True
```

```
MAC M1: 'https://www.youtube.com/watch?v=wOZ7p7Zmz2s'
MAC INTEL: 'https://www.youtube.com/watch?v=zl4vo0dhLRk'
WINDOWS: 'https://www.youtube.com/watch?v=GI7JGouGPsE'
LINUX: 'https://www.youtube.com/watch?v=tf4p-SMw5jA'
```
## Authors

- [@Saswat Das](https://github.com/dassaswat)

  
