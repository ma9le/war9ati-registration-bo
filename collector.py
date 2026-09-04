import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.education.gov.dz/"

KEYWORDS = [
    "مسابقة", "مسابقات", "توظيف", "التوظيف",
    "تسجيل", "التسجيل", "إعلان", "إعلانات",
    "بلاغ", "مترشحين", "المترشحين", "نتائج"
]

EXCLUDE = [
    "الفهرس", "مواقع مفيدة", "التلفزة",
    "الوزير", "صلاحيات", "اتصل بنا",
    "الرئيسية", "القانون التوجيهي", "النشرة الرسمية"
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
        seen = set()

        for link in soup.find_all("a", href=True):
            title = link.get_text(" ", strip=True)
            url = urljoin(BASE_URL, link["href"])

            if not title or url in seen:
                continue

            if any(word in title for word in EXCLUDE):
                continue

            if any(word in title for word in KEYWORDS):
                seen.add(url)
                results.append({
                    "title": title,
                    "url": url
                })

        return results[:15]

    except Exception as e:
        print("Collector error:", e)
        return []