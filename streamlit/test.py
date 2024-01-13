import streamlit as st
from streamlit_chat import message

background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://tabiracademy.com/_next/image?url=https%3A%2F%2Ftabir-prod.s3.amazonaws.com%2Fmedia%2FFAST_NUCES.jpg&w=1920&q=100");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

chat_input_style = """
<style>
div[data-baseweb="input"] {
    background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent dark background color */
    color: white; /* Text color */
    border: none; /* Remove border */
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)
st.markdown(chat_input_style, unsafe_allow_html=True)

st.title("Admission Query Bot ")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message['avatar']):
        st.markdown(message["content"])

# Placeholder container for user input
user_input_container = st.empty()

# Display user input using st.text_input
user_input = user_input_container.text_input("What is up?")

# Display user message in chat message container when user submits input
if st.button("Send"):
    with st.chat_message("user", avatar='🧑🏻‍🦱'):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "avatar": "🧑🏻‍🦱", "content": user_input})

# Example assistant response
response = f"Senior: {user_input}"
with st.chat_message("assistant", avatar='😎'):
    st.markdown(response)
st.session_state.messages.append({"role": "assistant", "avatar": "😎", "content": response})
