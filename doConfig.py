# -*- coding: UTF-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app=Flask(__name__,template_folder="static")
bootstrap = Bootstrap(app)

@app.route('/login/',methods=('GET','POST'))
@app.route('/',methods=('GET','POST'))
def index():

    return render_template('index.html')

def run_flask():
    app.run(debug=True,threaded=True)

if __name__ == '__main__':
    run_flask()





