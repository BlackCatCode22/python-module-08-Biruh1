import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. "
        "Create a .env file with: OPENAI_API_KEY=your_real_key_here"
    )

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Streamlit page setup
st.set_page_config(page_title="Biruh History Professor Chatbot", page_icon="🏛️")
st.title("🏛️ Biruh History Professor Chatbot")
st.write(
    "Ask any question about history, world events, or important people in the past.\n\n"
    "_This chatbot uses OpenAI models through the Chat Completions API._"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly and patient history professor. "
                "Explain historical events, time periods, and important people "
                "in clear and simple language. "
                "Give short examples and connect events to the bigger picture "
                "so a beginner can understand."
            ),
        }
    ]

# Display previous messages (hide system prompt)
for msg in st.session_state.messages[1:]:
    role_icon = "👤 Student" if msg["role"] == "user" else "🏛️ Professor"
    st.markdown(f"**{role_icon}:** {msg['content']}")

st.write("---")

# User input box
user_input = st.text_area(
    "Type your history question here:",
    placeholder="Example: What caused World War One, or who was Cleopatra?",
)

col1, col2 = st.columns(2)
with col1:
    send_clicked = st.button("Ask the professor")
with col2:
    clear_clicked = st.button("Clear conversation")

# Clear chat
if clear_clicked:
    st.session_state.messages = st.session_state.messages[:1]
    st.rerun()

# Handle user question
if send_clicked and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=500,
        )

        assistant_reply = completion.choices[0].message.content

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply}
        )

        st.rerun()

    except Exception as e:
        st.error(f"Error talking to OpenAI API: {e}")
