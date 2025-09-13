import logging
import io

# io.StringIO ストリームを作成
log_stream = io.StringIO()
stream_handler = logging.StreamHandler(log_stream)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # ログレベルを設定
logger.addHandler(stream_handler)

try:
    logger.info("アプリケーションを開始します")
    logger.warning("設定ファイルが見つかりません")
    logger.error("データベース接続に失敗しました")

    # ログの内容を取得して表示
    log_content = log_stream.getvalue()
    log_list = log_content.strip().split("\n")
    print("\n--- 取得したログ内容 ---")
    print(log_list)
finally:
    logger.removeHandler(stream_handler)
    stream_handler.close()
    log_stream.close()


# 2. ロガーを注入して利用するクラス
class MyService:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def run(self):
        self.logger.info("サービスが実行されました。")
        self.logger.info("ログメッセージをいくつか出力します。")
