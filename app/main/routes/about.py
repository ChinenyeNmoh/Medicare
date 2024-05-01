from flask import Flask, render_template

from app.main.routes import main

@main.route('/about', strict_slashes=False)
def about():
    return render_template('about.html', title= "aboutPage")