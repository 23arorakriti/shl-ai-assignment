from pathlib import Path

import google.generativeai as genai
from fastapi import FastAPI, HTTPException

from config import *
from models import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
)
from retrieval.retriever import retrieve_assessments
from utils.rules import (
    is_greeting,
    is_out_of_scope,
    is_prompt_injection,
    extract_information,
    get_clarification_question,
    build_search_query,
    end_conversation,
)

# ==========================================================
# FastAPI
# ==========================================================

app = FastAPI(
    title="SHL Assessment Recommendation API",
    version="1.0.0",
    description="AI-powered SHL Assessment Recommendation System",
)

# ==========================================================
# Load System Prompt
# ==========================================================

try:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    raise RuntimeError("system_prompt.txt not found.")

# ==========================================================
# Gemini Configuration
# ==========================================================

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)

# ==========================================================
# Startup Checks
# ==========================================================

if STARTUP_SELF_TEST:

    print("=" * 60)
    print("Starting SHL Assessment Recommendation API")
    print("=" * 60)

    print("Checking configuration...")

    if GEMINI_API_KEY:
        print("✅ Gemini API Key Loaded")
    else:
        print("❌ Gemini API Key Missing")

    if PROMPT_PATH.exists():
        print("✅ Prompt File Found")
    else:
        print("❌ Prompt File Missing")

    if VECTORSTORE_PATH.exists():
        print("✅ Vector Store Found")
    else:
        print("❌ Vector Store Missing")

    try:
        response = model.generate_content(
            "Reply only with OK."
        )

        if "OK" in response.text.upper():
            print(f"✅ Gemini Connected ({MODEL_NAME})")
        else:
            print("⚠ Gemini responded unexpectedly")

    except Exception as e:
        print("❌ Gemini Connection Failed")
        print(e)

    if PRINT_AVAILABLE_MODELS:

        print("\nAvailable Models:\n")

        for m in genai.list_models():

            if "generateContent" in m.supported_generation_methods:
                print(m.name)

    print("=" * 60)
    print("Startup Complete")
    print("=" * 60)

# ==========================================================
# Health Endpoint
# ==========================================================

@app.get(
    "/health",
    response_model=HealthResponse
)
def health():

    return HealthResponse(status="ok")
# ==========================================================
# Chat Endpoint
# ==========================================================

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    if not request.messages:
        raise HTTPException(
                status_code=400,
                detail="No conversation messages provided."
        )

    # --------------------------------------------------
    # Last User Message
    # --------------------------------------------------

    last_user_message = next(
        (
            msg.content
            for msg in reversed(request.messages)
            if msg.role == "user"
        ),
        "",
    )

    if not last_user_message:
        raise HTTPException(
            status_code=400,
            detail="User message not found."
        )

    # --------------------------------------------------
    # Greeting
    # --------------------------------------------------

    if is_greeting(last_user_message):

        return ChatResponse(
            reply="Hello! I'm here to help you find the most suitable SHL assessments. What role are you hiring for?",
            recommendations=[],
            end_of_conversation=False,
        )

    # --------------------------------------------------
    # Prompt Injection
    # --------------------------------------------------

    if (
        ENABLE_PROMPT_INJECTION_PROTECTION
        and is_prompt_injection(last_user_message)
    ):

        return ChatResponse(
            reply="I can't comply with requests that attempt to override my instructions. I can help recommend and explain SHL assessments.",
            recommendations=[],
            end_of_conversation=False,
        )

    # --------------------------------------------------
    # Out Of Scope
    # --------------------------------------------------

    if (
        ENABLE_OUT_OF_SCOPE_PROTECTION
        and is_out_of_scope(last_user_message)
    ):

        return ChatResponse(
            reply="I can only assist with recommending, comparing and explaining SHL assessments.",
            recommendations=[],
            end_of_conversation=False,
        )

    # --------------------------------------------------
    # End Conversation
    # --------------------------------------------------

    if end_conversation(last_user_message):

        return ChatResponse(
            reply="You're welcome! Feel free to reach out whenever you need help selecting SHL assessments.",
            recommendations=[],
            end_of_conversation=True,
        )

    # --------------------------------------------------
    # Extract Conversation Information
    # --------------------------------------------------

    info = extract_information(
        [message.model_dump() for message in request.messages]
    )

    # --------------------------------------------------
    # Clarification
    # --------------------------------------------------

    clarification = get_clarification_question(info)

    if clarification:

        return ChatResponse(
            reply=clarification,
            recommendations=[],
            end_of_conversation=False,
        )

    # --------------------------------------------------
    # Build Search Query
    # --------------------------------------------------

    search_query = build_search_query(info)

    if DEBUG:
        print(f"\nSearch Query: {search_query}")

    # --------------------------------------------------
    # Retrieve Assessments
    # --------------------------------------------------

    context, recommendations = retrieve_assessments(
    query=search_query,
    language=info.get("language"),
    job_level=info.get("job_level"),
    top_k=TOP_K,
)

    if DEBUG:
        print(f"Retrieved {len(recommendations)} assessments.")
            # --------------------------------------------------
        # No Matching Assessments
        # --------------------------------------------------

        if not recommendations:

            return ChatResponse(
                reply="I couldn't find any suitable SHL assessments matching your requirements.",
                recommendations=[],
                end_of_conversation=False,
            )

        # --------------------------------------------------
        # Build Conversation History
        # --------------------------------------------------

        conversation = "\n".join(
            f"{msg.role.capitalize()}: {msg.content}"
            for msg in request.messages
        )

        # --------------------------------------------------
        # Final Prompt
        # --------------------------------------------------

        final_prompt = f"""
{SYSTEM_PROMPT}

==================================================
Conversation
==================================================

{conversation}

==================================================
Retrieved SHL Assessments
==================================================

{context}

==================================================
Instructions
==================================================

1. Recommend ONLY from the retrieved assessments.
2. Never invent assessment names.
3. Never invent URLs.
4. Explain WHY each recommendation fits.
5. If comparing assessments, compare ONLY retrieved assessments.
6. If insufficient information exists, politely say so.
7. Keep the answer concise and recruiter-friendly.
"""

        if DEBUG:
            print("\nSending prompt to Gemini...\n")

        # --------------------------------------------------
        # Gemini Call
        # --------------------------------------------------

        try:

            response = model.generate_content(final_prompt)

            reply = response.text.strip()

            if not reply:
                reply = (
                    "I couldn't generate a recommendation at the moment."
                )
        except Exception as e:

            if DEBUG:
                print(f"\nGemini Error: {e}")

            raise HTTPException(
                status_code=500,
                detail="Failed to generate recommendation from Gemini."
            )

        # --------------------------------------------------
        # Return Response
        # --------------------------------------------------

        return ChatResponse(
            reply=reply,
            recommendations=recommendations,
            end_of_conversation=False
        )


# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/")
def root():

    return {
        "message": "SHL Assessment Recommendation API",
        "status": "running",
        "version": "1.0.0"
    }


# ==========================================================
# Run Locally
# ==========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )