from playwright.sync_api import Page, expect


def test_readbook_3(page: Page) -> None:
    page.goto("http://localhost:18001/")
    page.get_by_role("link", name="排行榜").click()
    page.get_by_role("row", name="2 [其他类型] 爱是大雾散尽时 第20章 棠遥女儿的爸爸是谁 作者：白熙月 70.58万").get_by_role("link", name="[其他类型]").click()
    page.get_by_role("link", name="都市言情").click()
    page.get_by_role("link", name="系统逼我抄书怎么办").click()
    page.get_by_role("link", name="点击阅读").click()
