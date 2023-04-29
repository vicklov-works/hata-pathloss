import math
from flask import Flask, render_template, request
#import pickle


project = Flask(__name__)

#HATA = pickle.load(open('Hata.pkl', 'rb'))

@project.route('/')
def Home():
    return render_template ('index.html')

@project.route('/About')
def About():
    return render_template('About.html')

@project.route('/predict', methods=['POST'])
def predict():
    Environment_dict = {"OPEN_LAR": 0, "OPEN_MED": 1,  "SUBURBAN_LAR": 2, "SUBURBAN_MED": 3, "URBAN_LAR": 4, "URBAN_MED":5}
    Environment = Environment_dict[request.form.get("Environment")] 

    f =float(request.form.get("Frequency"))
    hb =float(request.form.get("BaseA_height"))
    hm =float(request.form.get("MobA_height"))
    d =float(request.form.get("Distance"))

    A = 69.55 + (26.16*math.log10(f)) - (13.82 * math.log10(hb))
    B = (44.9 - 6.55*math.log10(hb))*math.log10(d)
    C = 5.4 + (2 * ((math.log10(f/28))**2))
    D = 40.94 + (4.78*((math.log10(f))**2)) - (19.33 * math.log10(f))
    S = 0.8 + ((1.1 * math.log10(f) - 0.7) * hm) - (1.5*math.log10(f))
    L = (8.29 * ((math.log10(1.5*hm))**2)) - 1.1
    Lg = (3.2 * ((math.log10(11.75*hm))**2)) - 4.97

    urb_L = A + B - L;  urb_Lg = A + B - Lg;  urb_M = A + B - S
    open_L = urb_L - D;  open_Lg = urb_Lg - D;  open_M = urb_M - D
    sub_L = urb_L - C;  sub_Lg = urb_Lg - C;  sub_M = urb_M - C

    if Environment == 0 and f >= 400:
        return render_template("index.html", predicted = "The calculated path loss is {}".format(open_Lg))
    elif Environment == 0 and f <= 200:
        return render_template("index.html", predicted = "The calculated path loss is {}".format(open_L))
    elif Environment == 1:
        return render_template("index.html", predicted = "The calculated path loss is {}".format(open_M))
    elif Environment == 2 and f >= 400:
        return render_template("index.html", predicted = "The calculated path loss is {}".format(sub_Lg))
    elif Environment == 2 and f <= 200:
        return render_template("index.html", predicted = "The calculated path loss is {}".format(sub_L))
    elif Environment == 3:
        return render_template("index.html", predicted = "The calculated path loss is {}".format(sub_M))
    elif Environment == 4 and f >= 400:
        return render_template("index.html", predicted = "The calculated path loss is {}".format(urb_Lg))
    elif Environment == 4 and f <= 200:
        return render_template("index.html", predicted = "The calculated path loss is {}".format(urb_L))
    elif Environment == 5:
        return render_template("index.html", predicted = "The calculated path loss is {}".format(urb_M))
    else:
        return render_template("index.html", predicted = "Check your input and predict again!!!")



if __name__ == "__main__":
    project.run('127.0.0.1', 8080, debug=True)