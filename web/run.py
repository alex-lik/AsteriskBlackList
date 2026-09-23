"""Flask web interface for managing the Asterisk blacklist."""

import os

from flask import Flask, redirect, render_template, request

import db

app = Flask(__name__)


@app.route("/blacklist", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def black_list():
    message = None
    if request.method == "POST":
        phone = (request.form.get("phone") or "").strip()
        comment = (request.form.get("comment") or "").strip().replace(" ", "_")
        success, message, _normalized = db.add_phone(phone, comment)

    entries = db.get_blacklist()
    return render_template("blacklist.html", black_list=entries, message=message)


@app.route("/delete/<phone>")
def delete(phone):
    db.del_phone(phone)
    return redirect("/blacklist")


if __name__ == "__main__":
    app.run(
        host=os.getenv("WEB_HOST", "0.0.0.0"),
        port=int(os.getenv("WEB_PORT", "81")),
        debug=os.getenv("WEB_DEBUG", "false").lower() == "true",
    )
