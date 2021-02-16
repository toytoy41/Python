from logging import (
    getLogger,
    Formatter,
    FileHandler,
    StreamHandler,
    DEBUG,
    ERROR,
)

import requests


# ロガー: __name__ には実行モジュール名 logging_sample が入ります
logger = getLogger(__name__)

# 出力フォーマット
default_format = '[%(levelname)s] %(asctime)s %(name)s %(filename)s:%(lineno)d %(message)s'
default_formatter = Formatter(default_format)
funcname_formatter = Formatter(default_format + ' (%(funcName)s)')

# ログ用ハンドラー: コンソール出力用
log_stream_handler = StreamHandler()
log_stream_handler.setFormatter(default_formatter)
log_stream_handler.setLevel(DEBUG)

# ログ用ハンドラー: ファイル出力用
log_file_handler = FileHandler(filename="crawler.log")
log_file_handler.setFormatter(funcname_formatter)
log_file_handler.setLevel(ERROR)

# ロガーにハンドラーとレベルをセット
logger.setLevel(DEBUG)
logger.addHandler(log_stream_handler)
logger.addHandler(log_file_handler)


def logging_example():
    logger.info('クロールを開始します.')
    logger.warning('外部サイトのリンクのためクロールしません.')
    logger.error('ページが見つかりませんでした')

    try:
        r = requests.get('#invalid_url', timeout=1)
    except requests.exceptions.RequestException as e:
        logger.exception('リクエスト中に例外が起きました: %r', e)


if __name__ == '__main__':
    logging_example()
