"""DBの内容を各種フォーマットで出力する."""
import json

import logging

from orator import DatabaseManager, Model
from orator.orm import belongs_to, has_many

# OratorがどんなSQLを実行するのかログを出力して確認します
logger = logging.getLogger('orator.connection.queries')
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    'It took %(elapsed_time)sms to execute the query %(query)s'
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)


# MySQLへの接続設定
config = {
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'aozora_bunko',
        'user': 'root',
        'password': '',
        'prefix': '',
        'log_queries': True,
    }
}

db = DatabaseManager(config)
Model.set_connection_resolver(db)


# 各テーブルとオブジェクトの関係性の定義
# クラス名を小文字かつスネークケースにし、複数形に読み替えたテーブル名が参照されます
class MojidukaiType(Model):
    """文字遣い種別."""

    pass


class Work(Model):
    """作品."""

    URL_FORMAT = "http://www.aozora.gr.jp/cards/{writer_id:06d}/card{id}.html"

    # worksテーブルのmojidukai_type_idはmojidukai_typesテーブルのid列から参照されます
    @belongs_to
    def mojidukai_type(self):
        """この作品の文字遣い."""
        return MojidukaiType

    # worksテーブルのwriter_idはwriterテーブルのid列から参照されます
    @belongs_to
    def writer(self):
        """この作品の作家."""
        return Writer

    def build_url(self):
        """作品URLを構築する."""
        return self.URL_FORMAT.format(
            writer_id=self.writer_id,
            id=self.id
        )


class Writer(Model):
    """作家."""

    # 作家と作品は1対多の関係になります
    @has_many
    def works(self):
        """この作家の作品群."""
        return Work


# 各フォーマットへの変換関数
def create_json():
    """JSONを作る."""
    works = []
    writers = Writer.all()
    writers.load('works', 'works.mojidukai_type')  # Eager Loading
    for writer in writers:
        for work in writer.works:
            d = {}
            d['id'] = work.id
            d['title'] = work.title
            d['url'] = work.build_url()
            d['writer'] = {'id': writer.id, 'name': writer.name}
            d['mojidukai_type'] = {'id': work.mojidukai_type.id, 'name': work.mojidukai_type.name}
            works.append(d)
    return json.dumps(works, ensure_ascii=False, indent=2)


# main実行ブロック
if __name__ == '__main__':
    json_str = create_json()
    print(json_str)
