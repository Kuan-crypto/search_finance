import requests
from bs4 import BeautifulSoup as bs
import re

base_url = "https://abmedia.io/"


def fetch_to_abmedia():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }

    keywords = [
        "比特幣",
        "以太幣",
        "eth",
        "bitcoin",
        "ada",
        "near"
    ]

    articles = []

    pages =4
    for page in range(1, pages + 1):
        url = f"https://abmedia.io/blog/page/{page}"

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = bs(response.text, "html.parser")

            for article in soup.find_all("article"):
                title_tag = article.find("h3", class_=True)
                link_tag = article.find("a", href=True)

                if not title_tag or not link_tag:
                    continue

                title = title_tag.get_text()
                href = link_tag["href"]

                if any(re.search(keyword, title, re.IGNORECASE) for keyword in keywords):
                    if not href.startswith("http"):
                        href = base_url + href
                    articles.append((title, href))


        else:
            print(f"抓不到該網站，狀態碼{response.status_code}")

    return articles