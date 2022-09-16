from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup as bs
from pandas import pandas as pd

def initplaywright(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    return browser, context

def exitplaywright(playwright: Playwright,browser,context) -> None:
    context.close()
    browser.close()

def login2list(playwright: Playwright,browser,context) -> None:
    # browser = playwright.chromium.launch(headless=False)
    # context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to https://itp.ne.jp/
    page.goto("https://itp.ne.jp/")
    # Click text=了承する
    page.locator("text=了承する").click()
    # Click [placeholder="キーワードを入力"]
    page.locator("[placeholder=\"キーワードを入力\"]").click()
    # Click [placeholder="キーワードを入力"]
    page.locator("[placeholder=\"キーワードを入力\"]").click()
    # Fill [placeholder="キーワードを入力"]
    page.locator("[placeholder=\"キーワードを入力\"]").fill("IT・情報通信")
    # Click [placeholder="エリア・駅 例）静岡市"]
    page.locator("[placeholder=\"エリア・駅 例）静岡市\"]").click()
    # Fill [placeholder="エリア・駅 例）静岡市"]
    page.locator("[placeholder=\"エリア・駅 例）静岡市\"]").fill("東京都")
    # Click form button
    page.locator("form button").click()
    page.wait_for_url("https://itp.ne.jp/keyword/?keyword=IT%E3%83%BB%E6%83%85%E5%A0%B1%E9%80%9A%E4%BF%A1&areaword=%E6%9D%B1%E4%BA%AC%E9%83%BD&sort=01&sbmap=false")
    # ---------------------
    
    import time
    
    while True:
        try:
            page.locator("button:has-text(\"さらに表示\")").click()
            time.sleep(2)

        except Exception as e:
            print('30秒経過 全対象表示完了')
            return page
    
def get_pageinfo(page) -> None:
    
    page.inner_html("#__layout > div > article > div.o-result-body > div > div > main > ul")

    html = page.content()
    soup = bs(html, "lxml")
    addinfos = []
    for addlist in soup.find_all('ul', class_='o-result-article-list'):
        for li in addlist.find_all('li'):
            infos = li.text.replace(' ','').replace('\n\n','\n').split('\n')
            flg = 0
            addinfo = {}
            for item in infos:
                if item == '':
                    continue
                if flg == 0:
                    addinfo['企業名'] = item
                    flg = 1
                elif flg == 1:
                    addinfo['事業者分類'] = item
                    flg = 2
                
                if '【最寄駅】' in item:
                    addinfo['最寄駅'] = item.replace('【最寄駅】','')
    
                if '【電話番号】' in item:
                    addinfo['電話番号'] = item.replace( '【電話番号】','')
                    
                if '【住所】' in item:
                    addinfo['住所'] = item.replace( '【住所】','')
                    
                if 'ウェブサイト' in item:
                    add_url = li.find_all(class_="m-card-tag-button")[0].get('href')
                    # add_url = li2[0].get('href')
                    addinfo['ウェブサイト'] = add_url
                    # print(addinfo)
            addinfos.append(addinfo)
    return addinfos
with sync_playwright() as playwright:
    browser,context = initplaywright(playwright)
    page = login2list(playwright,browser,context)
    addinfos = get_pageinfo(page)
    cs = pd.DataFrame(addinfos)
    cs.to_csv('result.csv',encoding='cp932')
    cs.to_csv('result.csv',encoding='cp932')
    exitplaywright(playwright,browser,context)


