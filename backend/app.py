import streamlit as st
import requests

# CONFIG

st.set_page_config(page_title="Todo App", layout="centered")

BASE_URL = "http://127.0.0.1:8001"
API_KEY = st.secrets["firebase_client"]["apiKey"]

st.title("Todo App")

# STYLE
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1 {
    text-align: center;
    font-weight: 700;
}
.stTextInput>div>div>input {
    border-radius: 10px;
}
.stButton button {
    border-radius: 10px;
    padding: 10px 20px;
}
.card {
    padding: 15px;
    border-radius: 12px;
    background: #1c1f26;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# SESSION
if "token" not in st.session_state:
    st.session_state.token = None

if "tasks" not in st.session_state:
    st.session_state.tasks = []

def load_tasks():
    if not st.session_state.token:
        return []

    headers = {
        "Authorization": "Bearer " + st.session_state.token
    }

    res = requests.get(f"{BASE_URL}/tasks", headers=headers)

    if res.status_code == 200:
        return res.json()
    else:
        return []

# LOGIN
st.header("🔐 Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"

    # reset token cũ
    st.session_state.token = None

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    res = requests.post(url, json=payload)

    if res.status_code == 200:
        data = res.json()
        st.session_state.token = data["idToken"]

        # load task ngay sau login
        st.session_state.tasks = load_tasks()

        st.success("Login success")
    else:
        st.error("Login failed")

# ADD TASK
st.header("➕ Add Task")

task = st.text_input("Task title")

if st.button("Add Task"):
    if not st.session_state.token:
        st.error("Bạn chưa login")
    else:
        headers = {
            "Authorization": "Bearer " + st.session_state.token,
            "Content-Type": "application/json"
        }

        res = requests.post(
            f"{BASE_URL}/tasks",
            headers=headers,
            json={"title": task}
        )

        st.success("Task created")
        st.session_state.tasks = load_tasks()
        st.rerun()

# TASK LIST
st.header("Task List")

if not st.session_state.token:
    st.warning("Vui lòng login trước")
    st.stop()

# nếu chưa có task thì load lần đầu
if not st.session_state.tasks:
    st.session_state.tasks = load_tasks()

for t in st.session_state.tasks:
    col1, col2, col3 = st.columns([6,1,1])

    with col1:
        st.markdown(
            f"<div class='card'>{'✅' if t['completed'] else '📝'} {t['title']}</div>",
            unsafe_allow_html=True
        )

    headers = {
    "Authorization": "Bearer " + st.session_state.token
}
    with col2:
        checked = st.checkbox(
            "",
            value=t["completed"],
            key=f"check_{t['id']}"
        )

        if checked != t["completed"]:
            headers = {
                "Authorization": "Bearer " + st.session_state.token
            }

            requests.put(
                f"{BASE_URL}/tasks/{t['id']}",
                headers=headers
            )

            st.session_state.tasks = load_tasks()
            st.rerun()  

    with col3:
        if st.button("❌", key=f"delete_{t['id']}"):
            requests.delete(
                f"{BASE_URL}/tasks/{t['id']}",
                headers=headers
            )
            st.session_state.tasks = load_tasks()