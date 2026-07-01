import os
from pathlib import Path
from dotenv import load_dotenv

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

# ==========================================================
# Base Directory
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

# ==========================================================
# Gemini Configuration
# ==========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-2.5-flash"

# ==========================================================
# Project Paths
# ==========================================================

VECTORSTORE_PATH = BASE_DIR / "vectorstore"

PROMPT_PATH = BASE_DIR / "prompts" / "system_prompt.txt"

CATALOG_PATH = BASE_DIR / "data" / "shl_product_catalog.json"

# ==========================================================
# Retrieval Configuration
# ==========================================================

TOP_K = 5

FETCH_K = 20

MMR_LAMBDA = 0.7

# ==========================================================
# Conversation Configuration
# ==========================================================

MAX_CONTEXT_ASSESSMENTS = 5

MAX_CONVERSATION_MESSAGES = 20

# ==========================================================
# Security
# ==========================================================

ENABLE_PROMPT_INJECTION_PROTECTION = True

ENABLE_OUT_OF_SCOPE_PROTECTION = True

ENABLE_RULE_ENGINE = True

# ==========================================================
# Development
# ==========================================================

DEBUG = True

# Runs startup checks (recommended during development)
STARTUP_SELF_TEST = True

# If True, prints available Gemini models once.
PRINT_AVAILABLE_MODELS = False