# 🏦 Bank Management System

A Python-based Bank Management System that allows users to create bank accounts, manage account details, perform transactions, and securely store account information using JSON files.

This repository contains **two versions** of the project:

1. **Console-Based Version** (Built entirely by me)
2. **Streamlit Web Application** (AI-assisted enhanced version)

---

## 📌 Features

- Create a new bank account
- Login using account credentials
- Deposit money
- Withdraw money
- Check account balance
- Update account information
- Delete account
- Persistent data storage using JSON
- User-friendly interface (Streamlit version)

---

# 📂 Project Structure

```
Bank-Management-System/
│
├── main.py                # Console-based Bank Management System(My version)
├── data.json              # Stores data for the console version
│
├── bank_app.py            # Streamlit web application(AI Version - Used Claude Ai To improve the code and Build Streamlit Application)
├── bank_data.json         # Stores data for the Streamlit version
```
---

# 💻 Console Version

### File

`main.py`

### About

This is the **original version** of the project.

- All business logic was designed and implemented by me.
- Includes account creation, authentication, deposits, withdrawals, account updates, balance checking, and account deletion.
- User data is stored locally in:

```
data.json
```

---

# 🌐 Streamlit Version

### File

`bank_app.py`

### About

This is an **AI-assisted enhanced version** of the project, built using **Streamlit** to provide a modern graphical web interface.

Features include:

- Interactive UI
- Better user experience
- Improved validation
- Responsive interface
- Same banking functionalities as the console version

All account data for this version is stored in:

```
bank_data.json
```

---

# 🚀 How to Run

## Console Version

```bash
python main.py
```

---

## Streamlit Version

Install Streamlit (if not already installed):

```bash
pip install streamlit
```

Run the application:

```bash
streamlit run bank_app.py
```

---

# 🛠 Technologies Used

- Python
- JSON
- Streamlit
- Object-Oriented Programming (OOP)

---

# 📖 Learning Outcomes

This project helped me practice:

- Object-Oriented Programming
- File Handling
- JSON Data Storage
- Exception Handling
- Input Validation
- Python Classes and Methods
- Streamlit Web App Development

---

# 👨‍💻 Author

**Ashutosh Panda**

This repository showcases both my original console-based implementation and an enhanced Streamlit version for learning and comparison purposes.

---
