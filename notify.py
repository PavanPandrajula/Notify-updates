import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
# =========================
# 🔧 CONFIG
# =========================
URL = "https://bdl-india.in/recruitments"
LAST_FILE = "last_seen.txt"

# Gmail setup
EMAIL = "saipavanpandrajula@gmail.com"            # your Gmail
APP_PASSWORD = "xvufoiqflygvswao"   # 16-char app password from Google
TO_EMAIL = "saipavanpandrajula@gmail.com"    # where to send updates

# =========================
# 🔍 SCRAPE LATEST NOTICE
# =========================
def get_latest_notice():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    row = soup.select_one("table tbody tr")
    if not row:
        return None, None

    cols = row.find_all("td")
    title = cols[1].text.strip() if len(cols) > 1 else "New Notification"
    link = row.find("a")["href"] if row.find("a") else URL

    if link.startswith("/"):
        link = "https://bdl-india.in" + link

    return title, link

# =========================
# 💾 MEMORY FUNCTIONS
# =========================
def load_last_seen():
    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_seen(title):
    with open(LAST_FILE, "w") as f:
        f.write(title)

# =========================
# 📧 SEND EMAIL
# =========================
def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(msg)

# =========================
# 📢 MAIN CHECK
# =========================
def check_updates():
    title, link = get_latest_notice()
    if not title:
        return

    last_seen = load_last_seen()
    if title != last_seen:
        subject = "📢 New BDL Recruitment Update"
        body = f"{title}\n\n🔗 {link}"
        send_email(subject, body)
        save_last_seen(title)

# =========================
# ▶️ RUN ONCE
# =========================
if __name__ == "__main__":
    check_updates()
