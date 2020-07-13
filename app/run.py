import couchdb
from flask import Flask, render_template, request
app = Flask(__name__)

couchdb_server = couchdb.Server('http://openCampus:openCampus@127.0.0.1:5984')
db = couchdb_server['course-report']

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    
    # Listado de todos los documentos almacenados
    documents = [row.doc for row in db.view("reports/all_reports", include_docs = True)]
    # Obtener valores unicos 
    documents_unique = list({document['courseID']:document for document in documents}.values())
    posts = []

    for document in documents_unique:
        posts.append({'courseID': document['courseID'],'courseName':document['courseName'],
            'totalReports': len([row for row in db.view("reports/number_reports",key=document['courseID'])])})
    
    # Ordenar primero por nombre del curso
    posts = sorted(posts, key=lambda post : post['courseName'])
    
    return render_template('index.html', posts = posts, coursesTotal = len(posts))

@app.route('/report', methods=['GET','POST'])
def report():
    
    # Obtener el listado de valores que retorna la vista 'details'
    posts = [eval(post) for post in [str(row.value).replace('[','').replace(']','') for row in \
        db.view("reports/details", key=request.form['courseID'])]]

    
    # Ordenar primero por hora y luego fecha
    posts = sorted(sorted(posts, key=lambda post : post['reportTime'], reverse = True), \
        key=lambda post : post['reportDate'], reverse = True)

    
    return render_template('report.html', reports = posts, courseName = posts[0]['courseName'], 
        courseID = posts[0]['courseID'])

@app.route('/view_details/<report_id>', methods=['GET'])
def view_details(report_id):
    
    # obtener el contenido de un reporte
    # report_detail = db.get(report_id)
    '''
    report_detail = [eval(str(row.value).replace('[','').replace(']','')) \
        for row in db.view("reports/status", key=report_id)]
    '''
    report_detail = [row for row in db.view("reports/status", key=report_id)]
    # print(report_detail)

    return render_template('view_details.html', report = report_detail)

if __name__ == '__main__':
    # app.run(host='0.0.0.0') # en una direccion en especifico
    app.run(debug=True) # en el localhost (127.0.0.1)