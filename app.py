from flask import *
from werkzeug.utils import secure_filename
import os
from utilities import Utils, Security
from db import Db

os.chdir(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)
db = Db()

def upload(folder, archivo):
    if archivo:
        filename = secure_filename(archivo.filename)
        
        if Security().verify_extensions_sqls(filename):
            url = f"{folder}/{filename}"
            print(url)
            archivo.save(os.path.join("static/" + url))
            return url
        
        else:
            return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/ordenes")
def ordenes():
    datas = db.select_all("ordenes")
    return render_template("ordenes.html", datas=datas)

@app.route("/resultados")
def resultados():
    datas = db.select_all("ExecutEdos")
    return render_template("resultados.html", datas = datas)

@app.route("/ordenes/merge")
def ordenes_merge():
    return render_template("add_item_shop.html")

@app.route("/api/merge_ordenes", methods=["POST"])
def add_item_shop():
    file = request.files['sql']
    url = upload("sqls", file)
    if url:
        orden, executed = Utils().filterSqlFile(url, db.select_last_data("Ordenes"),db.select_last_data("Executedos"))
        
        if orden:
            for query in orden:
                db.merge_table(query)
        
        if executed:
            for query in executed:
                db.merge_table(query)
        
        return redirect(url_for("ordenes"))
    else:
            pass
    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(debug=True)