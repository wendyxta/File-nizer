# File-nizer
**Your automated file system organizer.**

# Motivation
We often downloads lots of random things on our computer on a daily basis. Most of the time, they end up piling up in our \Downloads folder, and become hard to find. We then need to waste precious time going through the tedious process of dragging and dropping files to our desired location.

# Solution
- End-to-end automation tool to organize loose files across the file system 
- Configurable file classification and rerouting through a YAML rule engine 
- Google Sheets API integration to log file movements, file paths, and timestamps
- Flask-based web dashboard to trigger file organization, review file movement logs, and monitor activity

# Tech Stack
- Python
- Flask, HTML
- Google Sheets API
- Vercel Cloud Deployment

# Instructions
- Create a Google Sheets API service account and add the service_account.json file to project directory
- Create a config.yaml file with desired keywords and extension rules for customized file classificaiton
- Create virtual environment `python -m venv .venv` and activate using `.venv\Scripts\activate`
- Install the requried modules listed in requriements.txt with `pip install -r requriements.txt`
- Run File-nizer! `python app.py`