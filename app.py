from flask import Flask, render_template, request
from bot import OrganizerBot
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def organize():
    message=""
    total_files = "-"
    today_files = "-"
    time_saved = "-"

    if request.method == "POST":
        my_bot = OrganizerBot()

        summary = my_bot.organize_downloads()
        total_files = summary[0]
        today_files = summary[1]
        time_saved = str("{:.2f}".format(summary[2])) + " minutes"
        message = "Your files have been organized!"

    return render_template("dashboard.html", message=message, total_files=total_files, today_files=today_files, time_saved=time_saved)

if __name__ == "__main__":
    app.run(debug=True)