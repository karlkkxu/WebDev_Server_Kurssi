from flask import Flask, render_template, request, Response

app = Flask(__name__)
@app.route('/', methods=['POST','GET']) 
def peliLauta():
    p1 = " "
    p2 = " "
    koko = 8

    try:
        p1 = str(request.form.get("p1") or " ")
    except:
        p1 = "VITUN LAITON"

    try:
        p2 = str(request.form.get("p2") or " ")
    except:
        p2 = "VITUN LAITON"

    try:
        koko = int(request.form.get("koko") or 8)
    except:
        koko = 9999999

    return render_template("jinja.xhtml", koko=koko, p1=p1, p2=p2)