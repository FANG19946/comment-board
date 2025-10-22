import json
import os
import time
from flask import Flask, render_template, request, redirect, url_for


DATA_FILE = "data/comments.json"

def load_comments():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_comments(comments):
    # Save List as JSON
    with open(DATA_FILE, "w") as f:
        json.dump(comments, f, indent=2)



app = Flask(__name__)

@app.context_processor
def inject_time():
    """Make `time` available in Jinja templates."""
    import time
    return dict(time=time)


# Setting up the routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "Anonymous")
        text = request.form.get("text", "").strip()
        if text:
            comments = load_comments()
            comments.append({
                "name": name,
                "text": text,
                "timestamp": time.time()
            })
            save_comments(comments)
        return redirect(url_for("index"))

    comments = load_comments()
    # Show newest comments first
    comments = sorted(comments, key=lambda x: x["timestamp"], reverse=True)
    return render_template("index.html", comments=comments)



if __name__ == "__main__":
    app.run(debug=True)


