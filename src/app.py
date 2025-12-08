from flask import Flask, render_template, request, redirect
from random import randrange

app = Flask(__name__)

def random_color():
    """ Return a random hexcode """
    
    color = ""
    # Generate random two digit hexadecimal numbers
    for i in range(3):
        color += str(hex(randrange(0, 255)))[2:].zfill(2).upper()
    return color

def reset():
    """ Reset game global variables """
    
    global color # The color the user has to guess
    global attempts # Stores information about previous attempts
    global count # Stores the number of attempts the user has made
    global end # Stores if the game has ended
    global won # Stores if the user won
    global correct_digits # Stores digits in the right place
    global partial_digits # Stores digits in the hexcode but not in the right place
    global incorrect_digits # Stores digits not in the hexcode
    global key_classes # Stores classification for each digit guessed
    
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

# The maximum number of attempts a user has in limited guessing mode
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
    
    # Classify every digit in the user's guess
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
            # Add digit as a possible partially correct guess
            partial_guesses.append({"digit": digit, "index": i})
            correct = "incorrect"
            victory = False
        else:
            correct = "incorrect"
            victory = False
            key_classes[digit] = "incorrect"
        # Store guess and feedback about the guess
        attempt.append({"value": digit, "correct": correct})
        guessed_color += digit
    
    # Check each possible partially correct guess
    for guess in partial_guesses:
        if guess["digit"] in remaining:
            index = remaining.index(guess["digit"])
            attempt[guess["index"]]["correct"] = "partial"
            remaining[index] = ""
            key_classes[guess["digit"]] = "partial"
            
    # Record the guess
    attempts.append({"attempt": attempt, "color": guessed_color})
    
    # Check if the user won or lost
    if victory:
        global won
        global end
        
        won = True
        end = True
    elif limited_mode and count >= MAX_ATTEMPTS:
        end = True
        
    # Reload main page
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
        
        # Set the modes to boolean values
        dark_mode = settings.get("darkMode") == "true"
        limited_mode = settings.get("limitedMode") == "true"
        
        return settings
    else:
        return {"dark_mode": dark_mode, "limited_mode": limited_mode}
    
@app.route("/data")
def data():
    """ Send informative variables """
    
    # Store variables in dictionary
    data = {
        "count": count,
        "max_attempts": MAX_ATTEMPTS
    }
    return data

@app.route("/lose")
def lose():
    """ End game without victory """
    
    # End game without victory
    global end
    end = True
    
    return redirect("/")