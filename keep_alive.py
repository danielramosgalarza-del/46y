from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "🐢 Galapagos Bot está ONLINE y funcionando."

def run():
    # Render busca aplicaciones en el puerto 0.0.0.0
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()