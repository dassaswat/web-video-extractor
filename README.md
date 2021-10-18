
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

Create a new python file
```python
from downloader import VideoDownloader

video_downloader = VideoDownloader(path = path, log_to_file=False, convert_to_mp4= False)
video_downloader.create_folders_and_download_data()
```


  