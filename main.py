from downloader import VideoDownloader

video_downloader = VideoDownloader(path = "/Users/saswatdas/Documents", log_to_file=False, convert_to_mp4= False)
video_downloader.create_folders_and_download_data()