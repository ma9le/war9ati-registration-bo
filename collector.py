import requests
from bs4 import BeautifulSoup


URL = "https://www.education.gov.dz/"


def get_education_news():
    response = requests.get(URL, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for link in soup.find_all("a", href=True):
        title = link.get_text(" ", strip=True)
        href = link["href"]

        if title and href.startswith("http"):
            results.append({
                "title": title,
                "url": href
            })

    return results


if __name__ == "__main__":
    news = get_education_news()

    for item in news[:20]:
        print(item["title"])
        print(item["url"])
        print("-" * 50)