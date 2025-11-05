from flask import Flask, render_template, request, jsonify
import feedparser
from bs4 import BeautifulSoup
import pytz
from email.utils import parsedate_to_datetime

app = Flask(__name__)

RSS_FEEDS = {
    "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
    "Euro Gamer": "https://www.eurogamer.net/feed/features",
    "Tech News": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "The Guardian – World": "https://www.theguardian.com/world/rss",
    "GP Blog (F1)": "https://www.gpblog.com/en/sitemap/news.xml"
}

def sanitize_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup(["script", "style"]):
        tag.decompose()
    return soup.get_text()

def convert_time(published_str):
    try:
        published_dt = parsedate_to_datetime(published_str)
        ist = pytz.timezone("Asia/Kolkata")
        gmt_time = published_dt.astimezone(pytz.timezone("GMT")).strftime("%d %b %Y, %I:%M %p GMT")
        ist_time = published_dt.astimezone(ist).strftime("%d %b %Y, %I:%M %p IST")
        return f"{gmt_time} / {ist_time}"
    except Exception:
        return published_str

def extract_image(entry):
    image = None
    if "media_content" in entry:
        image = entry.media_content[0].get("url")
    elif "links" in entry:
        for l in entry.links:
            if l.get("type", "").startswith("image"):
                image = l.get("href")
    return image

@app.route("/")
def index():
    source = request.args.get("source", "All")
    entries = []

    if source == "All":
        for name, url in RSS_FEEDS.items():
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                summary = sanitize_html(entry.get("summary", ""))
                words = summary.split()
                summary = " ".join(words[:30]) + ("..." if len(words) > 30 else "")

                entries.append({
                    "title": entry.title,
                    "link": entry.link,
                    "summary": summary,
                    "time": convert_time(entry.get("published", "")),
                    "published": entry.get("published_parsed"),
                    "source": name,
                    "image": extract_image(entry)
                })

        entries.sort(key=lambda x: x["published"] or 0, reverse=True)

    else:
        feed_url = RSS_FEEDS.get(source, RSS_FEEDS["The Hindu"])
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:20]:
            summary = sanitize_html(entry.get("summary", ""))
            words = summary.split()
            summary = " ".join(words[:30]) + ("..." if len(words) > 30 else "")

            entries.append({
                "title": entry.title,
                "link": entry.link,
                "summary": summary,
                "time": convert_time(entry.get("published", "")),
                "published": entry.get("published_parsed"),
                "source": source,
                "image": extract_image(entry)
            })

    return render_template("index.html", entries=entries, sources=["All"] + list(RSS_FEEDS.keys()), current_source=source)

@app.route("/article")
def article():
    link = request.args.get("link")
    source = request.args.get("source", "The Hindu")
    feed_url = RSS_FEEDS.get(source, RSS_FEEDS["The Hindu"])
    feed = feedparser.parse(feed_url)

    article = None
    for entry in feed.entries:
        if entry.link == link:
            summary = sanitize_html(entry.get("summary", ""))
            words = summary.split()
            summary = " ".join(words[:70]) + ("..." if len(words) > 70 else "")

            article = {
                "title": entry.title,
                "summary": summary,
                "time": convert_time(entry.get("published", "")),
                "link": entry.link,
                "image": extract_image(entry)
            }
            break

    return render_template("article.html", article=article, source=source)

@app.route("/refresh")
def refresh():
    source = request.args.get("source", "All")
    articles = []

    if source == "All":
        for name, url in RSS_FEEDS.items():
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                summary = sanitize_html(entry.get("summary", ""))
                words = summary.split()
                summary = " ".join(words[:30]) + ("..." if len(words) > 30 else "")

                articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "summary": summary,
                    "time": convert_time(entry.get("published", "")),
                    "published": entry.get("published_parsed"),
                    "source": name,
                    "image": extract_image(entry)
                })

        articles.sort(key=lambda x: x["published"] or 0, reverse=True)

    else:
        feed_url = RSS_FEEDS.get(source, RSS_FEEDS["The Hindu"])
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:20]:
            summary = sanitize_html(entry.get("summary", ""))
            words = summary.split()
            summary = " ".join(words[:30]) + ("..." if len(words) > 30 else "")

            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": summary,
                "time": convert_time(entry.get("published", "")),
                "published": entry.get("published_parsed"),
                "source": source,
                "image": extract_image(entry)
            })

    return jsonify({"articles": articles})

if __name__ == "__main__":
    app.run(debug=True)
