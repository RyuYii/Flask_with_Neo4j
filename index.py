from flask import Flask , render_template, jsonify
from neo4j import GraphDatabase

bdgrafo=GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j","123"))
app = Flask(__name__)


@app.route('/')
def index():
    conectado = bdgrafo.session()
    q1='''MATCH (p1:Person)-[:READ]->(b1:Book)<-[:READ]-(p2:Person)-[:READ]->(b2:Book)
    WHERE not ((p1)-[:READ]->(b2))
    RETURN p1 as Persona1, p2 as Persona2, b2 as LibroRecomendado'''
    nodos=conectado.run(q1).data()

    lista = []
    for n in nodos:
        lista.append(n['LibroRecomendado']['title'])

    listaL = []
    for element in lista:
        if element not in listaL:
            listaL.append(element)
    
    conectado = bdgrafo.session()    
    q1 = '''MATCH (p1:Person)-[:READ]->(b1:Book)<-[:READ]-(p2:Person)-[:READ]->(b2:Book)
WITH p1, p2, count(b1) as NLibros, collect(b1) as LibrosCompartidos, b2
WHERE not ((p1)-[:READ]->(b2)) and NLibros >=2
RETURN p1.name as Persona1, p2.name as Persona2,
LibrosCompartidos as LibrosCompartidos, 
b2 as LibroRecomendado'''
    nodos=conectado.run(q1).data()
    lista = []
    for n in nodos:
        for t in n['LibrosCompartidos']:
            lista.append(t['title'])
            #lista.append(t)
            #print(type(t))
    
    listaA = []
    for element in lista:
        if element not in listaA:
            listaA.append(element)
    return render_template('index.html', lista=listaL, lista2=listaA)

@app.route('/libro/<string:cod>/')
def select_libro(cod='1'):
    return render_template('libro.html', title=cod)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': 'The requested URL was not found on the server.'}), 404

if __name__ == "__main__":
    app.run(debug=True)