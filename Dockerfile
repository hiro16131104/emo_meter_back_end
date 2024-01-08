# python3.11.3をベースイメージとして使用
FROM python:3.11.3

# lambda web adapterをインストール
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.5.0 /lambda-adapter /opt/extensions/lambda-adapter

# 環境変数を定義
ENV TZ Asia/Tokyo
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

# FastAPIで開発したアプリを丸ごとコピーし、pythonライブラリをインストール
WORKDIR /emo_meter_back_end
COPY . .
RUN pip install --upgrade pip
RUN pip install -r ./config/requirements.txt

# DockerコンテナとAPサーバーのポート番号を設定
ENV PORT=8080
EXPOSE 8080
# ENV PORT=5050
# EXPOSE 5050

# アプリの起動コマンドを設定
CMD ["python", "run.py"]