import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.education.gov.dz/"


KEYWORDS = [
    "مسابقة",
    "مسابقات",
    "توظيف",
    "التوظيف",
    "تسجيل",
    "التسجيل",
    "مناظرة",
    "مباراة",
    "إعلان",
    "إعلانات",
    "بلاغ",
    "منشور",
    "مترشحين",
    "المترشحين",
    "نتائج"
]


def get_education_news():
    try:
        response = requests.get(
            BASE_URL,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        seen_urls = set()

        for link in soup.find_all("a", href=True):

            title = link.get_text(" ", strip=True)
            url = urljoin(BASE_URL, link["href"])

            if not title:
                continue

            title_lower = title.lower()

            if not any(keyword in title_lower for keyword in KEYWORDS):
                continue

            if url in seen_urls:
                continue

            seen_urls.add(url)

            results.append({
                "title": title,
                "url": url
            })

        return results[:15]

    except Exception as error:
        print("Collector error:", error)
        return []


if __name__ == "__main__":
    news = get_education_news()

    for item in news:
        print(item["title"])
        print(item["url"])
        print("-" * 40)