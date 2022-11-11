from datetime import datetime
import re,aiohttp,orjson
from pydantic import AnyUrl, BaseModel, Field
from typing import Optional

class MusicInfo(BaseModel):
    id: Optional[int] = Field(None, title='Music ID')
    title: Optional[str] = Field(None, title='Music Title')
    play: Optional[str] = Field(None, title='Music Play URL')
    cover: Optional[str] = Field(None, title='Cover URL')
    author: Optional[str] = Field(None, title='Sound Author')
    original: Optional[bool] = Field(None, title='If Original Or Not')
    duration: Optional[int] = Field(None, title='Sound Duration')
    album: Optional[str] = Field(None, title='Sound Album')

class Author(BaseModel):
    id: Optional[int] = Field(None, title='Author ID')
    unique_id: Optional[str] = Field(None, title='Author Username')
    nickname: Optional[str] = Field(None, title='Author Nickname')
    avatar: Optional[str] = Field(None, title='Author Avatar')


class Statistics(BaseModel):
    id: Optional[int] = Field(None, title='Video ID')
    region: Optional[str] = Field(None, title='Video Region')
    title: Optional[str] = Field(None, title='Video Title')
    cover: Optional[str] = Field(None, title='Cover Image')
    origin_cover: Optional[str] = Field(None, title='Origin Cover')
    duration: Optional[int] = Field(None, title='Video Duration')
    play: Optional[str] = Field(None, title='Non Watermarked URL')
    wmplay: Optional[str] = Field(None, title='Watermarked URL')
    music: Optional[str] = Field(None, title='Sound URL')
    music_info: Optional[MusicInfo] = None
    play_count: Optional[int] = Field(None, title='Sound Play Count')
    digg_count: Optional[int] = Field(None, title='Like Count')
    comment_count: Optional[int] = Field(None, title='Comment Count')
    share_count: Optional[int] = Field(None, title='Share Count')
    download_count: Optional[int] = Field(None, title='Download Count')
    create_time: Optional[int] = Field(None, title='Creation TimeStamp')
    author: Optional[Author] = None


class TikTok(BaseModel):
    code: Optional[int] = Field(None, title="Status Code")
    msg: Optional[str] = Field(None, title="Status Message")
    processed_time: Optional[float] = Field(None, title='Total Time Taken to Process')
    data: Optional[Statistics] = None


    async def get_video_binary(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.data.play) as video:
                    binary=await video.read()
            return binary
        except Exception as e:
            print(e)
            
    @classmethod
    async def get_data(self,url):
        async with aiohttp.ClientSession(json_serialize=orjson.loads) as session:
            async with session.get(f"https://tikwm.com/api?url={url}") as f:
                return cls.parse_raw(await f.read())
