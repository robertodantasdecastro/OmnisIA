import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("OmnisIA Trainer Web")

uploaded_file = st.file_uploader("Upload arquivo")
if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    res = requests.post(f"{API_URL}/upload", files=files)
    st.write(res.json())

text = st.text_input("Digite para conversar")
if st.button("Enviar") and text:
    res = requests.post(f"{API_URL}/chat", json={"text": text})
    st.write(res.json().get("response"))
