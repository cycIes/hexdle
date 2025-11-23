from flask import Flask, render_template, request, redirect, jsonify
from random import randrange

app = Flask(__name__)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def random_color():
    color = ""
    for i in range(3):
        color += str(hex(randrange(0, 255)))[2:].zfill(2)
    return color

color = random_color()
attempts = []
victory = False


@app.route("/")
def index():
    # color = random_color()
    return render_template("index.html", color=f"#{color}", hex=color, attempts=attempts)

@app.route("/check", methods=["POST"])
def check():
    answer = [input for input in request.form.values()]
    length = len(color)
    correct = ["correct" if answer[i] == color[i] else "incorrect" for i in range(length)]
    attempt = [{"value": answer[i], "correct": correct[i]} for i in range(length)]
    attempts.append(attempt)
    info = {"feedback": correct, "victory": False in correct}
    if "incorrect" in correct:
        return redirect("/")
    else:
        return redirect("/victory")
    # return info
    
@app.route("/victory")
def victory():
    return None