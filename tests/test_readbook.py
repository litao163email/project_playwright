from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("http://localhost:18001/")
    page.get_by_placeholder("书名、作者、关键字").click()
    page.get_by_placeholder("书名、作者、关键字").fill("ni")
    page.locator("#btnSearch i").click()
    page.get_by_role("link", name="排行榜").click()
    page.get_by_role("link", name="@@@@@@....").click()
    page.get_by_role("link", name="点击阅读").click()
    page.get_by_role("link", name="下一章").click()
