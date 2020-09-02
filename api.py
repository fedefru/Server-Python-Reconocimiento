from flask import Flask
app = flask(__main__)

@app.route('/reconocimiento')
def test():
    return 'Hello world'