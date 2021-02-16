"""音楽ファイルの並列ダウンロードサンプル."""
import concurrent.futures
import random
import time
from collections import namedtuple
from os import path
from urllib import parse

import requests

from my_logging import get_my_logger

logger = get_my_logger(__name__)

# 音楽ファイルの名前とデータを保持するための名前付きタプルを定義
Music = namedtuple('music', 'file_name, file_content')
# クロールのリクエストごとの間隔を定義する 1秒から3.5秒までランダムに間隔を空ける
RANDOM_SLEEP_TIMES = [x * 0.1 for x in range(10, 40, 5)]  # 0.5秒刻み

# クロールするURLリスト
MUSIC_URLS = [
    'https://archive.org/download/ThePianoMusicOfMauriceRavel/01PavanePourUneInfanteDfuntePourPianoMr19.mp3',
    'https://archive.org/download/ThePianoMusicOfMauriceRavel/02JeuxDeauPourPianoMr30.mp3',
    'https://archive.org/download/ThePianoMusicOfMauriceRavel/03SonatinePourPianoMr40-Modr.mp3',
    'https://archive.org/download/ThePianoMusicOfMauriceRavel/04MouvementDeMenuet.mp3',
    'https://archive.org/download/ThePianoMusicOfMauriceRavel/05Anim.mp3',
]


def download(url, timeout=180):
    # mp3のファイル名をURLから取り出す
    parsed_url = parse.urlparse(url)
    file_name = path.basename(parsed_url.path)

    # リクエスト間隔をランダムに選択する
    sleep_time = random.choice(RANDOM_SLEEP_TIMES)

    # ダウンロードの開始をログ出力する
    logger.info("[download start] sleep: {time} {file_name}".format(
        time=sleep_time, file_name=file_name))

    # リクエストが失敗した場合でも後続のリクエストが連続しないようにここで間隔を空ける
    time.sleep(sleep_time)

    # 音楽ファイルのダウンロード
    r = requests.get(url, timeout=timeout)

    # ダウンロードの終了をログ出力する
    logger.info("[download finished] {file_name}".format(file_name=file_name))

    # 名前付きタプルにファイル名とmp3のデータ自身を格納して返す
    return Music(file_name=file_name, file_content=r.content)


if __name__ == '__main__':
    # 同時に2つの処理を並行実行するための executor を作成
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        logger.info("[main start]")

        # executor.submit() によりdownload()関数を並行実行する. download()関数の引数に music_url を与えている
        # 並行実行処理のまとまりを futures 変数に入れておく
        futures = [executor.submit(download, music_url) for music_url in MUSIC_URLS]

        # download()関数の処理が完了したものから future 変数に格納する
        for future in concurrent.futures.as_completed(futures):
            # download()関数の実行結果を result() メソッドで取り出す
            music = future.result()

            # music.filename にはmp3ファイルのファイル名が入っている.
            # このファイル名を使い、music.file_content に格納されている mp3 のデータをファイルに書き出す
            with open(music.file_name, 'wb') as fw:
                fw.write(music.file_content)
        logger.info("[main finished]")
