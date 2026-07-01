import re
from typing import Dict, List


# ==========================================================
# Greeting Detection
# ==========================================================

GREETINGS = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
}


def is_greeting(text: str) -> bool:
    return text.lower().strip() in GREETINGS


# ==========================================================
# Prompt Injection Detection
# ==========================================================

PROMPT_INJECTION_PATTERNS = [

    "ignore previous",

    "ignore all previous",

    "forget previous",

    "forget all previous",

    "system prompt",

    "developer prompt",

    "hidden prompt",

    "reveal prompt",

    "show prompt",

    "show instructions",

    "act as",

    "pretend",

    "override",

    "jailbreak",

    "bypass",

]


def is_prompt_injection(text: str) -> bool:

    text = text.lower()

    return any(pattern in text for pattern in PROMPT_INJECTION_PATTERNS)


# ==========================================================
# Out of Scope Detection
# ==========================================================

OUT_OF_SCOPE = [

    "politics",

    "president",

    "prime minister",

    "medical",

    "doctor",

    "hospital",

    "covid",

    "recipe",

    "movie",

    "cricket",

    "football",

    "ipl",

    "weather",

    "capital of",

    "resume",

    "cv",

    "cover letter",

    "salary",

    "leetcode",

    "python code",

]


def is_out_of_scope(text: str):

    text = text.lower()

    return any(keyword in text for keyword in OUT_OF_SCOPE)


# ==========================================================
# Conversation -> Single String
# ==========================================================

def conversation_to_text(messages: List[Dict]) -> str:

    return "\n".join(
        f"{m['role'].capitalize()}: {m['content']}"
        for m in messages
    )


# ==========================================================
# Extract Hiring Information
# ==========================================================

ROLE_PATTERN = re.compile(
    r"(java developer|python developer|backend developer|frontend developer|"
    r"software engineer|data engineer|data scientist|"
    r"developer|engineer|manager|analyst|consultant|architect|"
    r"sales manager|tester|qa engineer|administrator)",
    re.IGNORECASE,
)

EXPERIENCE_PATTERN = re.compile(
    r"(\d+)\s*(year|years|yr|yrs)",
    re.IGNORECASE,
)

LANGUAGE_PATTERN = re.compile(
    r"(english|spanish|german|french|arabic|japanese|chinese|portuguese)",
    re.IGNORECASE,
)

# ==========================================================
# Technical Skills
# ==========================================================

TECH_SKILLS = [
    "java",
    "python",
    "c++",
    "c#",
    ".net",
    "spring",
    "spring boot",
    "hibernate",
    "react",
    "angular",
    "node",
    "nodejs",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "sql",
    "mysql",
    "postgresql",
    "oracle",
    "mongodb",
    "git",
    "linux",
    "javascript",
]

# ==========================================================
# Job Levels
# ==========================================================

JOB_LEVELS = {
    "graduate": "Graduate",
    "entry": "Entry-Level",
    "entry level": "Entry-Level",
    "junior": "Entry-Level",
    "mid": "Mid-Professional",
    "mid-level": "Mid-Professional",
    "senior": "Mid-Professional",
    "lead": "Manager",
    "manager": "Manager",
    "director": "Director",
    "executive": "Executive",
    "supervisor": "Supervisor",
}

def extract_information(messages: List[Dict]):

    conversation = " ".join(
        msg["content"]
        for msg in messages
        if msg["role"] == "user"
    )

    info = {
    "role": None,
    "experience": None,
    "language": None,
    "job_level": None,
    "skills": [],
    "leadership": False,
    "remote": False,
    "personality": False,
    "ability": False,
    "comparison": False,
    "refinement": False,
}

    role = ROLE_PATTERN.search(conversation)

    if role:
        info["role"] = role.group()

    experience = EXPERIENCE_PATTERN.search(conversation)

    if experience:
        info["experience"] = experience.group()

    language = LANGUAGE_PATTERN.search(conversation)

    if language:
        info["language"] = language.group()

    lower = conversation.lower()
# ----------------------------------------------------------
# Technical Skills
# ----------------------------------------------------------

    for skill in TECH_SKILLS:
        if skill in lower:
            info["skills"].append(skill)

    # Remove duplicates while preserving order
    info["skills"] = list(dict.fromkeys(info["skills"]))

    # ----------------------------------------------------------
    # Job Level
    # ----------------------------------------------------------

    for keyword, level in JOB_LEVELS.items():
        if keyword in lower:
            info["job_level"] = level
            break    
    

    if any(word in lower for word in [
        "manager",
        "leader",
        "leadership",
        "supervisor"
    ]):
        info["leadership"] = True

    if "remote" in lower:
        info["remote"] = True

    if any(word in lower for word in [
        "personality",
        "behavior",
        "opq"
    ]):
        info["personality"] = True

    if any(word in lower for word in [
        "ability",
        "aptitude",
        "reasoning"
    ]):
        info["ability"] = True

    if any(word in lower for word in [
        "compare",
        "difference",
        "vs"
    ]):
        info["comparison"] = True

    if any(word in lower for word in [
        "also",
        "instead",
        "change",
        "update",
        "add"
    ]):
        info["refinement"] = True

    return info


# ==========================================================
# Clarification
# ==========================================================

def get_clarification_question(info):

    if info["role"] is None:
        return "What role are you hiring for?"

    if info["experience"] is None:
        return "What experience level are you looking for?"

    return None


# ==========================================================
# Build Retrieval Query
# ==========================================================

def build_search_query(info):

    query = []

    if info["role"]:
        query.append(info["role"])

    if info["experience"]:
        query.append(info["experience"])

    if info["job_level"]:
        query.append(info["job_level"])

    if info["language"]:
        query.append(info["language"])

    for skill in info["skills"]:
        query.append(skill)

    if info["leadership"]:
        query.append("leadership")

    if info["remote"]:
        query.append("remote")

    if info["personality"]:
        query.append("personality assessment")

    if info["ability"]:
        query.append("ability assessment")

    query.append("SHL assessment")

    return " ".join(query)


# ==========================================================
# End Conversation
# ==========================================================

END_WORDS = [

    "thanks",

    "thank you",

    "looks good",

    "that's all",

    "done",

    "perfect",

    "great",

]


def end_conversation(text):

    text = text.lower()

    return any(word in text for word in END_WORDS)