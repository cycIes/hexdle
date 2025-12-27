from flask import Flask, render_template, request, redirect
from random import randrange

app = Flask(__name__)

def reset():
    """ Reset game global variables """
    
    global color # The color the user has to guess
    global attempts # Stores information about previous attempts
    global count # Stores the number of attempts the user has made
    global end # Stores if the game has ended
    global won # Stores if the user won
    global key_classes # Stores classification for each digit guessed

    attempts = []
    count = 0
    end = False
    won = False
    key_classes = {}

reset()

# The maximum number of attempts a user has in limited guessing mode
MAX_ATTEMPTS = 10

dark_mode = False
limited_mode = False

@app.route("/")
def index():
    """ Generate main page """
    
    return render_template("index.html", dark_mode=dark_mode, limited_mode=limited_mode)

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