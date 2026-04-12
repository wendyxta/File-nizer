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
        print(summary)
        message = summary[0]
        stats = summary[1]

        total_files = stats[0]
        today_files = stats[1]
        time_saved = str("{:.2f}".format(stats[2])) + " minutes"
        
    return render_template("dashboard.html", message=message, total_files=total_files, today_files=today_files, time_saved=time_saved)

if __name__ == "__main__":
    app.run(debug=True)