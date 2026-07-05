import mimetypes
mimetypes.add_type("text/plain", ".md")

import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

from markdown import load_metadata, upsert_article_metadata

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
TARGET_STORE_NAME = os.getenv("STORE_ID")
if TARGET_STORE_NAME and not TARGET_STORE_NAME.startswith("fileSearchStores/"):
    TARGET_STORE_NAME = f"fileSearchStores/{TARGET_STORE_NAME}"

client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(api_version="v1beta")
)

# init vector store
def init_knowledge_base():
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY is missing in your .env file!")

    init_client = genai.Client(
        api_key=API_KEY,
        http_options=types.HttpOptions(api_version="v1beta")
    )

    file_search_store = init_client.file_search_stores.create(
        config={'display_name': 'Optibot Knowledge Base'}
    )

    print(file_search_store.name)

def upload_article(article, filepath, previous_record=None):
    metadata = load_metadata()
    article_id = str(article["id"])

    if not TARGET_STORE_NAME:
        print("✗ Error: Knowledge base store is not initialized.")
        return "failed"

    current_record = metadata.get(article_id, {})
    if current_record.get("updated_at") == article["updated_at"] and current_record.get("embedded_rag"):
        print(f"✓ Skip (Already in store): {article['title']}")
        return "skipped"

    status = "added" if not previous_record else "updated"

    print(f"Uploading and embedding: {article['title']}...")

    try:
        # Sử dụng hàm chuẩn nhất để đẩy file thẳng vào kho vector, tự động băm (auto-chunking)
        upload_op = client.file_search_stores.upload_to_file_search_store(
            file_search_store_name=TARGET_STORE_NAME,
            file=filepath,
            config=types.UploadToFileSearchStoreConfig(
                display_name=os.path.basename(filepath),
            )
        )

        while not (upload_op := client.operations.get(upload_op)).done:
            time.sleep(1)

        upsert_article_metadata(article, filepath, embedded_rag=True)
        print(f"   -> ✓ Successfully embedded!")
        return status

    except Exception as e:
        print(f"   -> ✗ Error uploading file: {e}")
        return "failed"