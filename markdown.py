import json
import os
import re

import html2text

converter = html2text.HTML2Text()

converter.ignore_links = False
converter.ignore_images = False
converter.body_width = 0
converter.ignore_tables = False

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
METADATA_FILE = os.getenv("METADATA_FILE", "metadata.json")

def slugify(title):
    title = title.lower()
    title = re.sub(r'[^a-z0-9]+', '-', title)
    return title.strip('-')


def load_metadata():
    if not os.path.exists(METADATA_FILE):
        return {}

    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as file_handle:
            return json.load(file_handle)
    except (json.JSONDecodeError, OSError):
        return {}


def save_metadata(metadata):
    metadata_dir = os.path.dirname(METADATA_FILE)
    if metadata_dir:
        os.makedirs(metadata_dir, exist_ok=True)

    with open(METADATA_FILE, "w", encoding="utf-8") as file_handle:
        json.dump(metadata, file_handle, indent=4, ensure_ascii=False)


def upsert_article_metadata(article, filepath, embedded_rag=False):
    metadata = load_metadata()
    article_id = str(article["id"])

    metadata[article_id] = {
        "title": article["title"],
        "filename": os.path.basename(filepath),
        "updated_at": article["updated_at"],
        "article_url": article["html_url"],
        "embedded_rag": embedded_rag,
    }

    save_metadata(metadata)


def save_article(article):
    markdown = converter.handle(article["body"])
    metadata = load_metadata()
    article_id = str(article["id"])
    current_record = metadata.get(article_id, {})
    embedded_rag = current_record.get("embedded_rag", False) if current_record.get("updated_at") == article["updated_at"] else False

    content = f"""# {article["title"]}

Article URL:
{article["html_url"]}

Last Updated:
{article["updated_at"]}

---

{markdown}
"""

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filename = slugify(article["title"]) + ".md"

    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as file_handle:
        file_handle.write(content)

    upsert_article_metadata(article, filepath, embedded_rag=embedded_rag)

    return filepath