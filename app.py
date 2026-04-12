chat_messages = []
from flask import Flask, render_template, request

app = Flask(__name__)

# ===================== COLLEGE AI DATA (OLD + SAFE) =====================
data = {

    # 📚 LIBRARY
    "library": "📚 BBD University Library is located on the 6th floor. Freshers can get a library card by filling a form provided by the coordinator and submitting it to the library office.",

    "library card": "📚 Freshers receive library cards after filling a form given by the class coordinator and submitting it in the library (6th floor).",

    # 🪪 ID CARD
    "id card": "🪪 ID Card is provided by the coordinator after a few weeks of admission. If lost, students can reissue it with help of their Class CR or Coordinator.",

    "identity card": "🪪 Identity card is issued by coordinator after some weeks. If lost, students must contact CR or coordinator for reissue.",

    # 🏠 HOSTEL
    "hostel": "🏠 Hostel facility is available with separate blocks for boys and girls. Contact hostel warden or coordinator for allocation.",

    # 💰 SCHOLARSHIP
    "scholarship": "💰 Apply for UP Scholarship through official portal. Documents must be submitted on time through college instructions.",

    # 📶 WIFI
    "wifi": "📶 Campus WiFi is available in academic blocks and hostels after registration in IT department.",

    # 🚌 TRANSPORT
    "bus": "🚌 College provides bus transport facilities across Lucknow routes for students and staff.",

    # 🚗 VEHICLE
    "vehicle": "🚗 Students are allowed to bring vehicles, but they must have a special vehicle permission card. This form is provided by the coordinator and must be placed on the vehicle for entry inside campus.",

    "bike": "🚗 Bike or car entry is allowed only with official vehicle permission card issued by coordinator.",

    # 👕 DRESS CODE
    "dress code": "👕 College dress code includes white shirt with black/blue trousers. It is recommended but not strictly mandatory.",

    "uniform": "👕 Students usually wear white shirt with black/blue trousers. It is not strictly enforced.",

    # 🎉 EVENTS
    "program": "🎉 BBD University organizes small programs regularly. Major events include 'Utkarsh' and 'Star Night' which are large annual celebrations.",

    "event": "🎉 College conducts multiple cultural and academic events. Major ones are Utkarsh and Star Night.",

    "star night": "🌟 Star Night is a major cultural event with performances, celebrities and student participation.",

    "utkarsh": "🏆 Utkarsh is a major annual fest of BBD University with competitions, cultural events and prizes.",

    # 🏫 CAMPUS
    "campus": "🏫 BBDU campus includes library, hostels, academic blocks, sports stadium, cafeteria and medical facilities.",

    # 📝 EXAM
    "exam": "📝 Exams are conducted semester-wise. Students should check official notices or department updates.",

    # 📊 ATTENDANCE
    "attendance": "📊 Minimum attendance rules are decided by department. Students should maintain regular attendance.",

    # 🪪 LOST ID HELP
    "lost id": "🪪 If ID card is lost, students should contact their Class CR or Coordinator for reissue procedure.",

    # 🎓 PLACEMENT
    "placement": "🎓 For placement details, students should visit the official BBD University website (bbdu.ac.in) or placement cell.",

    "job": "🎓 Placement and job-related information is available only on official university website or placement cell.",

    # 📞 CONTACT
    "contact": "📞 For official queries, visit bbdu.ac.in or contact university administration office."
}

# ===================== CLASSROOM CHAT STORAGE =====================
chat_messages = []

# ===================== HOME =====================
@app.route("/")
def home():
    return render_template("index.html")


# ===================== AI CHAT (IMPROVED VERSION) =====================
@app.route("/ask", methods=["GET", "POST"])
def ask():
    answer = ""
    question = ""

    if request.method == "POST":
        question = request.form["question"].lower()

        best_match = None
        best_score = 0

        # SMART MATCHING (IMPROVED AI LOGIC)
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
            answer = "🤖 Sorry, I don't have exact info. Please contact CR or admin."

    return render_template("ask.html", answer=answer, question=question)


# ===================== CONNECT PAGE =====================
@app.route("/connect")
def connect():
    return render_template("connect.html")


# ===================== CLASSROOM CHAT =====================
@app.route("/classroom")
def classroom():
    return render_template("classroom.html", messages=chat_messages)


@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.form["message"]

    if message:
        chat_messages.append(message)

    return render_template("classroom.html", messages=chat_messages)


# ===================== RUN APP ==================
if __name__ == "__main__":
    app.run(debug=True)