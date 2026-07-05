from scraper import fetch_articles
from markdown import save_article
from uploader import upload_article
from uploader import init_knowledge_base


def main():

    print("Fetching articles...")

    articles = fetch_articles()

    print(f"Found {len(articles)} articles.")
    print("\n--------------------------------------------")

    added = 0
    updated = 0
    skipped = 0

    for article in articles:

        filepath = save_article(article)

        status = upload_article(article, filepath)

        if status == "added":
            added += 1

        elif status == "updated":
            updated += 1

        elif status == "skipped":
            skipped += 1

    print("\n============== Daily Sync Report ==============")
    print(f"Total Articles : {len(articles)}")
    print(f"Added          : {added}")
    print(f"Updated        : {updated}")
    print(f"Skipped        : {skipped}")
    print("===============================================")


if __name__ == "__main__":
    # Uncomment this line if you need to initialize the knowledge base
    # init_knowledge_base()

    main()