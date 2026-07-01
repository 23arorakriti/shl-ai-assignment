import os
import requests
import streamlit as st

# ==========================================================
# Configuration
# ==========================================================

API_URL = os.getenv(
    "API_URL",
    # "http://127.0.0.1:8000/chat",
    "https://panda0987-shl-project.hf.space/docs#/default/health_health_get",
)

st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🧠",
    layout="wide",
)

# ==========================================================
# Session State
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.title("🧠 SHL AI Assistant")

    st.markdown("### Example Queries")

    st.markdown("""
- Hiring a Java Backend Developer with 5 years experience.
- Graduate Software Engineer.
- Data Analyst with SQL and Python.
- Compare Docker and AWS assessments.
- Recommend leadership assessments for managers.
""")

    if st.button("🗑 Clear Conversation"):

        st.session_state.messages = []
        st.session_state.recommendations = []

        st.rerun()

# ==========================================================
# Header
# ==========================================================

st.title("🧠 SHL Assessment Recommendation System")

st.caption(
    "Describe your hiring requirements and receive the most suitable SHL assessments."
)

# ==========================================================
# Conversation
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ==========================================================
# Chat Input
# ==========================================================

prompt = st.chat_input(
    "Describe your hiring requirement..."
)

if prompt:

    # -------------------------
    # Show user message
    # -------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    payload = {
        "messages": st.session_state.messages
    }

    # -------------------------
    # Backend
    # -------------------------

    with st.spinner("Finding suitable SHL assessments..."):

        try:

            response = requests.post(
                API_URL,
                json=payload,
                timeout=60,
            )

            response.raise_for_status()

            result = response.json()

        except Exception as e:

            st.error(f"Backend Error:\n\n{e}")
            st.stop()

    # -------------------------
    # Assistant
    # -------------------------

    reply = result["reply"]

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply,
        }
    )

    st.session_state.recommendations = result.get(
        "recommendations",
        [],
    )

    with st.chat_message("assistant"):
        st.markdown(reply)

# ==========================================================
# Recommendation Cards
# ==========================================================

if st.session_state.recommendations:

    st.divider()

    st.subheader("📋 Recommended SHL Assessments")

    cols = st.columns(2)

    for i, rec in enumerate(st.session_state.recommendations):

        with cols[i % 2]:

            with st.container(border=True):

                st.markdown(f"### {rec['name']}")

                st.caption(rec["test_type"])

                st.link_button(
                    "🔗 View Assessment",
                    rec["url"],
                    use_container_width=True,
                )