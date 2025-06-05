import streamlit as st
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Personality and scoring system prompt
marvin_personality = """
Your name is Marvin, an AI agent that qualifies vehicle sellers for Sub2 deals.
Ask these questions conversationally:
1. Is the vehicle paid off or do you still have a loan on it?
2. What’s your monthly payment and who’s the lender?
3. Do you know the current payoff or balance?
4. Is there a reason you’re looking to sell right now?
Based on their answers, score the deal (1-10). Score higher if:
- Vehicle is newer (<5 yrs)
- Seller has loan
- Monthly payment is low
- Seller is urgent or behind
Explain if it’s a good fit and ask if you can pass it to a real buyer.
Be friendly, helpful, and sharp — not salesy.
"""

st.title("🚗 Marvin - Sub2 Vehicle Lead Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": marvin_personality}]

user_input = st.text_input("You (Seller):", key="input")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=st.session_state.chat_history,
        temperature=0.6
    )

    reply = response['choices'][0]['message']['content']
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

    st.markdown(f"**Marvin:** {reply}")

# Optional: Display conversation history
with st.expander("Show full chat history"):
    for msg in st.session_state.chat_history:
        st.write(f"**{msg['role'].capitalize()}**: {msg['content']}")
