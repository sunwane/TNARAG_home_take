from scraper import fetch_articles
from markdown import save_article
from uploader import upload_article
from uploader import init_knowledge_base

def main():
    print("Fetching articles...")
    articles = fetch_articles()

    print(f"Found {len(articles)} articles.")
    print("\n--------------------------------------------")

    for article in articles:

        filepath = save_article(article)

        upload_article(article, filepath)

    print("\nDone!")

if __name__ == "__main__":
    # Uncomment this line if you need to initialize the knowledge base
    # init_knowledge_base() 

    main()