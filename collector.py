import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

ARCHIVE_URL = "https://www.education.gov.dz/category/منشورات-وبيانات/"

KEYWORDS = [
    "مسابقة",
    "مسابقات",
    "توظيف",
    "التوظيف",
    "تسجيل",
    "التسجيل",
    "إعلان",
    "إعلانات",
    "بلاغ",
    "مترشحين",
    "المترشحين",
    "نتائج",
]


def get_education_news():
    try:
        response = requests.get(
            ARCHIVE_URL,
            timeout=(10, 60),
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        seen = set()

        # البحث عن روابط المقالات
        for link in soup.find_all("a", href=True):

            title = link.get_text(" ", strip=True)
            url = urljoin(ARCHIVE_URL, link["href"])

            if not title:
                continue

            if url in seen:
                continue

            # نتأكد أن العنوان مرتبط بالتسجيلات/المسابقات/الإعلانات
            if any(keyword in title for keyword in KEYWORDS):

                seen.add(url)

                results.append({
                    "title": title,
                    "url": url
                })

        return results[:15]

    except requests.exceptions.Timeout:
        print("ERROR: Ministry website timed out")
        return []

    except requests.exceptions.RequestException as e:
        print("ERROR: Request failed:", e)
        return []

    except Exception as e:
        print("ERROR:", e)
        return []