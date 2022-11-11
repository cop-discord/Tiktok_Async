from datetime import datetime
import re,aiohttp,orjson

class Video:
    def __init__(self, api):
        self.api = api
        
    async def get_video_binary(self, download_url):
        """
        DOWNLOAD_URL (str):
            Get this from the object that the parse_video_data function returns, it can either be download_video_url or download_video_url_watermark
            
        Returns:
            binary: Raw binary mp4 data        
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(download_url) as video:
                    binary=await video.read()
            #self.api.debug.success(f"Received binary data ({video.elapsed.total_seconds()}s)")
            return binary
        except Exception as e:
            print(e)
            
    async def get_data(self, url, raw=False) -> dict:
        """Grabs the video data from a tiktok video url
        
        URL/VIDEO_ID (str):
            https://vm.tiktok.com/ZMNnX3Q4q 
            7116227445648395526 
            https://www.tiktok.com/@peachyfitness4/video/7116227445648395526
        
        RAW (bool):
            Optional if u want the raw data tiktok provided from the video (this contains way more info)
            
        Returns:
            formatted data from the video in a json object 
            
        """
        async with aiohttp.ClientSession(json_serialize=orjson.loads) as session:
            async with session.get(f"https://tikwm.com/api?url={url}") as f:
                return await f.json()

    async def video_data_formatter(self, video_data):
        data = {"download_urls": {}, "author": {}, "stats": {}, "music": {}}
        data["created_at_timestamp"] = video_data["create_time"]
        data["created_at"] = str(datetime.fromtimestamp(video_data["create_time"]))
        data["video_url"] = f'https://tiktok.com/@{video_data["author"]["unique_id"]}/video/{video_data["aweme_id"]}'
        data["video_id"] = video_data["aweme_id"]
        data["download_urls"]["no_watermark"] = video_data['video']['play_addr']['url_list'][0]
        data["download_urls"]["watermark"] = video_data["video"]["play_addr"]["url_list"][2]
        data["author"]["avatar_url"] = video_data["author"]["avatar_larger"]["url_list"][0].replace("webp", "jpeg")
        data["author"]["username"] = video_data["author"]["unique_id"]
        data["author"]["nickname"] = video_data["author"]["nickname"]
        data["author"]["sec_uid"] = video_data["author"]["sec_uid"]
        data["author"]["user_id"] = video_data["author"]["uid"]
        data["description"] = video_data["desc"]
        data["video_length"] = video_data["video"]["duration"]/1000
        data["stats"] = {
            "comment_count": video_data["statistics"]["comment_count"],
            "likes": video_data["statistics"]["digg_count"],
            "downloads": video_data["statistics"]["download_count"],
            "views": video_data["statistics"]["play_count"],
            "shares": video_data["statistics"]["share_count"],
        }
        data["music"] = {
            "music_id": video_data["music"]["mid"],
            "album": video_data["music"]["album"],
            "title": video_data["music"]["title"],
            "author": video_data["music"]["author"],
            "length": video_data["music"]["duration"] 
        }
        return data
    
    def highest_soundquality_download_url(self, data):
        bit_rates = data["bit_rate"]
        bit_rates.sort(key=lambda key: key["bit_rate"], reverse=True)
        return bit_rates[0]["play_addr"]["url_list"][2]