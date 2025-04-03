import os
from os import getenv
from flask import Flask, render_template

app = Flask(__name__)
app.config["SECRET_KEY"]=os.getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
