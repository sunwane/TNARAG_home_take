import os
import re
import html2text

converter = html2text.HTML2Text()

converter.ignore_links = False
converter.ignore_images = False


def slugify(title):
    title = title.lower()
    title = re.sub(r'[^a-z0-9]+', '-', title)
    return title.strip('-')


def save_article(article):

    markdown = converter.handle(article["body"])

    content = f"""# {article["title"]}

Article URL:
{article["html_url"]}

Last Updated:
{article["updated_at"]}

---

{markdown}
"""

    os.makedirs("output", exist_ok=True)

    filename = slugify(article["title"]) + ".md"

    with open(
        os.path.join("output", filename),
        "w",
        encoding="utf-8"
    ) as f:
        f.write(content)