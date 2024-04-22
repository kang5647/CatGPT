import streamlit as st
import requests
from utils import display_images

API_URL = "127.0.0.1:8000"

# Initialize the limit of cat images to show
limit = 0

with st.sidebar:
    st.image("https://cdn2.thecatapi.com/images/ant.gif")

    # Checkbox
    show_cat = st.checkbox("Show cats with the response?", value=True)
    # If checkbox is checked, allow the user to specify how many cat images to show
    if show_cat:
        limit = st.number_input(
            "Insert a number", value=1, placeholder="1", step=1, min_value=1
        )
    else:
        limit = 0


st.title("CatGPT 🐈")
st.caption("Greetings Hoomans at Nika! Get your daily dose of meow-tivation!")


# Initialize session state for storing messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "🐾",
            "content": {
                "text": "How can I paw-sitively assist you today?",
                "images": [],
            },
        }
    ]

# Display all messages stored in the session
for msg in st.session_state.messages:
    content = msg["content"]
    role = msg["role"]

    if role == "user":
        st.chat_message(role).write(content)

    else:
        st.chat_message(role).write(content["text"])

        images = content["images"]
        num_images = len(images)

        if num_images > 0:
            display_images(images)

prompt = st.chat_input("Type your mewsage here:", key="chat_input")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    headers = {"Content-Type": "application/json"}
    payload = {"prompt": prompt, "limit": limit}

    url = f"http://{API_URL}/chat/"

    with st.spinner("Waiting..."):
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:

            data = response.json()
            msg = data["generated_text"]
            st.chat_message("🐾").write(msg)

            images = []

            # If cat images are to be shown
            if show_cat:
                cats = data["cats"]
                for cat in cats:
                    cat_image = cat["image"]
                    images.append(cat_image)

            display_images(images)

            content = {"text": msg, "images": images}
            st.session_state.messages.append({"role": "🐾", "content": content})

        else:
            st.error(f"Failed to get response: {response.status_code}")
