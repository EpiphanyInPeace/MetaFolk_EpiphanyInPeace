
import requests
import re
from lxml import etree
import json
import time


class Song:
    songName = ''
    artists = ''
    lyric = ''
    mediaUrl = ''

    def show(self):
        print('name = ' + self.songName)
        print('artists = ' + self.artists)
        print('lyric = ' + self.lyric)
        print('url = ' + self.url)


def getSong(songId):
    """

    :param songId: str
    :return: an instance of the Song class
    """

    theSong = Song()

    headers = {
        'user-agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/'
                      '108.0.0.0 Safari/537.36 Edg/108.0.1462.76'
    }

    infoUrl = 'https://music.163.com/api/song/detail/?ids=[' + songId + ']'

    infoResponse = requests.get(url=infoUrl, headers=headers)

    try:
        info = json.loads(infoResponse.text).get('songs')[0]

        theSong.songName = info['name']

        for artist in info['artists']:
            theSong.artists = theSong.artists + artist['name'] + ';'

    except TypeError:
        print(songId + '歌曲信息查询异常')

    lyricResponse = requests.get('https://music.163.com/api/song/lyric?id=' + songId + '&lv=1&kv=1&tv=-1')

    lrc = json.loads(lyricResponse.text).get('lrc')['lyric']

    theSong.lyric = re.sub('\\[.*?]', '', lrc)

    theSong.mediaUrl = 'http://music.163.com/song/media/outer/url?id=' + songId + '.mp3'

    return theSong


def getSongIdListFromAlbum(albumId):
    """

    :param albumId: str
    :return: a List of songId
    """

    songIdList = []

    albumUrl = 'http://music.163.com/api/album/' + albumId

    albumData = requests.get(url=albumUrl, headers=headers).text

    albumSongs = json.loads(albumData).get('album').get('songs')

    for data in albumSongs:
        songIdList.append(data.get('id'))

    return songIdList


if __name__ == '__main__':

    headers = {
        'user-agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/'
                      '108.0.0.0 Safari/537.36 Edg/108.0.1462.76'
    }

    searchUrl = 'http://music.163.com/api/search/get/web?s=' \
                '陕北民歌' \
                '&type=10&limit=20'

    searchResponse = requests.get(url=searchUrl).text

    albums = json.loads(searchResponse).get('result').get('albums')

    songIdList = []

    for album in albums:
        if albums.index(album) < 3:
            try:
                albumId = album.get('idStr')

                songIdList = getSongIdListFromAlbum(albumId)

                time.sleep(0.5)

            except AttributeError:
                print(album.get('idStr') + '专辑查询异常')

    songList = []

    for songId in songIdList:
        song = getSong(str(songId))
        songList.append(song)
        print(song.songName, song.mediaUrl)
        time.sleep(1)

    with open('songList.json', 'w', encoding='utf-8') as fp:
        for song in songList:
            json.dump(obj=song.__dict__, fp=fp, ensure_ascii=False)
            fp.write(',')
