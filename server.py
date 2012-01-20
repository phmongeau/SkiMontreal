import os
from flask import Flask, url_for, redirect
from bin import ski_parse

app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_map():
    return redirect(url_for('static', filename='index.html'))

@app.route("/conditions.json", methods=['GET'])
def get_conditions():
    return ski_parse.get_conditions()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
