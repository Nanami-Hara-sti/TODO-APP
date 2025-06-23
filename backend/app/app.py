# import streamlit as st
# import random
# import requests
# import json
# import datetime

# st.title("API Test")


# with st.form(key='todo'):
#     id: int = random.randint(1, 1000)
#     title: str = st.text_area("Title", max_chars=255, value="Sample Title")
#     description: str = st.text_area("Description", max_chars=1000, value="Sample Description")
#     status: str = st.selectbox("Status", ["未着手", "進行中", "完了"], index=0)
#     current_time = datetime.datetime.now().isoformat()
#     data ={
#         "id": id,
#         "title": title,
#         "description": description,
#         "status": status,
#         "created_at": current_time,
#         "updated_at": current_time
#     }
#     submit_button = st.form_submit_button(label='Submit')

# if submit_button:
#     st.write("Submitting data...")
#     st.json(data)
#     st.write("Sending request to API...")
#     url = "http://localhost:8000/todos"
    
#     res = requests.post(
#         url, 
#         data=json.dumps(data),
#         headers={"Content-Type": "application/json"}
#     )
    
#     st.write(f"API Response Status Code: {res.status_code}") # ステータスコードを表示
    
#     # リクエストが成功したかを確認してからJSONをパース
#     if res.status_code == 200:
#         st.json(res.json())
#     else:
#         st.error(f"Error: {res.status_code} - {res.text}")