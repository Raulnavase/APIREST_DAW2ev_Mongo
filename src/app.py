from flask import Flask, render_template, url_for, redirect, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')
app.config['MONGO_URI'] = getenv('MONGO_URI')

mongo = PyMongo(app)

camisetas  = mongo.db.camisetas

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        marca = request.form['marca']
        talla = request.form['talla']
        color  = request.form['color']
        material = request.form['material']

        if not marca or not talla or not color or not material:
            return redirect(url_for('index'))
        
        camisetas.insert_one({
            "marca": marca,
            "talla": talla,
            "color": color,
            "material": material
        })

        return redirect(url_for('index'))
    
    data = camisetas.find()
    return render_template('index.html', camisetas=data)
        

@app.route('/delete/<string:id>')
def delete(id):
    camisetas.delete_one({ "_id": ObjectId(id) })
    
    return redirect(url_for("index"))


@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        marca = request.form['marca']
        talla = request.form['talla']
        color = request.form['color']
        material = request.form['material']


        camisetas.update_one({ "_id": ObjectId(id) },
                            { "marca": marca,
                            "talla": talla,
                            "color": color,
                            "material": material })
    
    data = camisetas.find()

    return render_template('edit.html', camiseta=data)


@app.route('/camisetas_json')
def camisetas_json():
    return jsonify(list(camisetas.find()))


if __name__ == '__main__':
    app.run(debug=True)

