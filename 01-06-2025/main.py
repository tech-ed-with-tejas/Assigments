import streamlit as st
from rag import generate_text_and_images


import base64
from io import BytesIO
from PIL import Image



prompt = st.chat_input("Say something")

st.text("Hi! I'm an AI model here to help you with any questions.I have Good Knowldge on  Just type your question below, and I'll do my best to explain it clearly!")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
    response = generate_text_and_images(prompt)
    print(response['table'])
    st.write(response["llm_answer"])
    for i in response["images"]:
        image_bytes = base64.b64decode(i)

        image = Image.open(BytesIO(image_bytes))
        st.image(image, caption='Your Image Caption')
    for i in response['table']:
        st.markdown(i, unsafe_allow_html=True)
