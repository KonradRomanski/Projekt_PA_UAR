from flask import Flask, render_template, jsonify
import random
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
# flask run

def z(a):
    return a*2*(-1)
@app.route('/_stuff', methods = ['GET'])
def stuff():
    return jsonify(result=random.randint(0, 10))

@app.route("/")
@app.route("/home")
def home():
    a = 1
    return render_template('home.html', temp = z(a))

if __name__ == '__main__':
    app.run(debug=True)
