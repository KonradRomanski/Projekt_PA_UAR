from flask import Flask, render_template, jsonify, request
import random
from UAR import UAR
app = Flask(__name__)


sd = {
    'n' : 1,
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


with app.app_context():
    print("[LOG] - data are created")
    uar = UAR(sd['n'], sd['T_star'], sd['T_zero'], sd['T_amb'], sd['kp'], sd['Tp'], sd['Ti'], sd['Td'], sd['A'], sd['e'], sd['W'], sd['S'])


# sets values
@app.route('/getmethod/<jsdata>')
def get_javascript_data(jsdata):
    print(f"###[PYLOG] {jsdata}")
    jsdata_list = list(map(float, jsdata.split(',')))
    #print(f"{jsdata_list}")
    #sd['n'] = jsdata_list[0]
    sd['n'] = jsdata_list[0]
    sd['T_star'] = jsdata_list[1]
    sd['T_zero'] = jsdata_list[2]
    sd['T_amb'] = jsdata_list[3]
    sd['kp'] = jsdata_list[4]
    sd['Tp'] = jsdata_list[5]
    sd['Ti'] = jsdata_list[6]
    sd['Td'] = jsdata_list[7]
    sd['A'] = jsdata_list[8]
    sd['e'] = jsdata_list[9]
    sd['W'] = jsdata_list[10]
    sd['S'] = jsdata_list[11]
    print(f"[LOG] - Received data: {sd}")
    if sd['n'] == 1:
        uar.update_values(sd['n'], sd['T_star'], sd['T_zero'], sd['T_amb'], sd['kp'], sd['Tp'], sd['Ti'], sd['Td'], sd['A'], sd['e'], sd['W'], sd['S'])
        print(f"[LOG] - Updating object...")
    if sd['n'] == 0:
        uar.restart_values(sd['n'], sd['T_star'], sd['T_zero'], sd['T_amb'], sd['kp'], sd['Tp'], sd['Ti'], sd['Td'], sd['A'], sd['e'], sd['W'], sd['S'])
        print(f"[LOG] - Restarting object...")

    print(f"[LOG] - done")
    return jsdata


# returns next value
@app.route('/_stuff', methods = ['GET'])
def stuff():
    a = uar.get_step()
    b = round(uar.uvar(),4)
    c = round(uar.pvar(),4)
    d = round(uar.cvar(),4)
    print(f"[LOG] - Next value: {a}, Uchyb ustalony: {b}, Przeregulowanie: {c}, Czas regulacji: {d}")
    return jsonify(A = a, B = b, C = c, D = d)


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
