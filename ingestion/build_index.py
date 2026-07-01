import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CATALOG_PATH = BASE_DIR / "data" / "shl_product_catalog.json"
VECTORSTORE_PATH = BASE_DIR / "vectorstore"


# ============================================================
# Load Catalog
# ============================================================

print("Loading SHL Product Catalog...")

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

print(f"Loaded {len(catalog)} assessments.")


# ============================================================
# Create Documents
# ============================================================

documents = []

for item in catalog:

    job_levels = ", ".join(item.get("job_levels", []))
    languages = ", ".join(item.get("languages", []))
    categories = ", ".join(item.get("keys", []))

    searchable_text = f"""
This is an SHL assessment used for hiring, candidate evaluation, talent assessment,
employee selection and recruitment.

Assessment Name:
{item.get("name","")}

Description:
{item.get("description","")}

Suitable Job Levels:
{job_levels}

Assessment Categories:
{categories}

Supported Languages:
{languages}

Duration:
{item.get("duration","")}

Remote Testing:
{item.get("remote","")}

Adaptive Assessment:
{item.get("adaptive","")}
"""

    metadata = {

        "entity_id": item.get("entity_id"),

        "name": item.get("name"),

        "url": item.get("link"),

        "keys": item.get("keys", []),

        "job_levels": item.get("job_levels", []),

        "languages": item.get("languages", []),

        "duration": item.get("duration", ""),

        "remote": item.get("remote", ""),

        "adaptive": item.get("adaptive", ""),
        
        "original_description": item.get("description","")
        
    }

    documents.append(
        Document(
            page_content=searchable_text.strip(),
            metadata=metadata
        )
    )


print(f"Created {len(documents)} documents.")


# ============================================================
# Embedding Model
# ============================================================

print("Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ============================================================
# Build FAISS
# ============================================================

print("Building FAISS index...")

vectorstore = FAISS.from_documents(
    documents,
    embeddings
)


# ============================================================
# Save
# ============================================================

VECTORSTORE_PATH.mkdir(exist_ok=True)

vectorstore.save_local(str(VECTORSTORE_PATH))

print("Vectorstore saved successfully!")