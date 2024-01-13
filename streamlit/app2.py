import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import random
import numpy as np
import json
from sklearn.preprocessing import LabelEncoder
import pandas as pd
with open('content.json') as content:
  data1 = json.load(content)

tags = []
inputs = []
responses = {}
for intent in data1['intents']:
  responses[intent['tag']]= intent['responses']
  for lines in intent['patterns']:
    inputs.append(lines)
    tags.append(intent['tag'])


data = pd.DataFrame({'inputs': inputs, 'tags':tags})

model = load_model("model.h5")


with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)


with open('label_encoder.pkl', 'rb') as handle:
     le = pickle.load(handle)




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

st.markdown(background_image, unsafe_allow_html=True)
st.title("Admission Query Bot ")

if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := st.text_input("You:"):
    for message in st.session_state.messages:
         with st.chat_message(message["role"], avatar=message['avatar']):
               st.markdown(f'<span style="color: white;">{message["content"]}</span>', unsafe_allow_html=True)
    with st.chat_message("user", avatar='🧑🏻‍🦱'):
          st.markdown(f'<span style="color: white;">{prompt}</span>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "avatar": "🧑🏻‍🦱", "content": prompt})

    # Preprocess the user input
    user_input = [letters.lower() for letters in prompt if letters.isalnum() or letters.isspace()]
    user_input = ''.join(user_input)

    # Tokenization and padding
    prediction_input = tokenizer.texts_to_sequences([user_input])
    prediction_input = np.array(prediction_input).reshape(-1)
    prediction_input = pad_sequences([prediction_input], 7)

    # Make prediction
    output = model.predict(prediction_input)
    output = output.argmax()

    # Get the response tag
    response_tag = le.inverse_transform([output])[0]

    # Display the bot's response
    with st.chat_message("assistant", avatar='😎'):
         response_text = random.choice(responses.get(response_tag, ["I'm not sure what you're asking."]))
         st.markdown(f'<span style="color: white;">{response_text}</span>', unsafe_allow_html=True)



    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "avatar": "😎", "content":response_text})
