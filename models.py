from run import db
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import datetime
class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }

        return {'data': list(map(lambda x: to_json(x), UserModel.query.all())),
                'message':'list of all users'}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}


    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

# on log out, store token in database and blacked list the logout token
class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


class EmployeeModel(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    employeeid = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    status = db.Column(db.String(10), nullable=False) #active and not active
    dob = db.Column(db.DateTime)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_employeeid(cls, employeeid):
        return cls.query.filter_by(employeeid=employeeid).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'employeeid': x.employeeid,
                'name': x.name,
                'designation': x.designation,
                'address': x.address,
                'gender': x.gender,
                'status': x.status,
                'dob': str(x.dob)
            }

        return {'data': list(map(lambda x: to_json(x), EmployeeModel.query.all())),
                'message': 'list of all employees'}

    @classmethod
    def return_one(cls,employeeid):
        employee = cls.query.filter_by(employeeid=employeeid).first()
        data = {'employeeid':employee.employeeid,
                'name':employee.name,
                'designation':employee.designation,
                'address':employee.address,
                'gender':employee.gender,
                'status':employee.status,
                'dob':str(employee.dob)
                }
        return data

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @classmethod
    def delete_by_id(cls,eid):
        try:
            employee = cls.query.filter_by(employeeid=eid).first()
            db.session.delete(employee)
            db.session.commit()
            return {'message': 'employee with employeeid {} deleted'.format(eid)}
        except:
            return {'message': 'Something went wrong'}

