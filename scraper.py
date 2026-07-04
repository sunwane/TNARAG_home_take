import requests

BASE_URL = "https://optisignshelp.zendesk.com/api/v2/help_center/en-us/articles"

def fetch_articles():
    articles = []
    url = BASE_URL

    while url:
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code}")

        data = response.json()

        articles.extend(data["articles"])
        url = data["next_page"]
        #print(f"Fetched {len(data['articles'])} articles, next page: {url}")

    return articles