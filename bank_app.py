import json
import random
import string
import re
from pathlib import Path
import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NexBank",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Theme & CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* ── Palette ──
   Deep navy   #0B1120
   Card bg     #131C30
   Accent teal #00D4B4
   Muted text  #6B7FA3
   Border      #1E2D4A
   Danger      #FF4F6B
   Gold        #FFB830
*/

.stApp {
    background: #0B1120;
    color: #E2E8F6;
}

/* Hide default streamlit header chrome */
#MainMenu, header, footer { visibility: hidden; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.hero-logo {
    font-family: 'Space Mono', monospace;
    font-size: 2.6rem;
    font-weight: 700;
    color: #E2E8F6;
    letter-spacing: -1px;
}
.hero-logo span { color: #00D4B4; }
.hero-tagline {
    font-size: 0.88rem;
    color: #6B7FA3;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* ── Nav tabs ── */
div[data-testid="stTabs"] button {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    color: #6B7FA3 !important;
    letter-spacing: 0.05em;
    border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.6rem 1.2rem !important;
    background: transparent !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #00D4B4 !important;
    border-bottom-color: #00D4B4 !important;
}
div[data-testid="stTabsContent"] {
    border-top: 1px solid #1E2D4A;
    padding-top: 1.5rem;
}

/* ── Card wrapper ── */
.card {
    background: #131C30;
    border: 1px solid #1E2D4A;
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.2rem;
}
.card-title {
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6B7FA3;
    margin-bottom: 1.2rem;
    font-weight: 600;
}

/* ── Stat boxes ── */
.stat-grid { display: flex; gap: 1rem; margin-bottom: 1.2rem; flex-wrap: wrap; }
.stat-box {
    flex: 1;
    min-width: 120px;
    background: #0F1826;
    border: 1px solid #1E2D4A;
    border-radius: 10px;
    padding: 1rem 1.2rem;
}
.stat-label { font-size: 0.68rem; color: #6B7FA3; letter-spacing: 0.12em; text-transform: uppercase; }
.stat-value { font-family: 'Space Mono', monospace; font-size: 1.4rem; font-weight: 700; color: #E2E8F6; margin-top: 0.25rem; }
.stat-value.teal { color: #00D4B4; }
.stat-value.gold { color: #FFB830; }

/* ── Info rows ── */
.info-row { display: flex; justify-content: space-between; align-items: center; padding: 0.7rem 0; border-bottom: 1px solid #1E2D4A; }
.info-row:last-child { border-bottom: none; }
.info-key { font-size: 0.78rem; color: #6B7FA3; text-transform: uppercase; letter-spacing: 0.1em; }
.info-val { font-family: 'Space Mono', monospace; font-size: 0.9rem; color: #E2E8F6; }
.info-val.accent { color: #00D4B4; }

/* ── Account number badge ── */
.accno-badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 1.05rem;
    font-weight: 700;
    background: linear-gradient(135deg, #00D4B4 0%, #0099FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.08em;
}

/* ── Alert banners ── */
.alert-success {
    background: rgba(0,212,180,0.12);
    border: 1px solid rgba(0,212,180,0.35);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #00D4B4;
    font-size: 0.9rem;
    margin: 0.6rem 0;
}
.alert-error {
    background: rgba(255,79,107,0.12);
    border: 1px solid rgba(255,79,107,0.35);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #FF4F6B;
    font-size: 0.9rem;
    margin: 0.6rem 0;
}
.alert-warn {
    background: rgba(255,184,48,0.12);
    border: 1px solid rgba(255,184,48,0.35);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #FFB830;
    font-size: 0.9rem;
    margin: 0.6rem 0;
}

/* ── Inputs ── */
.stTextInput input, .stNumberInput input, .stPasswordInput input {
    background: #0F1826 !important;
    border: 1px solid #1E2D4A !important;
    border-radius: 8px !important;
    color: #E2E8F6 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #00D4B4 !important;
    box-shadow: 0 0 0 2px rgba(0,212,180,0.2) !important;
}
label { color: #B0BEDC !important; font-size: 0.83rem !important; font-weight: 500 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #00D4B4, #0099FF) !important;
    color: #0B1120 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.6rem !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.04em !important;
    width: 100% !important;
    margin-top: 0.5rem !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stButton > button.danger {
    background: linear-gradient(135deg, #FF4F6B, #C0142B) !important;
    color: #fff !important;
}

/* ── Divider ── */
hr { border-color: #1E2D4A !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0B1120; }
::-webkit-scrollbar-thumb { background: #1E2D4A; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── Backend ───────────────────────────────────────────────────────────────────
DATABASE = "bank_data.json"


def load_data():
    p = Path(DATABASE)
    if p.exists():
        with open(DATABASE) as f:
            return json.load(f)
    return []


def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=2)


def gen_account_no():
    alpha = random.choices(string.ascii_uppercase, k=3)
    num   = random.choices(string.digits, k=4)
    sp    = random.choices("!@#$%&", k=1)
    parts = alpha + num + sp
    random.shuffle(parts)
    return "".join(parts)


def find_user(data, account_no, pin):
    for user in data:
        if user["accountNo"] == account_no and user["pin"] == int(pin):
            return user
    return None


def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


# ── Session state init ────────────────────────────────────────────────────────
if "bank_data" not in st.session_state:
    st.session_state.bank_data = load_data()


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-logo">Nex<span>Bank</span></div>
  <div class="hero-tagline">Secure · Simple · Modern Banking</div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs(["🆕 Open Account", "💳 Deposit", "💸 Withdraw", "👤 My Account", "✏️ Update", "🗑 Close Account"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Open Account
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="card"><div class="card-title">Create a new account</div>', unsafe_allow_html=True)

    name  = st.text_input("Full Name", placeholder="e.g. Ashutosh Mishra", key="ca_name")
    age   = st.number_input("Age", min_value=1, max_value=120, value=18, step=1, key="ca_age")
    email = st.text_input("Email Address", placeholder="you@example.com", key="ca_email")
    col1, col2 = st.columns(2)
    with col1:
        pin  = st.text_input("4-digit PIN", type="password", max_chars=4, placeholder="••••", key="ca_pin")
    with col2:
        pin2 = st.text_input("Confirm PIN", type="password", max_chars=4, placeholder="••••", key="ca_pin2")

    if st.button("Open Account", key="btn_create"):
        errors = []
        if not name.strip():
            errors.append("Name is required.")
        if age < 18:
            errors.append("You must be at least 18 years old.")
        if not validate_email(email):
            errors.append("Enter a valid email address.")
        if not pin.isdigit() or len(pin) != 4:
            errors.append("PIN must be exactly 4 digits.")
        if pin != pin2:
            errors.append("PINs do not match.")

        if errors:
            for e in errors:
                st.markdown(f'<div class="alert-error">⚠ {e}</div>', unsafe_allow_html=True)
        else:
            acc_no = gen_account_no()
            new_user = {
                "name": name.strip(),
                "age": int(age),
                "email": email.strip().lower(),
                "pin": int(pin),
                "accountNo": acc_no,
                "balance": 0,
            }
            st.session_state.bank_data.append(new_user)
            save_data(st.session_state.bank_data)

            st.markdown('<div class="alert-success">✅ Account created successfully!</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card" style="margin-top:1rem;">
              <div class="card-title">Your account details</div>
              <div class="info-row"><span class="info-key">Name</span><span class="info-val">{new_user['name']}</span></div>
              <div class="info-row"><span class="info-key">Age</span><span class="info-val">{new_user['age']}</span></div>
              <div class="info-row"><span class="info-key">Email</span><span class="info-val">{new_user['email']}</span></div>
              <div class="info-row"><span class="info-key">Account No</span><span class="info-val accent"><span class="accno-badge">{new_user['accountNo']}</span></span></div>
              <div class="info-row"><span class="info-key">Balance</span><span class="info-val">₹0.00</span></div>
            </div>
            <div class="alert-warn">📌 Save your Account Number — you'll need it for all transactions.</div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Deposit
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="card"><div class="card-title">Deposit money</div>', unsafe_allow_html=True)

    dep_acc = st.text_input("Account Number", placeholder="e.g. A3K!9Z2", key="dep_acc")
    dep_pin = st.text_input("PIN", type="password", max_chars=4, placeholder="••••", key="dep_pin")
    dep_amt = st.number_input("Amount (₹)", min_value=1, max_value=100000, value=500, step=100, key="dep_amt")
    st.caption("Single deposit: ₹1 – ₹1,00,000")

    if st.button("Deposit", key="btn_deposit"):
        data = st.session_state.bank_data
        user = find_user(data, dep_acc.strip(), dep_pin)
        if not user:
            st.markdown('<div class="alert-error">⚠ Invalid account number or PIN.</div>', unsafe_allow_html=True)
        elif dep_amt <= 0 or dep_amt > 100000:
            st.markdown('<div class="alert-error">⚠ Amount must be between ₹1 and ₹1,00,000.</div>', unsafe_allow_html=True)
        else:
            user["balance"] += int(dep_amt)
            save_data(data)
            st.markdown(f"""
            <div class="alert-success">✅ ₹{dep_amt:,} deposited successfully.</div>
            <div class="stat-grid" style="margin-top:1rem;">
              <div class="stat-box">
                <div class="stat-label">Deposited</div>
                <div class="stat-value gold">₹{dep_amt:,}</div>
              </div>
              <div class="stat-box">
                <div class="stat-label">New Balance</div>
                <div class="stat-value teal">₹{user['balance']:,}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Withdraw
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="card"><div class="card-title">Withdraw money</div>', unsafe_allow_html=True)

    wd_acc = st.text_input("Account Number", key="wd_acc")
    wd_pin = st.text_input("PIN", type="password", max_chars=4, placeholder="••••", key="wd_pin")
    wd_amt = st.number_input("Amount (₹)", min_value=1, value=500, step=100, key="wd_amt")

    if st.button("Withdraw", key="btn_withdraw"):
        data = st.session_state.bank_data
        user = find_user(data, wd_acc.strip(), wd_pin)
        if not user:
            st.markdown('<div class="alert-error">⚠ Invalid account number or PIN.</div>', unsafe_allow_html=True)
        elif wd_amt <= 0:
            st.markdown('<div class="alert-error">⚠ Enter a valid amount.</div>', unsafe_allow_html=True)
        elif user["balance"] < wd_amt:
            st.markdown(f'<div class="alert-error">⚠ Insufficient balance. Available: ₹{user["balance"]:,}</div>', unsafe_allow_html=True)
        else:
            user["balance"] -= int(wd_amt)
            save_data(data)
            st.markdown(f"""
            <div class="alert-success">✅ ₹{wd_amt:,} withdrawn successfully.</div>
            <div class="stat-grid" style="margin-top:1rem;">
              <div class="stat-box">
                <div class="stat-label">Withdrawn</div>
                <div class="stat-value gold">₹{wd_amt:,}</div>
              </div>
              <div class="stat-box">
                <div class="stat-label">Remaining Balance</div>
                <div class="stat-value teal">₹{user['balance']:,}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — My Account (Show Details)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="card"><div class="card-title">Account details</div>', unsafe_allow_html=True)

    sd_acc = st.text_input("Account Number", key="sd_acc")
    sd_pin = st.text_input("PIN", type="password", max_chars=4, placeholder="••••", key="sd_pin")

    if st.button("View Details", key="btn_show"):
        data = st.session_state.bank_data
        user = find_user(data, sd_acc.strip(), sd_pin)
        if not user:
            st.markdown('<div class="alert-error">⚠ Invalid account number or PIN.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="stat-grid">
              <div class="stat-box">
                <div class="stat-label">Balance</div>
                <div class="stat-value teal">₹{user['balance']:,}</div>
              </div>
              <div class="stat-box">
                <div class="stat-label">Account No</div>
                <div class="stat-value" style="font-size:1rem;"><span class="accno-badge">{user['accountNo']}</span></div>
              </div>
            </div>
            <div class="info-row"><span class="info-key">Full Name</span><span class="info-val">{user['name']}</span></div>
            <div class="info-row"><span class="info-key">Age</span><span class="info-val">{user['age']}</span></div>
            <div class="info-row"><span class="info-key">Email</span><span class="info-val">{user['email']}</span></div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — Update Details
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="card"><div class="card-title">Update account details</div>', unsafe_allow_html=True)

    up_acc = st.text_input("Account Number", key="up_acc")
    up_pin = st.text_input("Current PIN", type="password", max_chars=4, placeholder="••••", key="up_pin")

    if st.button("Load Account", key="btn_load"):
        data = st.session_state.bank_data
        user = find_user(data, up_acc.strip(), up_pin)
        if not user:
            st.markdown('<div class="alert-error">⚠ Invalid account number or PIN.</div>', unsafe_allow_html=True)
        else:
            st.session_state["update_user"] = user

    if "update_user" in st.session_state:
        u = st.session_state["update_user"]
        st.markdown('<hr>', unsafe_allow_html=True)
        st.caption("Leave a field unchanged to keep the current value.")

        new_name  = st.text_input("Name", value=u["name"], key="up_name")
        new_email = st.text_input("Email", value=u["email"], key="up_email")
        col1, col2 = st.columns(2)
        with col1:
            new_pin  = st.text_input("New PIN (leave blank to keep)", type="password", max_chars=4, key="up_new_pin")
        with col2:
            new_pin2 = st.text_input("Confirm New PIN", type="password", max_chars=4, key="up_new_pin2")

        if st.button("Save Changes", key="btn_update"):
            errors = []
            if not new_name.strip():
                errors.append("Name cannot be empty.")
            if not validate_email(new_email):
                errors.append("Enter a valid email address.")
            if new_pin:
                if not new_pin.isdigit() or len(new_pin) != 4:
                    errors.append("PIN must be exactly 4 digits.")
                elif new_pin != new_pin2:
                    errors.append("PINs do not match.")

            if errors:
                for e in errors:
                    st.markdown(f'<div class="alert-error">⚠ {e}</div>', unsafe_allow_html=True)
            else:
                u["name"]  = new_name.strip()
                u["email"] = new_email.strip().lower()
                if new_pin:
                    u["pin"] = int(new_pin)
                save_data(st.session_state.bank_data)
                del st.session_state["update_user"]
                st.markdown('<div class="alert-success">✅ Details updated successfully.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — Close Account
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="card"><div class="card-title">Close account</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-warn">⚠ This action is permanent and cannot be undone.</div>', unsafe_allow_html=True)

    del_acc = st.text_input("Account Number", key="del_acc")
    del_pin = st.text_input("PIN", type="password", max_chars=4, placeholder="••••", key="del_pin")
    confirm = st.checkbox("I understand this will permanently delete my account and all data.", key="del_confirm")

    if st.button("Close Account", key="btn_delete"):
        if not confirm:
            st.markdown('<div class="alert-error">⚠ Please confirm by checking the box above.</div>', unsafe_allow_html=True)
        else:
            data = st.session_state.bank_data
            user = find_user(data, del_acc.strip(), del_pin)
            if not user:
                st.markdown('<div class="alert-error">⚠ Invalid account number or PIN.</div>', unsafe_allow_html=True)
            else:
                data.remove(user)
                save_data(data)
                st.session_state.bank_data = data
                st.markdown('<div class="alert-success">✅ Account closed. All data has been removed.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#2A3A5A; font-size:0.72rem; margin-top:3rem; padding-bottom:2rem; letter-spacing:0.08em;">
  NexBank © 2026 &nbsp;·&nbsp; Built with Streamlit &nbsp;·&nbsp; Your data stays local
</div>
""", unsafe_allow_html=True)