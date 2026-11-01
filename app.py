from flask import Flask, render_template, request
from bot import OrganizerBot
from datetime import datetime

"""
This app handles the Flask web interface route for the main dashboard page.
"""
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def organize():
    """
    GET:
        Renders the main dashboard page with default vlaues.

    POST:
        Creates an OrganizerBot instance to trigger file organization. 
        Retrieves summary statistics and renders the dashboard with updated values.

    @return: a rendered HTML template with an organization status message, the total number of files organizes, 
    the number of files organzed today, and the amount of time saved.
    """
    message=""
    total_files = "-"
    today_files = "-"
    time_saved = "-"

    if request.method == "POST":
        my_bot = OrganizerBot()
        start = datetime.now()
        summary = my_bot.organize_downloads()
        end = datetime.now()
        print("Organized files in " + str(end-start) + "ms.")
        message = summary[0]
        stats = summary[1]

        total_files = stats[0]
        today_files = stats[1]
        time_saved = str("{:.2f}".format(stats[2])) + " minutes"
        
    return render_template("dashboard.html", message=message, total_files=total_files, today_files=today_files, time_saved=time_saved)

if __name__ == "__main__":
    app.run(debug=True)