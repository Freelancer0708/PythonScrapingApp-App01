from flask import Flask, render_template, request, redirect, url_for
from flask_basicauth import BasicAuth
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# ベーシック認証の設定
app.config['BASIC_AUTH_USERNAME'] = 'your_username'  # ここを環境変数に変更する場合はConfigクラスで設定します
app.config['BASIC_AUTH_PASSWORD'] = 'your_password'  # ここを環境変数に変更する場合はConfigクラスで設定します
basic_auth = BasicAuth(app)

# MySQL Database Configuration
DATABASE_URL = app.config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(DATABASE_URL)

@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
@basic_auth.required
def scrape():
    url = request.form['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {'Title': [], 'Link': []}
    for item in soup.select('a'):
        if item.text and item.get('href'):
            data['Title'].append(item.text)
            data['Link'].append(item.get('href'))

    df = pd.DataFrame(data)
    df.to_sql('scraped_data', con=engine, if_exists='replace', index=False)

    return redirect(url_for('results'))

@app.route('/results')
@basic_auth.required
def results():
    # データベースからデータを取得
    df = pd.read_sql('scraped_data', con=engine)
    data = df.to_dict(orient='records')
    return render_template('results.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
