from flask import Flask, render_template
from app.main.routes import main

@main.route('/', strict_slashes=False)
@main.route('/home', strict_slashes=False)
def home():
    return render_template('home.html', title= "homePage")