# VISUALIZACIÓN DE REPORTES DE CURSOS EDX
## Preparar el entorno de trabajo
> ### PYTHON
* Pendiente agregar archivo ```requirements.txt```

> ### APACHE COUCHDB
- Definir vistas (A través de la interfaz propia de couchDB)

    Vista: ```all_reports```
    - Crear una nueva vista y nombre del documento ( _/design ) colocar ```reports```
    - En la opción ```index name``` colocar ```all_reports```
	- En la opción ```Map function``` colocar:
	
			function (doc) {
  				emit(doc._id, [doc.courseID,doc.courseName]);
			}
			
			
	Vista: ```number_reports```
    - En la opción ```Design Document```  escoger ```_design/reports```
    - En la opción ```index name``` colocar ```number_reports```
	- En la opción ```Map function``` colocar:
	
			function (doc) {
  				emit(doc.courseID, doc);
			}
			
	
	Vista: ```details```
    - En la opción ```Design Document```  escoger ```_design/reports```
    - En la opción ```index name``` colocar ```details```
	- En la opción ```Map function``` colocar:
	
			function (doc) {
 				emit(doc.courseID, [{'_id':doc._id, 'courseName': doc.courseName, 'courseID': doc.courseID, 'reportDate': doc.reportDate, 'reportTime':doc.reportTime}]);
			}
		
## Ejecución
* Clone el repositoio (```Edx-Course-Report```) en el mismo directorio donde se encuentra el curso descomprimido de edX.   
		 
		 https://github.com/CarlosCastillo10/app-flask-openCampus.git
* Ubiquese en el repositorio clonado.
		
		cd app-flask-openCampus/
* Ubiquese en la aplicación

		cd app/
* Ejecute la aplicación.
		
		python run.py

## Uso
* La aplicación se estará ejecutando en: ```http://127.0.0.1:5000/```
