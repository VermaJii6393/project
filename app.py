import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "secret123"

# ===================== DATABASE =====================
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT,
        role TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ===================== COLLEGE AI DATA (SAFE) =====================
data = {
    "library": "📚 BBD University Library is located on the 6th floor...",
    "library card": "📚 Freshers receive library cards...",
    "id card": "🪪 ID Card is provided by the coordinator...",
    "identity card": "🪪 Identity card is issued by coordinator...",
    "hostel": "🏠 Hostel facility is available...",
    "scholarship": "💰 Apply for UP Scholarship...",
    "wifi": "📶 Campus WiFi is available...",
    "bus": "🚌 College provides bus transport...",
    "vehicle": "🚗 Students are allowed to bring vehicles...",
    "bike": "🚗 Bike or car entry is allowed...",
    "dress code": "👕 College dress code includes...",
    "uniform": "👕 Students usually wear...",
    "program": "🎉 BBD University organizes programs...",
    "event": "🎉 College conducts events...",
    "star night": "🌟 Star Night is a major event...",
    "utkarsh": "🏆 Utkarsh is a major fest...",
    "campus": "🏫 BBDU campus includes...",
    "exam": "📝 Exams are conducted semester-wise...",
    "attendance": "📊 Minimum attendance rules...",
    "lost id": "🪪 If ID card is lost...",
    "placement": "🎓 Placement details available...",
    "job": "🎓 Job-related info available...",
    "late fees": "💰 Late fees may apply...",
    "canteen": "🍽️ The college has a canteen...",
    "fees": "💰 Fees info at ground floor...",
    "contact": "📞 For queries visit website..."
}

# ===================== CHAT STORAGE =====================
chat_messages = []

# ===================== HOME =====================
@app.route("/")
def home():
    return render_template("index.html", user=session.get("user"), role=session.get("role"))

# ===================== SIGNUP =====================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                  (name, email, password, role))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")

# ===================== LOGIN =====================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()

        conn.close()

        if user:
            session["user"] = user[1]
            session["role"] = user[4]
            return redirect("/")
        else:
            return "Invalid email or password"

    return render_template("login.html")

# ===================== LOGOUT =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ===================== AI CHAT =====================
@app.route("/ask", methods=["GET", "POST"])
def ask():
    answer = ""
    question = ""

    if request.method == "POST":
        question = request.form.get("question", "").lower()

        best_match = None
        best_score = 0

        for key in data:
            score = 0
            for word in key.split():
                if word in question:
                    score += 1

            if key in question:
                score += 2

            if score > best_score:
                best_score = score
                best_match = key

        if best_match:
            answer = data[best_match]
        else:
            answer = "🤖 Sorry, I don't have exact info."

    return render_template("ask.html", answer=answer, question=question)

# ===================== CONNECT =====================
@app.route("/connect")
def connect():
    return render_template("connect.html")

# ===================== CLASSROOM =====================
@app.route("/classroom")
def classroom():
    return render_template("classroom.html", messages=chat_messages)

@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.form.get("message")

    if message:
        chat_messages.append(message)

    return redirect(url_for("classroom"))

# ===================== RUN =====================
if __name__ == "__main__":
    app.run(debug=True)