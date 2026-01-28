from rag import retrieve_context
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-latest")

st.set_page_config(page_title="E-commerce Support Bot")
st.title("🛒 E-commerce Customer Support AI")

st.sidebar.title("🛍️ ShopEase Support")
st.sidebar.markdown(
    """
    **AI Customer Support Bot**

    Ask questions about:
    - 📦 Orders  
    - 🔄 Returns & refunds  
    - 💳 Payments  
    - 🚚 Delivery  

    ---
    ⚠️ *This is a demo support assistant.*
    """
)

st.sidebar.success("🟢 AI Status: Online")

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.info("👋 Hi! I'm your AI support assistant. How can I help you today?")
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

user_input = st.chat_input("Ask about orders, returns, refunds...")

if user_input:
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    context = retrieve_context(user_input)

    prompt = (
        "You are a professional, polite e-commerce customer support assistant.\n"
        "Answer ONLY using the information provided below.\n"
        "If the answer is not present, politely say you don't have that information.\n\n"
        f"INFORMATION:\n{context}\n"
        f"Customer Question: {user_input}"
    )

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.generate_content(prompt)
            ai_reply = response.text
            st.markdown(ai_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )

st.markdown("### 💡 Try asking:")
cols = st.columns(3)

with cols[0]:
    if st.button("Return policy"):
        st.session_state.messages.append(
            {"role": "user", "content": "What is your return policy?"}
        )
        st.rerun()

with cols[1]:
    if st.button("Payment issue"):
        st.session_state.messages.append(
            {"role": "user", "content": "My payment failed but money was deducted"}
        )
        st.rerun()

with cols[2]:
    if st.button("Delivery time"):
        st.session_state.messages.append(
            {"role": "user", "content": "How long does delivery take?"}
        )
        st.rerun()
