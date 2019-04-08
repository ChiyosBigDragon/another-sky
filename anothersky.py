import re
import requests
from bs4 import BeautifulSoup
import os
import shutil

def scrape(soup) :
    pages = soup.find_all(class_='entryBox clearfix')
    for page in pages :
        div = page.find(class_='entryBody')
        # 日付取得
        date = ''.join(div.find('h3').text.split())
        print(date)
        dir = './data/' + date + '/'
        os.mkdir(dir)
        # 詳細取得
        details = div.find('p').text
        with open(dir + str('details.txt'), 'w', encoding='utf-8') as file :
            file.write(details)
        # 画像取得
        imgs = page.find_all('img')
        cnt = 0
        for img in imgs :
            src = requests.get(img['src'])
            with open(dir + str(cnt).zfill(3) + str('.jpg'), 'wb') as file :
                file.write(src.content)
                cnt += 1

def main():
    # dataディレクトリ作成
    if os.path.isdir('./data'):
        shutil.rmtree('./data')
    os.mkdir('./data')
    # URL生成
    for page in range(1,26):
        url = "http://www.ntv.co.jp/anothersky/fashion/index"
        if page > 1 :
            url += "_" + str(page)
        url += ".html"
        res = requests.get(url)
        content = res.content
        soup = BeautifulSoup(content, 'html.parser')
        # スクレイピング
        scrape(soup)

if __name__ == '__main__':
    main()
