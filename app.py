import json
from urllib.request import urlopen
from random import shuffle
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/")
def index():
    """初期画面を表示します."""
    return render_template("index.html")


@app.route("/api/recommend_article")
def api_recommend_article():
    """はてブのホットエントリーから記事を入手して、ランダムに1件返却します."""

    """1. はてブのホットエントリーページのHTMLを取得する"""
    with urlopen("http://feeds.feedburner.com/hatena/b/hotentry") as res:
        html = res.read().decode("utf-8")

    """2. BeautifulSoupでHTMLを読み込む"""
    soup = BeautifulSoup(html, "html.parser")

    """3. 記事一覧を取得する"""
    items = soup.select("item")

    """4. ランダムに1件取得する"""
    shuffle(items)
    item = items[0]

    """5. 以下の形式で返却する."""
    return json.dumps({
        "content": item.find("title").string,
        "link": item.get("rdf: about")
    })


@app.route("/tenki")
def index2():
    return render_template("index2.html")


@app.route("/api/get_weather")
def api_get_weather():
    with urlopen("https://weather.goo.ne.jp/weather/station/130504/3hours/") as res:
        html = res.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")

    items = soup(class_='weather_name')
    item = items[0]

    return json.dumps({
        "content": item.string
    })


if __name__ == "__main__":
    app.run(debug=True, port=5004)
