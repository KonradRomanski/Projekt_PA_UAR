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

# sets values
@app.route('/getmethod/<jsdata>')
def get_javascript_data(jsdata):
    # print(f"###[PYLOG] {jsdata}")
    jsdata_list = list(map(float, jsdata.split(',')))
    # print(f"{jsdata_list}")
    sd['n'] = jsdata_list[0];
    sd['T_star'] = jsdata_list[1];
    sd['T_zero'] = jsdata_list[2];
    sd['T_amb'] = jsdata_list[3];
    sd['kp'] = jsdata_list[4];
    sd['Tp'] = jsdata_list[5];
    sd['Ti'] = jsdata_list[6];
    sd['Td'] = jsdata_list[7];
    sd['A'] = jsdata_list[8];
    sd['e'] = jsdata_list[9];
    sd['W'] = jsdata_list[10];
    sd['S'] = jsdata_list[11];
    print(f"[LOG] - Received data: {sd}");

    print(f"[LOG] - Updating object...");
    uar.update_values(sd['n'], sd['T_star'], sd['T_zero'], sd['T_amb'], sd['kp'], sd['Tp'], sd['Ti'], sd['Td'], sd['A'], sd['e'], sd['W'], sd['S'])
    print(f"[LOG] - done");
    return jsdata

# creates the object
@app.route('/_generate', methods = ['GET'])
def generate():
    global uar
    uar = UAR(sd['n'], sd['T_star'], sd['T_zero'], sd['T_amb'], sd['kp'], sd['Tp'], sd['Ti'], sd['Td'], sd['A'], sd['e'], sd['W'], sd['S'])
    return jsonify(msg=1)

# returns next value
@app.route('/_stuff', methods = ['GET'])
def stuff():
    a = uar.get_step()
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
