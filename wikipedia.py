from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.wikipedia.org/
    page.goto("https://www.wikipedia.org/")

    # Click input[name="search"]
    page.locator("input[name=\"search\"]").click()

    # Fill input[name="search"]
    page.locator("input[name=\"search\"]").fill("python ")

    # Click text=機械学習やAI開発、自動化ツールの作成やスクレイピングも可能な言語である。 インデントが意味を持つ「オフサイドルール」が特徴的である。 以下に、階乗 (関数名:
    page.locator("text=機械学習やAI開発、自動化ツールの作成やスクレイピングも可能な言語である。 インデントが意味を持つ「オフサイドルール」が特徴的である。 以下に、階乗 (関数名:").click()

    # Click text=Python 機械学習やAI開発、自動化ツールの作成やスクレイピングも可能な言語である。 インデントが意味を持つ「オフサイドルール」が特徴的である。 以下に、階 >> span >> nth=0
    page.locator("text=Python 機械学習やAI開発、自動化ツールの作成やスクレイピングも可能な言語である。 インデントが意味を持つ「オフサイドルール」が特徴的である。 以下に、階 >> span").first.click()
    page.wait_for_url("https://ja.wikipedia.org/wiki/Python")

    # Click text=Pythonのインタプリタは多くのOSに対応している。プログラマーのグローバルコミュニティは、無料のオープンソース [† 3] リファレンス実装であるCPyth
    page.locator("text=Pythonのインタプリタは多くのOSに対応している。プログラマーのグローバルコミュニティは、無料のオープンソース [† 3] リファレンス実装であるCPyth").click()
    page.wait_for_url("https://ja.wikipedia.org/wiki/Python%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2%E8%B2%A1%E5%9B%A3")

    # Go to https://ja.wikipedia.org/wiki/Python
    page.goto("https://ja.wikipedia.org/wiki/Python")

    # Click img[alt="Python"]
    page.locator("img[alt=\"Python\"]").click()
    page.wait_for_url("https://ja.wikipedia.org/wiki/Python#/media/%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB:Python_logo_and_wordmark.svg")

    # Click a[role="button"] >> nth=0
    page.locator("a[role=\"button\"]").first.click()

    # Click text=元のファイルをダウンロード
    with page.expect_download() as download_info:
        with page.expect_popup() as popup_info:
            page.locator("text=元のファイルをダウンロード").click()
        page1 = popup_info.value
    download = download_info.value
    page.wait_for_url(":")

    # Close page
    page1.close()

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
