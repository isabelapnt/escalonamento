from flask import Flask, request, render_template
from jinja2 import Template

app = Flask(__name__)

@app.route("/")
def root():
    return render_template('grafico.html')
    
if __name__ == "__main__":
    app.run()