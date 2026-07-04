import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Initialize the Gemini Client
client = genai.Client()

# Fetch your existing File Search Store ID from environment variables
STORE_ID = os.getenv("STORE_ID")
if not STORE_ID:
    raise ValueError("STORE_ID is missing in your .env file!")

if not STORE_ID.startswith("fileSearchStores/"):
    STORE_ID = f"fileSearchStores/{STORE_ID}"

# Configure the File Search Tool bound to your specific store
file_search_tool = {
    "file_search": {
        "file_search_store_names": [STORE_ID]
    }
}

# System prompt verbatim from the requirements
SYSTEM_PROMPT = """You are OptiBot, the customer-support bot for OptiSigns.com.
• Tone: helpful, factual, concise.
• Only answer using the uploaded docs.
• Max 5 bullet points; else link to the doc.
• Cite up to 3 "Article URL:" lines per reply."""

def main():
    print("====================================================")
    print("🤖 OptiBot CLI Assistant Initialized Successfully!")
    print("👉 Type your question and press Enter.")
    print("👉 Type 'exit' or 'quit' to close the assistant.")
    print("====================================================\n")

    while True:
        question = input("👤 Ask OptiBot: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("Goodbye! Exiting OptiBot.")
            break

        if not question:
            continue

        print("\nThinking and searching internal docs...\n")

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=question,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    tools=[file_search_tool],
                    temperature=0.0
                )
            )

            print("--- OptiBot Response ---")
            print(response.text)
            print("------------------------\n")

            metadata = response.candidates[0].grounding_metadata
            if metadata and metadata.grounding_chunks:
                print("--- Grounding Metadata (Citations) ---")
                print(f"Sources Used: {len(metadata.grounding_chunks)} chunk(s)")

                file_counters = {}
                for index, chunk in enumerate(metadata.grounding_chunks, 1):
                    source_title = "Unknown Source"

                    if hasattr(chunk, 'retrieved_context') and chunk.retrieved_context:
                        source_title = getattr(chunk.retrieved_context, 'title', "Uploaded Doc Chunk")
                    elif isinstance(chunk, dict) and "retrieved_context" in chunk:
                        source_title = chunk["retrieved_context"].get("title", "Uploaded Doc Chunk")

                    if source_title not in file_counters:
                        file_counters[source_title] = 1
                    else:
                        file_counters[source_title] += 1

                    chunk_number = file_counters[source_title]
                    print(f" [{index}] {source_title} [{chunk_number}]")
                print("--------------------------------------\n")
            else:
                print("--- Grounding Metadata --- \nNo grounding metadata returned.\n")

        except Exception as e:
            print(f"✗ Error generating content: {e}\n")


if __name__ == "__main__":
    main()