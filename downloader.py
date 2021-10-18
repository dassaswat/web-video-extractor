import os
import json
import ffmpeg
import logging
import requests
from pprint import pprint
from dataExtractor import MagooshVideoDataExtractor


class VideoDownloader():
    def __init__(self, path: str, log_to_file: bool = False ,convert_to_mp4: bool = False):
        self.convert_to_mp4 = convert_to_mp4
        self.topics = ['INTRO', 'QUANTS', 'VERBAL', 'WRITING']
        self.path = path
        if not log_to_file:
            logging.basicConfig(
                level=logging.NOTSET,
                format="{asctime} {levelname} {message}",
                style='{',
                )
        else:
            logging.basicConfig(
                level=logging.NOTSET,
                format="{asctime} {levelname} {message}",
                style='{',
                filename='%slog' % __file__[:-2],
                filemode='w'
                )
    
    def get_data(self):
        try:
            with open('//data.json', 'r') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            logging.error("File not found! Creating a new one!")
            data_extractor = MagooshVideoDataExtractor()
            data_extractor.get_all_categories()
            data_extractor.get_data_with_video_urls()
            logging.info('A new "data.json" file has been created. Restart the Program in order to download all the videos!')

    def downloader(self, path: str, item: dict):
        os.chdir(path)
        sub_path = os.path.join(path, item['Head'])
        if not os.path.exists(sub_path):
            os.mkdir(sub_path)
        os.chdir(sub_path)
        for topics in item['sub-topics']:
            file_name = topics['topic-name'] + '.webm'
            
            logging.info("Downloading:%s"%file_name) 
            try:
                r = requests.get(topics['uri'], stream=True)
            except Exception as e:
                logging.error(f"Request to the server failed!")
            else:
                try:
                    with open(file_name, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024*1024):
                            if chunk:
                                f.write(chunk)
                except Exception as e:
                    logging.error(f"Something went wrong! Please Retry {e}")
                    break
                
                if self.convert_to_mp4:
                    logging.info("Converting to MP4")
                    try:
                        stream = ffmpeg.input(file_name)
                        stream = stream.output(stream, file_name.replace('.webm', '.mp4'))
                        ffmpeg.run(stream)
                        os.remove(file_name)
                    except Exception as e:
                        logging.error(f"Something went wrong! Please Retry {e}") 
                        break
                    
                    logging.info("Downloaded and Converted:%s"%file_name)
                
                else:
                    logging.info("Downloaded:%s"%file_name)

    def create_folders_and_download_data(self):
        data = self.get_data()
        path = os.path.join(self.path, 'MagooshVideos')
        
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            logging.error('Folder already exists')
        
        for item in data:
            if item['category'] in self.topics:
                new_path = os.path.join(self.path, 'MagooshVideos', item['category'])
                if not os.path.exists(new_path):
                    os.mkdir(new_path)
                    self.downloader(new_path, item)           
                else:
                    self.downloader(new_path, item)

        logging.info("All files downloaded Successfully!")


downloader = VideoDownloader(path='/Users/saswatdas/Downloads/')
downloader.create_folders_and_download_data()