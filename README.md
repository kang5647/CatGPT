# CatGPT

1. Activate venv
  ```
   python3 -m venv venv
   source venv/bin/activate
  ```
2. Install dependencies
  ```
  pip install -r requirements.txt
  ```
3. Change directory to backend and run
  ```
  uvicorn main:app --reload
  ``` 
4. Open another terminal, change directory to frontend and run
  ```
  streamlit run cat_gpt.py
  ```
