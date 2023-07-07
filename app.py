from flask import Flask, render_template
from iqoption import Iq
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)
iq = Iq()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'market'
app.secret_key = "OtakuTeca"


def fetch_ordens():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM ordens ORDER BY id_orden DESC"
    cur.execute(query)
    datas = cur.fetchall()
    return datas

def fecth_result():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM executeds ORDER BY id_executed DESC"
    cur.execute(query)
    datas = cur.fetchall()
    return datas

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/ordenes")
def ordenes():
    return render_template('ordenes.html', datas = fetch_ordens())

@app.route("/resultados")
def resultados():
    return render_template('resultados.html', datas= fecth_result())


if __name__ == "__main__":
    app.run(debug=True)
