import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "Fresher_drive_63"

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
    "id card": "🪪 ID Card is provided by the coordinator after few weeks of session start in respective class.,",
    "identity card": "🪪 Identity card is issued by coordinator after few weeks of session start in respective class.",
    "hostel": "🏠 hostels are available in the bbd group of institutions, but not in the university itself. 4th (girls hostel) and {2 boys hostels(4-blocks)}",
    "scholarship": "💰 Apply for UP Scholarship and submit the application form and required documents in DSW office.",
    "wifi": "📶 Campus WiFi is available on specific wing.",
    "bus": "🚌 College provides bus transport for student and teachers",
    "vehicle": "🚗 Students are allowed to bring vehicles. And they have to get permission card provide by authority . It form provide  by coordinator few week after session start. ",
    "bike": "🚗 Bike and car are allowed on permission card .",
    "dress code": "👕 Black/blue jeans & white shirt",
    "uniform": "👕 Students usually wear white shirts and black/blue pants.",
    "Clubs": "🎭 Various clubs and societies are active on campus, including cultural, technical, and sports clubs , Like Alankar , Aaina , Udaan , NSS etc. ",
    "program": "🎉 BBD University organizes programs on specific occasions and on auditorium and campus.",
    "event": "🎉 College conducts events like Utkarsh , star night..",
    "star night": "🌟 Star night is organise on 31 march (founder day)",
    "utkarsh": "🏆 Utkarsh fest is held annually in february it goes 3 days and last day is celebrate as DJ Night.",
    "campus": "🏫 BBD campus includes various facilities and buildings,like Auditorium, Canteen , Stadium, Cafe , Parking",
    "exam": "📝 Exams are conducted semester-wise .  ",
    "attendance": "📊 Minimum attendance rules 75%",
    "lost id": "🪪 If ID card is lost then contact the class coordinator.",
    "placement": "🎓 Placement details available in 3rd & 4th year ",
    "DSW Office": "👩‍🎓 DSW office is located on the front of Pnb atm ",
    "Bank": "🏦 There is a PNB bank branch on the campus and pnb atm also available in campus.",
    "E-sports": "🎮 E-sports club is active in the campus and organize various gaming events and tournaments.",
    "sports": "⚽ Sports facilities include a stadium and various sports courts for basketball, volleyball, and badminton.",
    "job": "🎓 Job-related information is available in the placement cell.",
    "late fees": "💰 Late fees may apply if you are not able to submit the fees  on time..",
    "canteen": "🍽️ The college has a canteen which have various food options.Provide campus 1 kharray canteen , 1 nescafe , and canteen next to the auditorium",
    "fees": "💰 Fees structure is available at the accounting office or admission cell",
    "Lab": "🔬 There are multiple labs.1st- year {Lower ground floor(LGF)} workshop , Graphics lab , electrical lab , mechanics lab ",
    "Dean of SOE ": "On fifth floor, there is the office of Dean of School of Engineering.",
    "placement cell": "🎓 Placement cell is located on the 1st floor.",
    "examination cell": "📝 Examination cell is located on the 1st floor & 8th floor (teacher)",
    "admission cell": "🎓 Admission cell is located on Near on behind auditorium and front of akhilesh das gupta stadium.",
    "contact": "📞 For queries visit website (https://bbdu.ac.in/)"
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

        # SAFE: ignore extra fields (no crash)
        request.form.get("number")
        request.form.get("branch")
        request.form.get("id_card")

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (name, email, password, role))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")
# ===================== LOGIN =====================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

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
    app.run(host="0.0.0.0", port=10000)