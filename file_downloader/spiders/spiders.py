# from tools.save_json.save import save_json
import scrapy
import requests
import os
from urllib.parse import unquote
from datetime import datetime

class FiledownloaderSpider(scrapy.Spider):
    name = "spider"
    start_urls = []

    def start_requests(self):
        headers = {
            'User-Agent': 'Your User Agent'
        }
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        domain = response.url.split('/')[2]
        self.source = 'Article Archive'

        file_names = []        
        response = requests.get(response.url, verify=False)
        if response.status_code == 200:
            content_disposition = response.headers.get('content-disposition')
            if content_disposition:
                name = content_disposition.split('filename=')[-1]
                name = unquote(name).strip().strip('"')
            else:
                extension = response.url.split('.')[-1]
                name = response.url.split('/')[-1] + '.' + extension

            file_names.append(name)
        path_raw = 'json'
        dir_raw = os.path.join(self.source ,path_raw)
        os.makedirs(dir_raw, exist_ok=True)
        for file_name in file_names:
            exs = file_name.split('.')[-1]

        filename_json = response.url.split('/')[-1]+'.json'
        # filename_json = f'{int(datetime.now().timestamp())}.json'


        data = {
            'link' : response.url,
            'domain' : domain,
            'crawling_time' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'crawling_time_epoch' : int(datetime.now().timestamp()),
            'file_name' : file_names,
        }
        # save_json(data, os.path.join(dir_raw, filename_json))
        
        for link in self.start_urls:
            self.download_file(link)

    def download_file(self, url):
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            content_disposition = response.headers.get('content-disposition')
            if content_disposition:
                file_name = content_disposition.split('filename=')[-1]
                file_name = unquote(file_name).strip().strip('"')
            elif 'filename*=' in content_disposition:
                file_name = content_disposition.split('filename*=')[-1]
                file_name = unquote(file_name).strip().strip('"')
            else:
                extension = url.split('.')[-1]
                file_name = url.split('/')[-1] + '.' + extension
                
            
            exs = file_name.split('.')[-1]
            save_directory = os.path.join(self.source, exs)
            os.makedirs(save_directory, exist_ok=True)
            save_path = os.path.join(save_directory)
            
            with open(os.path.join(save_path, file_name.replace('"', '').replace("'", "").replace(':', '')), 'wb') as f:
                f.write(response.content)
        else:
            self.logger.error(f"Failed to download file from {url}")