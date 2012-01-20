import os
from flask import Flask, url_for, redirect

app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_map():

    return redirect(url_for('static', filename='index.html'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
