import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from app.graph import graph


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="EduQuery | AI College Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Main application */
.stApp {
    background: #0b1020;
    color: #e5e7eb;
}

/* Remove default top spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1150px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #263247;
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

/* Sidebar text */
.sidebar-brand {
    font-size: 27px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1px;
}

.sidebar-subtitle {
    color: #94a3b8;
    font-size: 13px;
    margin-top: -5px;
}

.sidebar-label {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 30px;
    margin-bottom: 10px;
}

/* Hero section */
.hero {
    background: linear-gradient(135deg, #172554 0%, #312e81 55%, #4338ca 100%);
    border: 1px solid #4f46e5;
    border-radius: 22px;
    padding: 38px;
    margin-bottom: 30px;
    box-shadow: 0 15px 50px rgba(30, 41, 100, 0.25);
}

.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 6px 12px;
    border-radius: 30px;
    font-size: 12px;
    color: #c7d2fe;
    margin-bottom: 15px;
}

.hero h1 {
    color: #ffffff;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1.5px;
    margin: 0;
}

.hero p {
    color: #c7d2fe;
    font-size: 15px;
    line-height: 1.7;
    max-width: 650px;
    margin-top: 12px;
}

/* Section headings */
.section-heading {
    font-size: 19px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 5px;
}

.section-description {
    color: #94a3b8;
    font-size: 13px;
    margin-bottom: 18px;
}

/* Suggestion cards */
div.stButton > button {
    border: 1px solid #334155;
    background: #151e30;
    color: #e2e8f0;
    border-radius: 12px;
    padding: 13px 16px;
    min-height: 55px;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    border-color: #818cf8;
    background: #202b45;
    color: #ffffff;
}

/* Primary buttons */
div.stButton > button[kind="primary"] {
    background: #4f46e5;
    border: 1px solid #6366f1;
    color: white;
}

/* Chat messages */
div[data-testid="stChatMessage"] {
    background: #141d2e;
    border: 1px solid #273449;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 14px;
}

/* Chat input */
div[data-testid="stChatInput"] {
    border: 1px solid #334155;
    border-radius: 16px;
    background: #151e30;
}

/* Select box */
div[data-baseweb="select"] > div {
    background: #172033;
    border-color: #334155;
    border-radius: 10px;
}

/* Divider */
hr {
    border-color: #263247;
}

/* Status panel */
.status-panel {
    background: #172033;
    border: 1px solid #29364b;
    border-radius: 12px;
    padding: 13px;
    margin-top: 15px;
}

.status-dot {
    color: #4ade80;
    font-size: 12px;
}

.status-text {
    color: #cbd5e1;
    font-size: 12px;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding: 25px 0 5px 0;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">🎓 EduQuery</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">Your AI-powered college assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-label">Student Profile</div>',
        unsafe_allow_html=True
    )

    program = st.selectbox(
        "Select your academic program",
        ["BSCS", "BBA", "B.Com (H)"],
        label_visibility="collapsed"
    )

    st.markdown(
        '<div class="sidebar-label">Workspace</div>',
        unsafe_allow_html=True
    )

    if st.button("＋  New Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-label">About EduQuery</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div style="color:#94a3b8; font-size:13px; line-height:1.8;">
        EduQuery helps students find accurate information from official
        academic handbooks and fee documents.
        <br><br>
        <span style="color:#c7d2fe;">✦ Academic information</span><br>
        <span style="color:#c7d2fe;">✦ Fee structure</span><br>
        <span style="color:#c7d2fe;">✦ General assistance</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class="status-panel">
        <span class="status-dot">●</span>
        <span class="status-text"> AI Assistant Ready</span>
        <br><br>
        <span class="status-text">Powered by LangGraph + Groq</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="footer">EduQuery · AI College Assistant</div>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ YOUR SMART ACADEMIC COMPANION</div>
    <h1>Ask. Explore. Understand.</h1>
    <p>
        Get answers about academic policies, examination rules,
        attendance, fee structures and more — powered by your
        college documents.
    </p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# WELCOME SCREEN
# --------------------------------------------------

if not st.session_state.chat_history:

    st.markdown(
        '<div class="section-heading">What would you like to know?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Choose a suggested question or type your own below.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "📚  Academic & Attendance Rules",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "What are the academic and attendance requirements?"
            )

        if st.button(
            "📝  Examination & Grading Policy",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Explain the examination and grading policy."
            )

    with col2:
        if st.button(
            "💳  Fee Structure & Payments",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                f"What is the fee structure for {program}?"
            )

        if st.button(
            "🎓  Degree Requirements",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "What are the degree completion requirements?"
            )

    st.markdown("---")


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for chat in st.session_state.chat_history:

    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_query = st.chat_input(
    "Ask anything about academics, fees or college policies..."
)

if st.session_state.pending_prompt:
    user_query = st.session_state.pending_prompt
    st.session_state.pending_prompt = None


# --------------------------------------------------
# LANGGRAPH EXECUTION
# --------------------------------------------------

if user_query:

    # Display user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user"):
        st.markdown(user_query)

    # Convert chat history into LangChain messages
    conversation = []

    for chat in st.session_state.chat_history[:-1]:
        if chat["role"] == "user":
            conversation.append(
                HumanMessage(content=chat["content"])
            )
        else:
            conversation.append(
                AIMessage(content=chat["content"])
            )

    # Add current question
    conversation.append(
        HumanMessage(content=user_query)
    )

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("EduQuery is analyzing your question..."):

            try:

                result = graph.invoke({
                    "program": program,
                    "messages": conversation,
                    "query_type": "",
                    "retrieved_context": ""
                })

                answer = result["messages"][-1].content

                st.markdown(answer)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:

                st.error(
                    "Something went wrong while generating your answer."
                )

                with st.expander("View technical error"):
                    st.code(str(error))

    st.rerun()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    EduQuery AI · Academic Knowledge Assistant
    <br>
    Always verify important academic decisions with official college documents.
</div>
""", unsafe_allow_html=True)