#Template inheritance, CSS exercise
from flask import Flask, render_template

app = Flask(__name__, template_folder='template')

@app.route('/')
def login():
    return render_template("login.html", tag="login")

@app.route('/search')
def search():
    return render_template("Search.html", tag="search")

@app.route('/recipes')
def recipes():
    return render_template("recipes.html", tag="recipes")

@app.route('/socials')
def socials():
    return render_template("socials.html", tag="socials")

#Use if in localhost environment
if __name__=='__main__':
    app.run(debug=True)

#Use in editor.computing.dcu.ie environment
#if __name__=='__main__':   
#    app.run(host='0.0.0.0', port='8080', debug=True)
