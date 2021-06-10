from flask import Flask , render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/libro/<int:cod>/')
def select_libro(cod=1):
    return render_template('libro.html', title=cod)

@app.route('/saludo/noche')
def noche():
    return "Buenas Noches!!! Que descanses!!!"

if __name__ == "__main__":
    app.run(debug=True)