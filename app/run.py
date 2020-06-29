import couchdb
from flask import Flask, render_template
app = Flask(__name__)

couchdb_server = couchdb.Server('http://openCampus:openCampus@127.0.0.1:5984')
db = couchdb_server['course-report']

@app.route('/')
@app.route('/index')
def index():
    # Listado de todos los documentos almacenados
    documents = [row.doc for row in db.view("_all_docs", include_docs=True)]
    
    # Obtener valores unicos 
    documents_unique = list({document['courseID']:document for document in documents}.values())
    posts = []
    for document in documents_unique:
        posts.append({'courseID': document['courseID'],'courseName':document['courseName'],
            'totalReports': len([row for row in db.find({'selector':{'courseID':document['courseID']}})])})
    
    return render_template('index.html', posts=posts, coursesTotal = len(posts))

if __name__ == '__main__':
    # app.run(host='0.0.0.0') # en una direccion en especifico
    app.run() # en el localhost (127.0.0.1)