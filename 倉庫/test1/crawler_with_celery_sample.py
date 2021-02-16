"""Celeryを使ったサンプル."""
import random
import time
from os import path
from urllib import parse

import requests

from celery import Celery
from pydub import AudioSegment

from my_logging import get_my_logger 


logger = get_my_logger(__name__)

# クロールのリクエストごとの間隔を定義する 1秒から3.5秒までランダムに間隔を空ける
RANDOM_SLEEP_TIMES = [x * 0.1 for x in range(10, 40, 5)]  # 0.5秒刻み

# アーティスト名
ARTIST_NAME = "Maurice RAVEL "
# アルバムタイトル
ALBUM_NAME = "The Piano Music of Maurice Ravel from archive.org"


# クロールするURLリスト
MUSIC_URLS = [
    'https://archive.org/download/ThePianoMusicOfMauriceRavel/01PavanePourUneInfanteDfuntePourPianoMr19.mp3',
    'https://archive.org/download/ThePianoMusicOfMauriceRavel/02JeuxDeauPourPianoMr30.mp3',
    'https://archive.org/download/ThePianoMusicOfMauriceRavel/03SonatinePourPianoMr40-Modr.mp3',
    'https://archive.org/download/ThePianoMusicOfMauriceRavel/04MouvementDeMenuet.mp3',
    'https://archive.org/download/ThePianoMusicOfMauriceRavel/05Anim.mp3',
]


# Reidsの0番目のDBを使う例です
app = Celery('crawler_with_celery_sample', broker='redis://localhost:6379/0')
app.conf.update(
    # Redisにタスクや、その実行結果を格納する際のフォーマットにJSONを指定
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Tokyo',
    enable_utc=True,  # Celeryタスク内では時刻をUTCで扱う
    # 1つのワーカーは同時に1つのプロセスだけ実行するようにする
    worker_max_tasks_per_child=1,
    # Redisに保存されるタスクの実行結果は60秒間経過したら破棄する
    result_expires=60,
    # ワーカーが標準出力に出力した内容をコマンド実行ターミナルには出さない
    worker_redirect_stdouts=False,
    # タスクの実行時間が180秒を超えた場合、タスクを終了させる
    task_soft_time_limit=180,

    # どのタスクをどのワーカーにルーティングするかの設定
    task_routes={
        'crawler_with_celery_sample.download': {
            'queue': 'download',
            'routing_key': 'download',
        },
        'crawler_with_celery_sample.cut_mp3': {
            'queue': 'media',
            'routing_key': 'media',
        },
    },
)


# リトライは最大2回まで, リトライ時は10秒の間隔を空ける
@app.task(bind=True, max_retries=2, default_retry_delay=10)
def download(self, url, timeout=180):
    """ファイルのダウンロード."""
    try:
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
        with open(file_name, 'wb') as fw:
            fw.write(r.content)

        # ダウンロードの終了をログ出力する
        logger.info("[download finished] {file_name}".format(file_name=file_name))
        cut_mp3.delay(file_name)  # cut_mp3関数の実行をタスクとしてエンキューする
    except requests.exceptions.RequestException as e:
        # 例外時はログを出力し、リトライする
        logger.error("[download error - retry] file: {file_name}, e: {e}".format(
            file_name=file_name, e=e))
        raise self.retry(exc=e, url=url)


@app.task
def cut_mp3(file_name):
    """先頭5秒を抜き出して保存する."""
    logger.info("[cut_mp3 start] {file_name}".format(file_name=file_name))

    # ダウンロードされたファイルをpydubのデータ形式に変換して読み込む
    music = AudioSegment.from_mp3(file_name)

    # mp3ファイルの先頭2秒間を切り出す
    head_time = 2 * 1000  # milliseconds
    head_part = music[:head_time]  # 切り出し
    root_name, ext = path.splitext(file_name)  # ファイル名を拡張子とそれ以外に分割

    # 保存
    # 元のファイルとの区別がつくよう、拡張子の手前に _head を付加したファイル名で
    # 切り出したデータを書き出す
    file_handler = head_part.export(
        root_name + "_head" + ext,
        format="mp3",
        tags={
            'title': root_name,
            'artist': ARTIST_NAME,
            'album': ALBUM_NAME,
        }
    )
    # ファイルハンドラをクローズすることを忘れない
    file_handler.close()
    logger.info("[cut_mp3 finished] {file_name}".format(file_name=file_name))


if __name__ == '__main__':
    logger.info("[main start]")

    # クロール対象のURLごとにdownload()関数をタスクとしてエンキューする
    # エンキューされたタスクはワーカーにより適時実行される
    for music_url in MUSIC_URLS:
        download.delay(music_url)
    logger.info("[main finished]")
