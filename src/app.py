from flask import Flask, render_template, request, redirect
from random import randrange

app = Flask(__name__)

def random_color():
    """ Return a random hexcode """
    color = ""
    for i in range(3):
        color += str(hex(randrange(0, 255)))[2:].zfill(2).upper()
    return color

def reset():
    """ Reset game global variables """
    global color
    global attempts
    global count
    global end
    global won
    global correct_digits
    global partial_digits
    global incorrect_digits
    global key_classes
    
    color = random_color()
    attempts = []
    count = 0
    end = False
    won = False
    correct_digits = []
    partial_digits = []
    incorrect_digits = []
    key_classes = {}

reset()

MAX_ATTEMPTS = 10

dark_mode = False
limited_mode = False

@app.route("/")
def index():
    """ Generate main page """
    return render_template("index.html", color=f"#{color}", hex=color, attempts=attempts, max=MAX_ATTEMPTS, end=end, victory=won, count=count, key_classes=key_classes, dark_mode=dark_mode, limited_mode=limited_mode)

@app.route("/check", methods=["POST"])
def check():
    """ Check the user's guess """
    global count
    count += 1
    attempt = []
    answers = request.form.values()
    victory = True
    guessed_color = "#"
    length = len(color)
    
    digits = [input.upper() for input in answers]
    remaining = [digit for digit in color]
    partial_guesses = []
    for i in range(length):
        digit = digits[i]
        if digit == color[i]:
            correct = "correct"
            remaining[i] = ""
            key_classes[digit] = "correct"
        elif digit in color:
            partial_guesses.append({"digit": digit, "index": i})
            correct = "incorrect"
            victory = False
        else:
            correct = "incorrect"
            victory = False
            key_classes[digit] = "incorrect"
        attempt.append({"value": digit, "correct": correct})
        guessed_color += digit
    
    for guess in partial_guesses:
        if guess["digit"] in remaining:
            index = remaining.index(guess["digit"])
            attempt[guess["index"]]["correct"] = "partial"
            remaining[index] = ""
            key_classes[guess["digit"]] = "partial"
            
    attempts.append({"attempt": attempt, "color": guessed_color})
    
    if victory:
        global won
        global end
        
        won = True
        end = True
    elif limited_mode and count >= MAX_ATTEMPTS:
        end = True
    return redirect("/")

@app.route("/new")
def new():
    """ Start a new game """
    reset()
    return redirect("/")

@app.route("/settings", methods=["GET", "POST"])
def settings():
    """ Modify settings variables """
    if request.method == "POST":
        settings = request.form
        
        global dark_mode
        global limited_mode
        
        dark_mode = settings.get("darkMode") == "true"
        limited_mode = settings.get("limitedMode") == "true"
        
        return settings
    else:
        return {"dark_mode": dark_mode, "limited_mode": limited_mode}
    
@app.route("/data")
def data():
    """ Send informative variables """
    data = {
        "count": count,
        "max_attempts": MAX_ATTEMPTS
    }
    return data

@app.route("/lose")
def lose():
    """ End game without victory """
    global end
    end = True
    return redirect("/")