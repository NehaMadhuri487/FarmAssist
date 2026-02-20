import streamlit as st
import requests

st.set_page_config(page_title="Agri AI Query", layout="centered")
st.title("🌾 Agricultural AI Query System")

query = st.text_area("Enter your query here (any language):")

if st.button("Ask"):
    if query:
        response = requests.post("http://127.0.0.1:8000/ask", json={"text": query})
        if response.status_code == 200:
            data = response.json()
            st.success("Response:")
            st.write(data["response"])
        else:
            st.error("Error processing query")