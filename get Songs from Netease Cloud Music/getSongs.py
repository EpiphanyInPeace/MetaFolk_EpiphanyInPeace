
import requests
import re
import pymysql


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


def getSong(song_Id):
    """

    :param song_Id: str
    :return: an instance of the Song class
    """

    theSong = Song()

    headers_ = {
        'user-agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/'
                      '108.0.0.0 Safari/537.36 Edg/108.0.1462.76'
    }

    infoUrl = 'https://music.163.com/api/song/detail/?ids=[' + song_Id + ']'

    infoResponse = requests.get(url=infoUrl, headers=headers_).json()

    try:

        info = infoResponse.get('songs')[0]

        theSong.songName = info['name']

        for artist in info['artists']:

            theSong.artists = theSong.artists + artist['name'] + ';'

        lyricResponse = requests.get('https://music.163.com/api/song/lyric?id=' + song_Id + '&lv=1&kv=1&tv=-1').json()

        lrc = lyricResponse.get('lrc')['lyric']

        theSong.lyric = re.sub('\\[.*?]', '', lrc)

        theSong.mediaUrl = 'http://music.163.com/song/media/outer/url?id=' + song_Id + '.mp3'

        return theSong
    except TypeError:

        print(song_Id + '歌曲信息查询异常，访问过于频繁，请稍后再试')
        return None


def getSongIdListFromAlbum(album_Id):
    """

    :param album_Id: str
    :return: a List of songId
    """

    headers_ = {
        'user-agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/'
                      '108.0.0.0 Safari/537.36 Edg/108.0.1462.76'
    }

    songId_List = []

    albumUrl = 'http://music.163.com/api/album/' + album_Id

    print('第1次查询' + album_Id + '专辑信息...')

    albumData = requests.get(url=albumUrl, headers=headers_).json()

    count = 1

    while albumData.get('code') != 200:

        count += 1

        print('第' + str(count) + '次查询' + album_Id + '专辑信息...')

        albumData = requests.get(url=albumUrl, headers=headers_).json()

    albumSongs = albumData.get('album').get('songs')

    for data in albumSongs:

        songId_List.append(data.get('id'))

    return songId_List


def putSongListIntoDB(song_List):
    """

    :param song_List: a List of instances of class Song
    :return:
    """

    db = pymysql.connect(host='localhost', user='root', password='root', database='metafolk')

    print('数据库连接成功')

    cursor = db.cursor()

    for song_ in song_List:

        insert_Song = "insert into song(song_name) values('{song_name}');".format(song_name=song_.songName)

        cursor.execute(insert_Song)

        get_song_id = "select song_id from song order by song_id desc limit 1;"

        cursor.execute(get_song_id)

        insert_item_song = "insert into item_song(song_ref_id, item_singer) values({song_ref_id}, " \
                           "'{item_singer}');".format(
                            song_ref_id=cursor.fetchone()[0], item_singer=song_.artists)

        cursor.execute(insert_item_song)

        get_item_id = "select item_id from item_song order by item_id desc limit 1;"

        cursor.execute(get_item_id)

        insert_item_lyrics = "insert into item_lyrics(item_ref_id, lyrics) values({item_ref_id}, " \
                             "'{lyrics}');".format(
                              item_ref_id=cursor.fetchone()[0], lyrics=song_.lyric)

        cursor.execute(insert_item_lyrics)

    db.commit()

    cursor.close()

    db.close()


if __name__ == '__main__':

    headers = {
        'user-agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/'
                      '108.0.0.0 Safari/537.36 Edg/108.0.1462.76'
    }

    searchUrl = 'https://music.163.com/api/search/get/web?s=' \
                '陕北民歌' \
                '&type=10&limit=20'

    searchResponse = requests.get(url=searchUrl).json()

    albums = searchResponse.get('result').get('albums')

    songIdList = []

    for i in range(len(albums)):

        if i < 2:

            albumId = albums[i].get('idStr')

            songIdList.extend(getSongIdListFromAlbum(albumId))

    songList = []

    for songId in songIdList:

        song = getSong(str(songId))

        if song is not None:

            songList.append(song)

    putSongListIntoDB(songList)

    # with open('songList.json', 'w', encoding='utf-8') as fp:
    #
    #     fp.write('[')
    #
    #     for i in range(len(songList) - 1):
    #
    #         json.dump(obj=songList[i].__dict__, fp=fp, ensure_ascii=False)
    #
    #         fp.write(',')
    #
    #     json.dump(obj=songList[-1].__dict__, fp=fp, ensure_ascii=False)
    #
    #     fp.write(']')
