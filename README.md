📰 RSS News Web Application

A Python and Flask-based web application that aggregates and displays live news from multiple RSS feeds in one place. The project fetches real-time updates from various sources including The Hindu, Tech News, Eurogamer, The Guardian — World, and GP Blog (F1).

When executed, the Python script runs a local web server and provides a browser link where users can view categorized news feeds. The front-end is built using HTML templates, while the backend uses Flask for routing and Feedparser for RSS data extraction.

⚙️ Features

Fetches and parses live RSS feeds from multiple trusted news sources

Categorized sections: All, The Hindu, Tech News, Eurogamer, The Guardian — World, GP Blog (F1)

Simple and clean HTML-based interface

Flask-powered backend with dynamic routing

Real-time updates upon page refresh

Lightweight and easy to run locally

🧰 Tech Stack

Languages: Python, HTML

Framework: Flask

Libraries Used: Feedparser, Jinja2, Werkzeug, Click, Blinker, MarkupSafe, itsdangerous, sgmllib3k

🚀 How to Run
  # Clone the repository
  git clone https://github.com/mahi-ayub/rss-news-webapp.git

  # Navigate to the project folder
  cd rss-news-webapp

  # Install dependencies
  pip install -r requirements.txt

  # Run the Flask app
  python app.py

  # Open the local server link displayed in your terminal
  

Developed During a 4-week internship at Brandlution, as part of the Python Web Development Internship under the Presidency University academic program (2025).
