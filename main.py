from flask import Flask, render_template, request
from bot import OrganizerBot

app = Flask(__name__)
my_bot = OrganizerBot()

@app.route("/")
def organize():
    my_bot.organize_downloads()
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
