import json
import os
import time
from flask import Flask, render_template, request, redirect, url_for


DATA_FILE = "data/comments.json"


# Time Limit of Comments
TTL_SECONDS = 60 * 2  # 2 minutes for demo

def load_comments():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            comments = json.load(f)
    except json.JSONDecodeError:
        comments = []

    for c in comments:
        if "likes" not in c:
            c["likes"] = 0


    # Filter expired comments
    now = time.time()
    comments = [c for c in comments if now - c["timestamp"] < TTL_SECONDS]
    save_comments(comments)

    return comments



def save_comments(comments):
    # Save List as JSON
    with open(DATA_FILE, "w") as f:
        json.dump(comments, f, indent=2)



app = Flask(__name__)

@app.context_processor
def inject_time():
    """Make `time` available in Jinja templates."""
    import time
    return dict(time=time, TTL_SECONDS=TTL_SECONDS)


# Setting up the routes
@app.route("/")
def home():
    comments = load_comments()
    comments = sorted(comments, key=lambda x: (-x["likes"], -x["timestamp"]))
    return render_template("home.html", comments=comments, TTL_SECONDS=TTL_SECONDS, active_page='home')


# 📝 Post page - add comment
@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "POST":
        name = request.form.get("name", "Anonymous").strip()
        text = request.form.get("text", "").strip()
        if text:
            comments = load_comments()
            comments.append({
                "name": name,
                "text": text,
                "timestamp": time.time()
            })
            save_comments(comments)
        return redirect(url_for("home"))

    return render_template("post.html", active_page='post')


# Adding Likes
from flask import jsonify

@app.route("/like/<int:comment_index>", methods=["POST"])
def like(comment_index):
    comments = load_comments()
    if 0 <= comment_index < len(comments):
        comments[comment_index]["likes"] += 1
        save_comments(comments)
        return jsonify({"likes": comments[comment_index]["likes"]})
    return jsonify({"error": "Invalid index"}), 400


if __name__ == "__main__":
    app.run(debug=True)