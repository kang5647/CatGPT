from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

app = FastAPI()

origins = ["http://localhost", "http://localhost:8080", "http://172.30.127.213:8501"]

# Set up CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")
CAT_API = os.getenv("CAT_API_KEY")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Define a POST endpoint to process chat requests
@app.post("/chat/")
async def chat(req: Request):
    data = await req.json()
    prompt = data["prompt"]
    limit = data["limit"]
    response = {}

    # If cat images are requested, fetch them and add to response
    if limit > 0:
        cats = []
        cat_data = get_cats(limit=limit)
        for cat in cat_data:
            image_url = cat["url"]
            cats.append({"image": image_url})
        response["cats"] = cats

    generated_text = generate_text(prompt)
    response["generated_text"] = generated_text

    return response


@app.get("/ping/")
async def ping():
    return {"ping": "200"}


# Generate text using OpenAI's model
def generate_text(prompt, limit=1):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are part of a distinguished company of cats.\
                         Your job is to motivate empployees who are working at Nika.eco,\
                         a climate data and insights team for carbon project investors and developers \
                         to predict opportunities and risks at scale. \
                         Your mission, as a feline motivator, is to offer encouragement and wisdom. \
                         Whenever someone types a question or needs a boost, you and your fellow cats are here to meow positively,\
                         offer motivational purrs, and provide answers to help guide their environmental endeavors.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Error in getting response: ", str(e))

    return None


# Fetch cat images from TheCatAPI
def get_cats(limit=1, breed=None):
    headers = {"x-api-key": CAT_API}
    url = f"https://api.thecatapi.com/v1/images/search?limit={limit}"

    if breed != None:
        url += "&breed_ids=" + breed
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()

        else:
            print(response.status_code)

    except Exception as e:
        print("Error in getting response: ", str(e))

    return None
