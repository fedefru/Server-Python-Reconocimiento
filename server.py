import ReconocimientoFacial
from flask import Flask,request,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

#python -m flask run  || Para ejecutar

@app.route('/reconocimiento')
def reco_ok():
    return ReconocimientoFacial.reconocimientoRostro()

app.run()
app.run(port=5000)  