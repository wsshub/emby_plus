import json
from flask import Flask, request, redirect, jsonify
import requests
import pymysql
from logging.config import dictConfig

emby_url = 'https://movie.onerookie.site'
alist_url = 'https://pan.onerookie.site/api/fs/get'
main_site = "http://127.0.0.1:8096/"
api_key = 'emby的apiKey'
main_port = '8096'
new_port = '8097'
password_value = "alist密码"
replace_list = [
    {
        "from": "/onedrive/od-movie/",
        "to": "https://pan.onerookie.site/d/onedrive/"
    },
    {
        "from": "/onedrive/pp-movie-dav/",
        "to": "https://pan.onerookie.site/d/emby/"
    },
    {
        "from": "/onedrive/pp-movie2-dav/",
        "to": "https://pan.onerookie.site/d/emby2/"
    },
    {
        "from": "/onedrive/ali/",
        "to": "https://pan.onerookie.site/d/ali/"
    }
]

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(filename)s: %(lineno)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
#也可以用sqlite
db = pymysql.connect(
    host='127.0.0.1', port=3306, user='root', passwd='xxxxx', database='xxxx')


@app.route('/')
def send_static():
    """ serves all files from ./client/ to ``/client/<path:path>``
    :param path: path from api call
    """
    return "hello World"


@app.route('/api/detail', methods=['GET'])
def video_raw_url():
    path = request.args.get('target')
    app.logger.info('解析 %s', path)
    true_url = getRawUrl(path)
    res = {
        'true_url': true_url,
    }
    return res


@app.route('/emby/videos/<item_id>/<stream>')
def stream_proxy(item_id, stream):
    MediaSourceId = request.args.get('MediaSourceId')
    api_key = request.args.get('api_key')
    info_url = f"{main_site}emby/Items?Fields=Path&Ids={MediaSourceId}&api_key={api_key}"
    info_json = requests.get(url=info_url).json()
    index_url = str(info_json['Items'][0]['Path'])
    true_url = getRawUrl(index_url)
    return redirect(true_url)


def getRawUrl(index_url):
    if 'private' in index_url:
        data_pass = {"password": password_value,
                     'path': index_url.replace('/onedrive', '')}
        true_result = requests.post(
            alist_url, allow_redirects=False, data=data_pass)
        j = json.loads(true_result.text)
        true_url = j['data']['raw_url']
    else:
        for a in replace_list:
            index_url = index_url.replace(a['from'], a['to'])
        app.logger.info(f"处理后的直链:{index_url}")
        true_result = requests.get(index_url, allow_redirects=False)
        true_url = dict(true_result.headers)['Location']
    app.logger.info(f"重定向后的直链{true_url}")
    return true_url


def serialize(danmu):
    return{
        'video_title': danmu[0],
        'border': danmu[1],
        'color': danmu[2],
        'mode': danmu[3],
        'text': danmu[4],
        'time': danmu[5],
    }


@app.route('/api/danmu/all', methods=['GET'])
def all_danmu():
    video_title = request.args.get('video_title')
    app.logger.info('%s 加载弹幕', video_title)
    sql = f'SELECT video_title,border,color,mode,text,time FROM bullet_chat WHERE video_title="{video_title}"'
    cursor = db.cursor()
    cursor.execute(sql)
    danmus = cursor.fetchall()
    return jsonify(list(map(serialize, danmus)))


@app.route('/api/danmu/add', methods=['POST'])
def add_danmu():
    j = request.get_json()
    app.logger.info('发送弹幕 %s', j)
    sql = f"""INSERT INTO bullet_chat (video_title,border,color,mode,text,time)\
        VALUES ("{j['videoTitle']}",{j['border']},"{j['color']}",{j['mode']},"{j['text']}",{j['time']})"""
    insert(sql)
    app.logger.info('commit')
    return 'succeed'


def insert(sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f'插入失败：{e}')
    finally:
        cursor.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10809)
