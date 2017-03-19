# ライブラリをインポート
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import upload
import logging
from logging.handlers import RotatingFileHandler

# MySQLドライバはmysql.connector
import mysql.connector
# Dockerを使う場合で、初期設定の場合hostは"192.168.99.100"
# MySQLのユーザやパスワード、データベースはdocker-compose.ymlで設定したもの
connector = mysql.connector.connect(
            user='python',
            password='python',
            host='192.168.99.100',
            database='sample')

cursor = connector.cursor()
cursor.execute("select * from users")

disp = ""
for row in cursor.fetchall():
    disp = "ID:" + str(row[0]) + "  名前:" + row[1]

cursor.close
connector.close

# Flaskはインスタンスを生成する
app = Flask(__name__)
app.config.update({'DEBUG': True })

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def hello():
    # return "Flask DBから取得 "+disp
    # Jinjaを使う
    logging.info('---root----')
    title = "ようこそ"
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    app.logger.info('Info')   
    message = "DBから取得 "+disp
    print(message)
    # index.html をレンダリングする
    return render_template('index.html', message=message, title=title)


#upload sample
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    message = ''
    if request.method == 'POST':
        f = request.files['file']
        f.save('tmp/' + secure_filename(f.filename))
        message = 'upload success'
    return render_template('upload.html', message=message) 


if __name__ == '__main__':
    handler = RotatingFileHandler('log/foo.log', maxBytes=10004, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    
    app.run(host='0.0.0.0')

