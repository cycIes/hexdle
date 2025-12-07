A “design document” for your project in the form of a Markdown file called DESIGN.md that discusses, technically, how you implemented your project and why you made the design decisions you did. Consider your design document your opportunity to give the staff a technical tour of your project underneath its hood.

# The Project Design
The project is a monolithic website using Flask in Python, HTML, Javascript, and CSS.

## Flask and Python
Flask renders HTML templates and handles the game logic inside the routes. I chose to program the game logic in Python because I had more confidence in Python, and I wanted to separate the game logic from the user interface logic.
The main route (/) renders index.html with important game variables, including the status of the game.
Upon loading, Flask sets certain game variables like the color the user has to guess and resets containers for holding information about the user's game, like the user's guesses and the status of the round. 
When a user submits their guess, index.html posts the guess to the /check route. When Flask receives the guess, it records the guess and the correct, partially correct, and incorrect digits in the guess, and then its determines if the user has won, lost, or neither. If the game has ended, the check function updates the status of game and redirects the user to the main route.
The /lose route, when called, updates the game status and reloads the page to end the game without a victory.
The /new route resets the game variables, generates a new random hexcode answer, and reloads the main page.
The /settings route updates the settings dictionary, which contains information about the user's preferred color scheme and game mode.
The /data route sends a dictionary of certain variables about the game required by JavaScript.

## HTML and CSS
The main html file, index.html, extends the boilerplate code in base.html.
Jinja provides a convenient method of accessing server-side variables about the game and helps modify the html based on variables sent from Flask.
Bootstrap aids the HTML and CSS files with its custom classes, components, and variables. Bootstrap offers convenient, already designed features and aids in consistency. I use several different classes to modify the appearance of elements. The two components I use are modals and switches. I use modals to show additional information without leaving the page, and use switches for aesthetic settings toggles. For styles, I make use of existing color variables for readability and a consistent palette.

### Header and Clue
At the top of the page is the title, a toolbar, and the color the user must guess. I use Jinja inside a script tag to easily set the color on the box. The toolbar links to the information and settings modals, so that the website provides enough readability and customizability without cluttering the main page.

### User Input Fields
In the middle of the page are a series of input fields. One row is for the user to type into, and the others either exist as a part of previous guesses or show how many guesses the user has left.

### Keyboard
On computer, the keyboard provides an alternate method of typing. When the user receives colored feedback after submitting a guess, the corresponding keys on the keyboard will also change to the appropriate color.

### Modals
I use three modals for the information cards and settings tab. 
In addition, I display user's results upon ending the game in a modal. I believe this method is more aesthetic and cohesive.

## Javascript
There are two Javascript sources, one inside a script tag in index.html, and index.js, which is linked to index.html. Javascript handles the functionality and dynamic aesthetics of the website.

### Internal Script Element
When the page loads, JavaScript checks if each key has a special class, sent in a list from Flask, and assigns the class if it exists. These classes represent the three results of a guess, correct, partially correct, and incorrect.
Depending on whether the game has ended or not, JavaScript may show a special results modal with the aid of Jinja.

### External Script
The external script includes most of the webpage functionality. The main functions are user keyboard behavior for the input fields and settings for the game. 
