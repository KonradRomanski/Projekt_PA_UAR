from flask import Flask, render_template, jsonify
import random
from UAR import UAR
app = Flask(__name__)

#FLASK SETUP
#-------------------------
#Windows:
# set FLASK_APP=main.py
# when above command isn't working:
# $env:FLASK_APP = "main"
#UNIX
#export FLASK_APP=main.py
#-------------------------
# when debug mode is needed
# $env:FLASK_DEBUG = 1 (for WIN)
# to run flask
# flask run

uar = UAR(1000, 320, 293.15, 293.15, 1, 0.005, 1, 10, 2, 0.6, 3, 2)

@app.route('/_stuff', methods = ['GET'])
def stuff():
    # return jsonify(result=random.randint(0, 10))
    return jsonify(result=uar.get_step())

@app.route("/")
@app.route("/home")
def home():
    a = 1
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
