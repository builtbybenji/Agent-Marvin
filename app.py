import streamlit as st
import os
from openai import OpenAI

# Load API key (from secrets or env var)
api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", ""))
client = OpenAI(api_key=api_key)

# Marvin's system message
marvin_personality = """
Your name is Marvin, an AI assistant trained to qualify vehicle sellers for creative finance deals (Sub2, Seller Finance).
You ask about:
1. Whether the vehicle has a loan
2. Current monthly payment and payoff
3. The reason for selling
You score deals 1–10. Higher scores = financed, newer car, low payment, urgency. Be helpful and confident. You do NOT negotiate.
"""

st.set_page_config(page_title="Marvin AI - Vehicle Lead Audit", page_icon="🚗")
st.title("🚗 Marvin: Sub2 Vehicle Lead Screener")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": marvin_personality}]

user_input = st.text_input("You (Vehicle Seller):", key="input")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.chat_history,
            temperature=0.6
        )

        reply = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.markdown(f"**Marvin:** {reply}")

    except Exception as e:
        st.error(f"Error: {str(e)}")

with st.expander("🧠 Show Chat History"):
    for msg in st.session_state.chat_history:
        st.write(f"**{msg['role'].capitalize()}**: {msg['content']}")

