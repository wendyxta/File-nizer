from flask import Flask, render_template, request
from bot import OrganizerBot

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def organize():
    message=""

    if request.method == "POST":
        my_bot = OrganizerBot()
        my_bot.organize_downloads()
        message = "Your files have been organized!"

    return render_template("dashboard.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)