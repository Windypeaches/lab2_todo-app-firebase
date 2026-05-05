## Tác giả

24120006 - Đào Thanh Phong
Tư duy tính toán - 24CTT3 - Lab2



# Todo App (Streamlit + FastAPI + Firebase)

## Mô tả

Ứng dụng Todo đơn giản cho phép:

* Đăng nhập bằng Firebase (Email/Password)
* Thêm task
* Lưu task theo từng user
* Xem danh sách task

---

## Công nghệ

* FastAPI (Backend)
* Streamlit (Frontend)
* Firebase Authentication
* SQLite + SQLAlchemy

---

## Cách chạy

### 1. Cài thư viện

```bash
pip install fastapi uvicorn streamlit firebase-admin sqlalchemy requests
```

---

### 2. Chạy Backend

```bash
cd backend
python -m uvicorn main:app --reload --port 8001
```

---

### 3. Chạy Frontend (Streamlit)

Mở terminal mới:

```bash
cd backend
python -m streamlit run app.py
```

Truy cập:

* http://127.0.0.1:8001/docs (API)
* http://localhost:8501 (UI)

---

## Firebase

* Bật **Email/Password Authentication**
* Tạo file:

```
backend/.streamlit/secrets.toml
```

---

## API

* `POST /tasks` → tạo task
* `GET /tasks` → lấy danh sách task


---

## Kết quả

- Login thành công
- Thêm task
- Lưu database
- Hiển thị task


---


## Video demo
* https://drive.google.com/drive/folders/1fsShr-OZebuiZgq5EJBIRJsGL9lGsh5a?usp=sharing
