
# I got this streamlit interface from this repository: https://github.com/heiko-hotz/streamlit-chatgpt-ui

import streamlit as st
from streamlit_chat import message
import asyncio
from whisper_stt import whisper_stt
from coordinator import triage_agent, CustomerContext
from agents import Runner, OutputGuardrailTripwireTriggered

# Page config
st.set_page_config(page_title="Customer Support Chat", page_icon="💬")

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "customer_id" not in st.session_state:
    st.session_state.customer_id = "cust_001"

# Sidebar: customer selection
st.sidebar.header("Customer Selection")
customer_id = st.sidebar.selectbox("Select Customer ID", ["cust_001", "cust_002", "cust_003"], index=0)
customer_names = {
    "cust_001": "User 1",
    "cust_002": "User 2",
    "cust_003": "User 3"
}

# Update customer context if changed
if st.session_state.customer_id != customer_id:
    st.session_state.customer_id = customer_id
    st.session_state.messages = []  # Clear chat on customer switch
    st.rerun()  # Force immediate rerun to reset the session

# Set or update customer context
if "customer_context" not in st.session_state or st.session_state.customer_context.customer_id != customer_id:
    st.session_state.customer_context = CustomerContext(
        customer_id=customer_id,
        customer_name=customer_names.get(customer_id, "User")
    )

# Title
st.title("💬 Customer Support Chat")
st.caption("Ask about order tracking or returns")

# Display chat history
for i, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=msg["role"] == "user", key=str(i))

# Whisper voice input
audio_text = whisper_stt(
    start_prompt="🎤",
    stop_prompt="⏹️",
    language='en',
    key="audio_input"
)

# Text input fallback
user_prompt = st.chat_input("Type your message here...")

# Determine final input
final_input = audio_text if audio_text else user_prompt

# Response handler
async def get_agent_response(user_input, context):
    result = await Runner.run(triage_agent, input=user_input, context=context)
    return result.final_output

# If input available, process
if final_input:
    st.session_state.messages.append({"role": "user", "content": final_input})
    message(final_input, is_user=True, key=f"user-{len(st.session_state.messages)}")
    with st.spinner("Thinking..."):
        response = asyncio.run(get_agent_response(final_input, st.session_state.customer_context))
    message(response, is_user=False, key=f"ai-{len(st.session_state.messages)}")
    st.session_state.messages.append({"role": "assistant", "content": response})

# About info
with st.expander("About this chat"):
    st.write("""
    This chat interface uses a triage agent to route queries:
    - **Returns Agent**: For product return questions
    - **Tracking Agent**: For order tracking issues
    - **Fallback**: General questions
    """)