import requests
import json


class Song:
    songName = ''
    artist = ''
    lyric = ''
    mediaUrl = ''


def getSong(mid):
    """

    :param mid: str
    :return: an instance of the Song class
    """

    song = Song()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76',
        'Cookie': '_ga=GA1.2.932287532.1638404291; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1673328749; _gid='
                  'GA1.2.515316208.1673328749; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1673329329; kw_token='
                  'YYHN7IXXPWS',
        'csrf': 'YYHN7IXXPWS'
    }

    infoGetUrl = 'http://m.kuwo.cn/newh5/singles/songinfoandlrc?musicId=' + \
                 mid + \
                 '&httpsStatus=1&reqId=d0343ab0-90a9-11ed-ab59-aba555305f03'

    infoResponse = requests.get(url=infoGetUrl).text

    infoData = json.loads(infoResponse).get('data')

    songInfo = infoData.get('songinfo')

    song.artist = songInfo.get('artist')

    song.songName = songInfo.get('songName')

    lrcList = infoData.get('lrclist')

    try:
        for line in lrcList:
            song.lyric = song.lyric + line.get('lineLyric') + ';'
    except TypeError:
        song.lyric = '暂无歌词'

    mediaGetUrl = 'http://www.kuwo.cn/api/v1/www/music/playUrl?mid=' + \
                  mid + \
                  '&type=music&httpsStatus=1&reqId=d037bd20-90a9-11ed-ab59-aba555305f03'

    mediaResponse = requests.get(url=mediaGetUrl).text

    song.mediaUrl = json.loads(mediaResponse).get('data').get('url')

    return song


if __name__ == '__main__':

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76',
        'Cookie': '_ga=GA1.2.932287532.1638404291; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1673328749; _gid='
                  'GA1.2.515316208.1673328749; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1673329329; kw_token='
                  'YYHN7IXXPWS',
        'csrf': 'YYHN7IXXPWS',
        'Referer': 'http://www.kuwo.cn/search/list?key=%E9%99%95%E5%8C%97%E6%B0%91%E6%AD%8C'
    }

    url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key=%E9%99%95%E5%8C%97%E6%B0%91%E6%AD%8C ' \
          '&pn=1&rn=30&httpsStatus=1&reqId=d08b4921-920e-11ed-bb35-197ef2168392'

    response = requests.get(url=url, headers=headers).text

    musicList = json.loads(response).get('data').get('list')

    songList = []

    for music in musicList:
        musicrId = music.get('musicrid')
        musicId = musicrId.split('_')[1]
        song = getSong(musicId)
        songList.append(song)

    with open('songList.json', 'w', encoding='utf-8') as fp:
        for song in songList:
            json.dump(obj=song.__dict__, fp=fp, ensure_ascii=False)
