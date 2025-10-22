Comment Board

A tiny Flask app where you can post comments that expire after a few minutes.

How to run

Clone repo:

git clone https://github.com/FANG19946/comment-board.git
cd comment-board


Make a virtual environment and activate it:

python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate


Install Flask:

pip install Flask


Run the app:

python app.py


Open http://127.0.0.1:5000
 in your browser.

Features

Post comments with your name

Comments expire automatically after 2 minutes

Dark theme with a “Add Comment” page

Notes

TTL can be changed in app.py (TTL_SECONDS)

JSON file stores all comments: data/comments.json

Team

Adnan Khan