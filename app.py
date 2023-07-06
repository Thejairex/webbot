from flask import Flask, render_template
from iqoption import Iq
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql=MySQL(app)
iq = Iq()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'market'
app.secret_key = "OtakuTeca"

def fecth_data():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM ordens"
    cur.execute(query)
    return cur.fetchall()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/ordenes")
def ordenes():
    return render_template('ordenes.html', datas = fecth_data())


if __name__ == "__main__":
    app.run(debug=True)