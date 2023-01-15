
import requests
import re
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
        print('mediaUrl = ' + self.mediaUrl)


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

    infoResponse = requests.get(url=infoUrl, headers=headers).json()

    try:

        info = infoResponse.get('songs')[0]

        theSong.songName = info['name']

        for artist in info['artists']:

            theSong.artists = theSong.artists + artist['name'] + ';'

    except TypeError:

        print(songId + '歌曲信息查询异常')

    lyricResponse = requests.get('https://music.163.com/api/song/lyric?id=' + songId + '&lv=1&kv=1&tv=-1').json()

    lrc = lyricResponse.get('lrc')['lyric']

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

    albumData = requests.get(url=albumUrl, headers=headers).json()

    albumSongs = albumData.get('album').get('songs')

    for data in albumSongs:

        songIdList.append(data.get('id'))

    return songIdList


if __name__ == '__main__':
    # song = getSong('304827')
    # song.show()

    headers = {
        'user-agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/'
                      '108.0.0.0 Safari/537.36 Edg/108.0.1462.76'
    }

    searchUrl = 'http://music.163.com/api/search/get/web?s=' \
                '陕北民歌' \
                '&type=10&limit=20'

    searchResponse = requests.get(url=searchUrl).json()

    albums = searchResponse.get('result').get('albums')

    songIdList = []

    for i in range(len(albums)):

        if i < 3:

            albumId = albums[i].get('idStr')

            try:

                songIdList.extend(getSongIdListFromAlbum(albumId))

            except AttributeError:

                print(albumId + '专辑第一次查询异常')

            time.sleep(1)

    songList = []

    for songId in songIdList:

        song = getSong(str(songId))

        songList.append(song)

        time.sleep(1)

    with open('songList.json', 'w', encoding='utf-8') as fp:

        fp.write('[')

        for i in range(len(songList) - 1):

            json.dump(obj=songList[i].__dict__, fp=fp, ensure_ascii=False)

            fp.write(',')

        json.dump(obj=songList[-1].__dict__, fp=fp, ensure_ascii=False)

        fp.write(']')
