import playwright
import playwright.sync_api
from playwright.sync_api import sync_playwright
import json
from tqdm import tqdm

with open ("sections.json", "r") as f:
    data = json.load(f)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    def fetch_description(url, selector):

            page.goto(url)
            page.wait_for_timeout(3000)
            description = page.query_selector(selector).text_content()
            return description

    selector_description = "div.s-rte"

    def check_if_url(url,selector):
        if url is not None:
            return fetch_description(url, selector)
        else:
            pass

    for item in tqdm(data):
        for i in range(len(item["activities"])):
            description = check_if_url((item["activities"][i]["url"]), selector_description)
            item["activities"][i]["description"] = description
            print(item["activities"][i]["description"])

with open ("sections_with_details.json", "w") as f:
    json.dump(data, f)