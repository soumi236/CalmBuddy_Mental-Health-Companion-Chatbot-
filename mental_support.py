import streamlit as st
import ollama
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    

    page_title="Mental Health Support Agent",
    page_icon="🧠",
    layout="centered" 
)
st.markdown("""
    <style>
        header {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# ---------------- BACKGROUND IMAGE ----------------
def get_base64(background_file):
    try:
        with open(background_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

bin_str = get_base64("background.png")

# ---------------- CSS FOR LARGE BLACK TEXT ----------------
st.markdown(f"""
    <style>

        /* Overall Page Background */
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
        }}

        /* ✅ BOX REMOVED */
        .centered-box {{
            background-color: transparent !important;
            padding: 0px !important;
            border: none !important;
            box-shadow: none !important;
        }}

        /* HUGE FONT FOR INPUT */
        .stChatInput textarea {{
            font-size: 26px !important;
            color: #000000 !important;
            font-weight: 500 !important;
        }}

        /* TITLE */
        .box-title {{
            font-size: 50px !important;
            font-weight: 900;
            text-align: center;
            margin-bottom: 10px;
            color: #000000 !important;
        }}

        .box-subtitle {{
            font-size: 24px;
            text-align: center;
            margin-bottom: 40px;
            color: #333333 !important;
            font-weight: bold;
        }}

        /* CHAT TEXT */
        [data-testid="stChatMessage"] p {{
            font-size: 24px !important;
            color: #000000 !important;
            line-height: 1.4 !important;
            font-weight: 500 !important;
        }}

        /* Buttons */
        .stButton>button {{
            font-size: 20px !important;
            color: black !important;
        }}

        /* 🔒 LOCK CHAT INPUT CONTAINER */
        [data-testid="stChatInput"] {{
        position: fixed !important;
        bottom: 25px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;

        width: 70% !important;
        max-width: 950px !important;
        min-width: 650px !important;

        padding: 0 !important;
        margin: 0 !important;

        z-index: 999 !important;
        background: transparent !important;
        }}

        /* 🔒 LOCK INNER WRAPPER */
        [data-testid="stChatInput"] > div {{
        width: 100% !important;
        }}

        /* 🔒 LOCK TEXTAREA */
        [data-testid="stChatInput"] textarea {{
        height: 65px !important;
        min-height: 65px !important;
        max-height: 65px !important;

        font-size: 20px !important;
        padding: 18px !important;

        border-radius: 20px !important;
        box-sizing: border-box !important;
        }}

        /* 🔒 PREVENT FLEX SHRINK */
        textarea {{
        resize: none !important;
        }}


        /* Style the actual input box */
        [data-testid="stChatInput"] textarea {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-radius: 20px !important;
        padding: 18px !important;
        font-size: 20px !important;
        box-shadow: 0px 5px 25px rgba(0,0,0,0.25);
        }}


        /* 🌫️ Transparent chat bubbles (BOTH user & bot) */
        [data-testid="stChatMessage"] {{
        background-color: rgba(255, 255, 255, 0.35) !important;
        backdrop-filter: blur(6px);
        border-radius: 18px;
        padding: 12px 18px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        }}

        /* 💬 Chat text */
        [data-testid="stChatMessage"] p {{
        font-size: 22px !important;
        color: #000000 !important;
        font-weight: 500;
        }}

    </style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- UI LAYOUT ----------------

# All content wrapped in the Rectangular Box
st.markdown('<div class="centered-box">', unsafe_allow_html=True)

st.markdown('<div class="box-title">🧠 Mental Health Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="box-subtitle">How may I help you today?</div>', unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Box
user_input = st.chat_input("Write your statement here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("Processing..."):
        response = ollama.chat(model="llama3.1:8b", messages=st.session_state.messages)
        ai_reply = response["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True) 
    

