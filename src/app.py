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
count = 0
won = False


@app.route("/")
def index():
    return render_template("index.html", color=f"#{color}", hex=color, attempts=attempts, victory=False, count=count)

@app.route("/check", methods=["POST"])
def check():
    global count
    count += 1
    attempt = []
    answers = request.form.values()
    victory = True
    i = 0
    
    for input in answers:
        if input == color[i]:
            correct = "correct"
        elif input in color:
            correct = "partial"
            victory = False
        else:
            correct = "incorrect"
            victory = False
        attempt.append({"value": input, "correct": correct})
        i += 1
    attempts.append(attempt)
    
    if victory:
        global won
        won = True
        return redirect("/victory")
    else:
        return redirect("/")
    
@app.route("/victory")
def victory():
    if won:
        # return render_template("index.html", color=f"#{color}", hex=color, attempts=attempts, victory=True, count=count)
        return render_template("victory.html", color=color)
    return redirect("/")