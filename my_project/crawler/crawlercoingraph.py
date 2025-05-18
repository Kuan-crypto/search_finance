import requests
from bs4 import BeautifulSoup as bs
import re

base_url = "https://cointelegraph.com/"

keywords = [
    "bitcoin",
    "ada",
    "eth",
    "near",
    "trump"
]

def fetch_to_coingraph():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }

    response = requests.get(base_url,headers=headers,timeout=10)

    soup = bs(response.text,"html.parser")

    articles = []

    for article in soup.find_all("article"):
        title_tag = article.find("a",title=True)
        link_tag = article.find("a",href=True)

        if not title_tag or not link_tag:
            continue

        title = title_tag.get_text()
        href = link_tag["href"]

        if any(re.search(keyword , title, re.IGNORECASE) for keyword in keywords):
            if not href.startswith("http"):
                href = base_url+href

            articles.append((title,href))

    return articles

