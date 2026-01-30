from rag import retrieve_context
import streamlit as st
import requests

st.set_page_config(page_title="E-commerce Support Bot")
st.title("🛒 E-commerce Customer Support AI")

# ------------------ SIDEBAR ------------------

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
    ⚙️ *Powered by a local open-source LLM*
    """
)

st.sidebar.success("🟢 AI Status: Local model running")

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ------------------ SESSION STATE ------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ DISPLAY CHAT HISTORY ------------------

if not st.session_state.messages:
    st.info("👋 Hi! I'm your AI support assistant. How can I help you today?")
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ------------------ USER INPUT ------------------

user_input = st.chat_input("Ask about orders, returns, refunds...")

if user_input:
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # ------------------ RAG ------------------
    context = retrieve_context(user_input)

    # ------------------ PROMPT ------------------
    prompt = (
        "You are a professional, polite e-commerce customer support assistant.\n"
        "Answer ONLY using the information provided below.\n"
        "If the answer is not present, politely say you don't have that information.\n\n"
        f"INFORMATION:\n{context}\n\n"
        f"Customer Question: {user_input}"
    )

    # ------------------ LLM RESPONSE (LM STUDIO) ------------------
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {
                    "model": "mistral",
                    "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional, polite e-commerce customer support assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3
                }

                response = requests.post(
                    "http://localhost:1234/v1/chat/completions",
                     json=payload,
                     timeout=60
                )

                data = response.json()

                choice = response.choices[0]
                if choice.message and choice.message.content:
                    ai_reply = choice.message.content
                elif hasattr(choice, "text") and choice.text:
                    ai_reply = choice.text
                else:
                    ai_reply = "⚠️ The local model returned an empty response."

            except Exception as e:
                ai_reply = f"⚠️ Local model error: {e}"

            st.markdown(ai_reply)

    # Save assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )

# ------------------ SUGGESTED QUESTIONS ------------------

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
