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

#sd == start data
sd = {
    'n' : 1000,
    'T_star' : 40,
    'T_zero' : 70,
    'T_amb' : 23,
    'kp' : 1,
    'Tp' : 0.5,
    'Ti' : 0.5,
    'Td' : 1,
    'A' : 5,
    'e' : 0.6,
    'W' : 4,
    'S' : 2

}

@app.route('/getmethod/<jsdata>')
def get_javascript_data(jsdata):
    print(f"### {jsdata}")
    return jsdata

@app.route('/_generate', methods = ['GET'])
def generate():
    global uar
    uar = UAR(sd['n'], sd['T_star'], sd['T_zero'], sd['T_amb'], sd['kp'], sd['Tp'], sd['Ti'], sd['Td'], sd['A'], sd['e'], sd['W'], sd['S'])
    return jsonify(msg=1)

@app.route('/_stuff', methods = ['GET'])
def stuff():
    # return jsonify(result=random.randint(0, 10))
    # for i in range(100):
    a = uar.get_step()
    # a = uar.get_test()
    print(f"[PYTHON_LOG] - {a}")
    print(f"[LOG] - Next value: {a}")
    return jsonify(result=a)

@app.route("/")
@app.route("/home")
def home():
    a = 1
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
