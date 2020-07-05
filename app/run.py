import couchdb
from flask import Flask, render_template, request
app = Flask(__name__)

couchdb_server = couchdb.Server('http://openCampus:openCampus@127.0.0.1:5984')
db = couchdb_server['course-report']

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    
    # Listado de todos los documentos almacenados
    documents = [row.doc for row in db.view("_all_docs", include_docs=True)]
    
    # Obtener valores unicos 
    documents_unique = list({document['courseID']:document for document in documents}.values())
    posts = []

    for document in documents_unique:
        posts.append({'courseID': document['courseID'],'courseName':document['courseName'],
            'totalReports': len([row for row in db.find({'selector':{'courseID':document['courseID']}})])})
    posts = sorted(posts, key=lambda post : post['courseName'])
    '''
    # Para realizar procedimiento de busqueda
    if request.method == 'POST':
        for document in documents_unique:
            if request.form['courseName'].lower() == document['courseName'].lower():
                posts = document 
    '''
    return render_template('index.html', posts = posts, coursesTotal = len(posts))

@app.route('/report', methods=['GET','POST'])
def report():
    
    posts = [row for row in db.find({'selector':{'courseID':request.form['courseID']}})]
    posts = sorted(sorted(posts, key=lambda post : post['reportTime'], reverse = True), \
        key=lambda post : post['reportDate'], reverse = True)
    # posts = sorted(posts, key=lambda post : post['reportTime'], reverse = True)
    
    return render_template('report.html', reports = posts, courseName = posts[0]['courseName'], 
        courseID = posts[0]['courseID'])

@app.route('/view_details/<report_id>', methods=['GET'])
def view_details(report_id):
    
    report_detail = db.get(report_id)
    
    return render_template('view_details.html', report = report_detail)

if __name__ == '__main__':
    # app.run(host='0.0.0.0') # en una direccion en especifico
    app.run(debug=True) # en el localhost (127.0.0.1)