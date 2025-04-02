import streamlit as st
import requests

st.title("AI Text-to-Video Generator")

# User Authentication
st.sidebar.title("Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    response = requests.post("http://127.0.0.1:8000/token", data={"username": username, "password": password})
    if response.status_code == 200:
        st.session_state["token"] = response.json()["access_token"]
        st.success("Logged in successfully!")
    else:
        st.error("Invalid credentials.")

# Video Generation
if "token" in st.session_state:
    st.text_input("Enter a scene description:", key="prompt")

    if st.button("Generate Video"):
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        response = requests.post("http://127.0.0.1:8000/generate_video/", headers=headers, json={"prompt": st.session_state["prompt"]})

        if response.status_code == 200:
            st.success("Video generated successfully!")
            st.video(response.json()["video_url"])
        else:
            st.error("Failed to generate video.")
