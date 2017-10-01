
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import datetime
#e = create_engine('sqlite:///attendance.db')

e = create_engine('mysql+mysqldb://username:password@localhost:3306/attendance',echo=False, pool_recycle=3600)

#conn = e.connect()
#query = conn.execute("create table TEST")
#conn.execute("use attendance;")
app = Flask(__name__)
api = Api(app)

class Students(Resource):
	def get(self):
		conn = e.connect()
		query = conn.execute("select distinct Name from STUDENT")
		return {'Names': [i[0] for i in query.cursor.fetchall()]}

class Students_Names(Resource):
    def get(self, student_name):
        conn = e.connect()
        query = conn.execute("select * from STUDENT where Name='%s'"%student_name)
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class MarkAttendance(Resource):
    def get(self, student_fingerprint,cid):
        conn = e.connect()
        query = conn.execute("select SID, Name from STUDENT where FINGERPRINT='%s'"%student_fingerprint)
        #result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        s1=str(query.fetchall())
        query = conn.execute("select CID, Name from COURSE where CID='%s'" % cid)
        s2=str(query.fetchall())
        replace="[(')]"
        for char in replace:
            s1=s1.replace(char,"")
            s2=s2.replace(char,"")
        return jsonify(Student=s1,Course=s2)

class DateTime(Resource):
    def get(self):
        conn = e.connect()
        time=str(datetime.datetime.now())
        time=time.split('.')
        return time[0]
class TeacherDetails(Resource):
    def get(self,teacher_fingerprint):
        conn=e.connect()
        query=conn.execute("SELECT CID FROM TEACHER WHERE FINDERPRINT='%s'"%teacher_fingerprint)
        s=str(query.fetchall())
        replace="[(',)]"
        for char in replace:
            s=s.replace(char,"")
        print(s)
        conn.close()
        return jsonify(CID=s)

            


api.add_resource(Students_Names, '/names/<string:student_name>')
api.add_resource(Students, '/names')
api.add_resource(MarkAttendance, '/mark/<string:student_fingerprint>,<string:cid>')
api.add_resource(DateTime, '/time')
api.add_resource(TeacherDetails,'/teacherprint/<string:teacher_fingerprint>')


if __name__ == '__main__':
    app.run(
        #host = "127.0.0.1",
        # port=3058,
        debug=True)
