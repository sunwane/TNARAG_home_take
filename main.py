from scraper import fetch_articles
from markdown import save_article

articles = fetch_articles()

print(f"Found {len(articles)} articles")

for article in articles:
    save_article(article)

print("Done!")