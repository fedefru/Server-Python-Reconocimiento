import ReconocimientoFacial, CapturoRostro
from flask import Flask,request,jsonify,send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

#python -m flask run  || Para ejecutar
#CapturoRostro.capturoRostro('FFrutos')

@app.route('/reconocimiento')
def reco_ok():
    return ReconocimientoFacial.reconocimientoRostro()

@app.route('/get_image')
def get_image():
    filename = request.args.get('filename')
    return send_file(filename, mimetype='image/jpg')
    #http://localhost:5000/get_image?filename=./Registros/FFrutos/FFrutos_2020-09-20T21-35-43.jpg
    #SELECT ruta_imagen from FICHAJES where USUARIO_ID = 11

app.run()
app.run(port=5000)  
