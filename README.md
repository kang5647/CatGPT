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

![image](https://github.com/kang5647/CatGPT/assets/76279908/68e41fb8-a3d3-4c40-91a7-5c65654c0fae)
