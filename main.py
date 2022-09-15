from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup

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
    page.inner_html("#__layout > div > article > div.o-result-body > div > div > main > ul")
    return browser, context
with sync_playwright() as playwright:
    browser,context = initplaywright(playwright)
    browser,context = login2list(playwright,browser,context)
    exitplaywright()


