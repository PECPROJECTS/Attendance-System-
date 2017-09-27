
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import datetime

#e = create_engine('sqlite:///attendance.db')
e = create_engine('mysql+mysqldb://username:password@localhost:3306/mydb',echo=False, pool_recycle=3600)

app = Flask(__name__)
api = Api(app)

class Students(Resource):
	def get(self):
		conn = e.connect()
		query = conn.execute("select distinct Name from attendance")
		return {'Names': [i[0] for i in query.cursor.fetchall()]}

class Students_Names(Resource):
    def get(self, student_name):
        conn = e.connect()
        query = conn.execute("select * from attendance where Name='%s'"%student_name)
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class MarkAttendance(Resource):
    def get(self, student_names):
        conn = e.connect()
        students = student_names.split(',')
        query = conn.execute("select * from attendance where Name='%s'"%student_name)
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return students

class DateTime(Resource):
    def get(self):
        conn = e.connect()
        time=str(datetime.datetime.now())
        time=time.split('.')
        query = conn.execute("select * from attendance where Name='%s'"%student_name)
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return time[0]

api.add_resource(Students_Names, '/names/<string:student_name>')
api.add_resource(Students, '/names')
api.add_resource(MarkAttendance, '/mark/<string:student_names>')
api.add_resource(DateTime, '/time')

if __name__ == '__main__':
    app.run(
        #host = "127.0.0.1",
        # port=3058,
        debug=True)
