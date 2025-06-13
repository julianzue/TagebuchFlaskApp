from flask import Flask, render_template, redirect, url_for, request
import time
import os
import json

data = "static/data.json"

app = Flask(__name__)


if not os.path.exists(data):
    with open(data, "w") as file:
        json.dump([], file, indent=4)


@app.route("/", methods=["POST", "GET"])
def start():

    if request.method == "POST":
        if "search" in request.form:
            query = request.form.get("query")

            with open(data, "r") as file:
                content = json.load(file)

            content_search = []

            for item in content:
                if query.lower() in item["title"].lower() or query in item["date"] or query.lower() in " ".join(item["content"]).lower():
                    content_search.append(item)

            if len(content_search) == 1:
                text = "Ergebnis"
            else:
                text = "Ergebnisse"

            if query != "":
                return render_template("search.html", content=content_search, query=query, count=len(content_search), text=text)
            else:
                pass

    with open(data, "r") as file:
        content = json.load(file)

    return render_template("start.html", content=content)


@app.route("/neu", methods=["POST", "GET"])
def new():

    if request.method == "POST":
        if "add" in request.form:
            title = request.form.get("title")
            content = request.form.get("content")
            d = time.strftime("%Y-%m-%d %H:%M:%S")

            with open(data, "r") as file:
                content_file = json.load(file)

            content_file.append(
                {
                    "title": title,
                    "date": d,
                    "content": str(content).split("\n")
                }
            )

            with open(data, "w") as file:
                json.dump(content_file, file, indent=4)

    return render_template("new.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")