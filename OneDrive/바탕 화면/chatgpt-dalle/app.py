import streamlit as st # 모듈 임포트
import openai
import time

openai.api_key = st.secrets["api_key"]

st.title("ChatGPT-4 + DALL-E") # 제목 지정(표시)

with st.form("form"): #제출이 가능한 하나의 폼 만들기
    user_input = st.text_input("Prompt") # 글상자(입력 가능) 추가하기
    model = st.selectbox("GPT Model", ["gpt-4", "gpt-3.5-turbo"])
    size = st.selectbox("Image Size", ["1024x1024", "512x512", "256x256"])
    response_times = st.selectbox("Number of responses(Normally 1)", ["1", "2"])
    sumbit = st.form_submit_button("Sumbit") # 제출 버튼 추가하기

if sumbit and user_input: # 만약 버튼을 눌렀다면 and 글상자가 있다면
    gpt_prompt = [{
        "role": "system",
        "content": "Imagine the detail appeareance of the input. Response it in medium length, around 20~50 words or a few sentences. Provide additional details. Use polite/formal words when responsing with languages other than English."
    }]
    for i in range(1, int(response_times)+1):
        gpt_prompt.append({
            "role": "user",
            "content": user_input
        })

        with st.spinner("Waiting for ChatGPT to response..."):
            gpt_response = openai.ChatCompletion.create(
                model=model,
                messages=gpt_prompt
            )

        prompt = gpt_response["choices"][0]["message"]["content"]
        st.write(prompt)
        time.sleep(3)

        with st.spinner("Waiting for DALL-E to create images..."):
            dalle_response = openai.Image.create(
                prompt=prompt,
                size=size
            )

        st.image(dalle_response["data"][0]["url"])
        if i == int(response_times)+1:
            st.write("Final Text/Image")
        else:
            st.write("Text&Image Number", i)