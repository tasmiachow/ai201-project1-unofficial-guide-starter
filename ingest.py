import os
import re
from config import DOCS_PATH

def load_documents():
    """Load all normalized .md park documents from the docs folder and parse metadata headers."""
    documents = []
    
    # Ensure the path exists
    if not os.path.exists(DOCS_PATH):
        print(f"Error: Path '{DOCS_PATH}' does not exist.")
        return []

    # Read through documents directory
    for filename in sorted(os.listdir(DOCS_PATH)):
        if filename.endswith(".md"):
            filepath = os.path.join(DOCS_PATH, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            # Base metadata fallbacks in case a header has a minor typo
            metadata = {
                "source": filename.replace(".md", "").replace("_", " ").title(),
                "url": "Unknown URL",
                "target_park": "Unknown Park",
                "filename": filename,
                "text": text
            }

            # Extract normalized header values using regex
            source_match = re.search(r"^#\s*Source:\s*(.*)$", text, re.MULTILINE)
            url_match = re.search(r"^#\s*URL:\s*(.*)$", text, re.MULTILINE)
            target_match = re.search(r"^#\s*Target Park:\s*(.*)$", text, re.MULTILINE)

            if source_match:
                metadata["source"] = source_match.group(1).strip()
            if url_match:
                metadata["url"] = url_match.group(1).strip()
            if target_match:
                metadata["target_park"] = target_match.group(1).strip()

            # Clean out the raw metadata lines from the body text so they don't pollute your embeddings
            clean_text = re.sub(r"^#\s*(Source|URL|Target Park):.*$", "", text, flags=re.MULTILINE).strip()
            metadata["text"] = clean_text

            documents.append(metadata)

    print(f"Loaded {len(documents)} document(s): {[d['target_park'] for d in documents]}")
    return documents

def chunk_document(doc_dict):
    """
    Split a rule document into chunks ready for embedding.

    This function is already implemented — read through it and the inline
    comments before moving on. The decisions made here directly shape what
    retrieval returns in Milestones 2 and 3, so it's worth understanding
    before you build on top of it.

    Strategy: character-based sliding window with overlap.
      - chunk_size = 300 characters: long enough to carry the semantic
        meaning of a single rule, short enough to return targeted results
      - overlap = 50 characters: duplicates a small window of text at each
        boundary so a rule that spans two chunks can still be retrieved intact
      - min_length = 50 characters: filters out whitespace artifacts and
        very short fragments that add noise without useful semantic content

    Returns a list of dicts, each with:
      - "text"     : the chunk text (str)
      - "game"     : the game name, e.g. "Catan" (str)
      - "chunk_id" : a unique identifier, e.g. "catan_0", "catan_1" (str)
    """
    chunk_size = 1200
    overlap = 200
    min_length = 200

    chunks = []
    text = doc_dict["text"]
    park_name = doc_dict["target_park"]

    prefix = doc_dict["source"].lower().replace(" ", "_").replace(":", "").replace("-", "")
    counter = 0

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end].strip()

        if len(chunk_text) >= min_length:
            chunks.append({
                "text": chunk_text,
                "park": park_name,
                "source": doc_dict["source"],
                "url": doc_dict["url"],
                "chunk_id": f"{prefix}_{counter}",
            })
            counter += 1

        # Advance by (chunk_size - overlap) so the next chunk shares
        # `overlap` characters with the tail of this one.
        start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    print("🚀 Starting ingestion pipeline...")
    
    # 1. Load the documents
    docs = load_documents()
    
    # 2. Track total chunks generated
    total_chunks = 0
    
    # 3. Loop through and chunk them to test the output
    for doc in docs:
        chunks = chunk_document(doc)
        total_chunks += len(chunks)
        print(f"   ↳ Split '{doc['source']}' into {len(chunks)} chunks.")
        
    print(f"\n✅ Success! Total files processed: {len(docs)}")
    print(f"📦 Total database chunks generated: {total_chunks}")