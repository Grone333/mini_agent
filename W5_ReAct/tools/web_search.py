import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Union


def web_search(query: str, max_results: int = 5, timeout: int = 10) -> Union[List[Dict], str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    url = "https://www.baidu.com/s"
    params = {"wd": query}

    results = []
    try:
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("div.result.c-container")

        for item in items[:max_results]:
            title_tag = item.select_one("h3 a")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href")
            summary_tag = item.select_one("div.c-abstract")
            summary = summary_tag.get_text(strip=True) if summary_tag else ""
            results.append({"title": title, "link": link, "summary": summary})

    except requests.exceptions.RequestException as e:

        return f"网络请求异常: {e}"
    return results
          
