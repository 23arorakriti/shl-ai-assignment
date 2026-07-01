from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from config import DEBUG


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
VECTORSTORE_PATH = BASE_DIR / "vectorstore"


# ============================================================
# Embeddings
# ============================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ============================================================
# Load FAISS
# ============================================================

vectorstore = FAISS.load_local(
    str(VECTORSTORE_PATH),
    embeddings,
    allow_dangerous_deserialization=True,
)


# ============================================================
# Skill Keywords
# ============================================================

TECH_KEYWORDS = [
    "java",
    "python",
    "aws",
    "docker",
    "spring",
    "spring boot",
    "sql",
    "react",
    "angular",
    "node",
    "kubernetes",
    "azure",
    "gcp",
    ".net",
    "javascript",
]


# ============================================================
# Retrieve Assessments
# ============================================================

def retrieve_assessments(
    query: str,
    language: str | None = None,
    job_level: str | None = None,
    top_k: int = 5,
):

    docs = vectorstore.max_marginal_relevance_search(
        query=query,
        k=15,
        fetch_k=50,
        lambda_mult=0.75,
    )

    query_lower = query.lower()

    ranked = []
    seen = set()

    for doc in docs:

        meta = doc.metadata

        name = meta.get("name", "")

        if name in seen:
            continue

        seen.add(name)

        languages = meta.get("languages", [])
        job_levels = meta.get("job_levels", [])
        keys = meta.get("keys", [])

        if language and language not in languages:
            continue

        if job_level and job_level not in job_levels:
            continue

        score = 0

        page = doc.page_content.lower()

        # Technical skill matching
        for skill in TECH_KEYWORDS:
            if skill in query_lower and skill in page:
                score += 3

        # Prefer technical assessments
        if "Knowledge & Skills" in keys:
            score += 3

        # Match job level
        if job_level and job_level in job_levels:
            score += 2

        # Match language
        if language and language in languages:
            score += 1

        # Exact role match bonus
        if any(word in page for word in query_lower.split()):
            score += 2

        context = f"""
Assessment Name:
{name}

Description:
{meta.get("original_description", "")}

Categories:
{", ".join(keys)}

Job Levels:
{", ".join(job_levels)}

Languages:
{", ".join(languages)}

Duration:
{meta.get("duration", "")}

Remote:
{meta.get("remote", "")}

Adaptive:
{meta.get("adaptive", "")}

URL:
{meta.get("url", "")}

---------------------------------------------------------
"""

        recommendation = {
            "name": name,
            "url": meta.get("url", ""),
            "test_type": ", ".join(keys),
        }

        ranked.append((score, context, recommendation))

    ranked.sort(
        key=lambda x: x[0],
        reverse=True,
    )

    context = ""
    recommendations = []

    for _, ctx, rec in ranked[:top_k]:
        context += ctx
        recommendations.append(rec)

    if DEBUG:

        print("\n" + "=" * 70)
        print("Retriever Query")
        print("=" * 70)
        print(query)

        print("\nTop Recommendations\n")

        for rec in recommendations:
            print(f"- {rec['name']}")

        print("=" * 70)

    return context, recommendations


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    context, recommendations = retrieve_assessments(
        query="Senior Java Backend Developer with Spring Boot SQL Docker AWS",
        top_k=5,
    )

    print(context)

    print("\nReturned Recommendations\n")

    for item in recommendations:
        print(item)