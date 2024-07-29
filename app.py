from flask import Flask, render_template, request, redirect, url_for
from flask_basicauth import BasicAuth
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

basic_auth = BasicAuth(app)

# MySQL Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL')
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
