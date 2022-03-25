#Template inheritance, CSS exercise
from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import os

UPLOAD_FOLDER = './static'

app = Flask(__name__, template_folder='templates')

#For Workbench use 'localhost'
#For editor.computing use 'student.computing.dcu.ie'
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='mealtime'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

#This function will retrieve all recipe data from database
@app.route('/recipes', methods=['GET', 'POST'])
def recipes():

    cur = mysql.get_db().cursor()
    query1 = "SELECT * from mealtime.meal_time;"
    cur.execute(query1,)
    output = cur.fetchall()
    mysql.get_db().commit()
    cur.close()

    return render_template('Recipes.html', recipe = output)

@app.route('/search', methods=['GET', 'POST'])
def search():

    if request.method == 'POST':
        Recipe_Ingredient = request.form['Recipe_Ingredient']

        #Make everything lowercase
        Recipe_Ingredient = Recipe_Ingredient.lower()
        #Chop up into a list
        user_IngredientL = Recipe_Ingredient.split(',')
        cur = mysql.get_db().cursor()
        #Get all database rows first
        query1 = "SELECT * from mealtime.meal_time"
        cur.execute(query1)
        output = cur.fetchall()
        mysql.get_db().commit()
        cur.close()

        #Tuple of tuples is retrieved
        #Now find the rows that contain all user-entered ingredients
        #Create a new list to pass to HTML template
        newOut = []

        #For each row in database
        for row in output:
            #Use count to check #matches
            count = 0
            #For each user's term, if its Ingredients field contains it, add to count
            for user_term in user_IngredientL:
                if user_term in row[1].lower():
                    count = count + 1
            #If more than 4 matches, then add the whole row into the newOut
            if count >= 4:
                newOut.append(row)

        return render_template('filter_result.html', recipe = newOut)

    return render_template('Search.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        Recipe_Name = request.form['RecipeNameF']
        Recipe_Ingredient = request.form['RecipeIngredientF']
        Recipe_Description = request.form['RecipeDescriptionF']
        Recipe_Time = request.form['RecipeTimeF']
        #Get file1 object as file1
        file1 = request.files['RecipeImageF']
        #Then get filename as 'photo'
        Recipe_Image = file1.filename
        cur = mysql.get_db().cursor()

        #Upload a photo to a folder
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)

        query1 = "INSERT INTO mealtime.meal_time (Recipe_Name, Recipe_Ingredient, Recipe_Description, Recipe_Image, Recipe_Time) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query1, (Recipe_Name, Recipe_Ingredient, Recipe_Description, Recipe_Image, Recipe_Time))
        mysql.get_db().commit()
        cur.close()
        return render_template('Uploadmessage.html')

    return render_template('Upload.html')

#Use if in localhost environment
if __name__=='__main__':
    app.run(debug=True)

#Use in editor.computing.dcu.ie environment
#if __name__=='__main__':
#    app.run(host='0.0.0.0', port='8080', debug=True)
