from flask_restful import Resource, reqparse
from models import UserModel, RevokedTokenModel,EmployeeModel
from flask import request
import time
from flask import jsonify
from datetime import timedelta
from datetime import datetime
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                jwt_refresh_token_required,
                                get_jwt_identity,
                                get_raw_jwt)

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}
        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password']))
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was created'.format( data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 500

#expires = datetime.timedelta(days=365)
#token = create_access_token(username, expires_delta=expires)
#token = create_access_token(username)
#default expiration time for access_token= 15 minuts, and for refresh_token=365 days
#token = create_access_token(username, expires_delta=False) #no expiray
class UserLogin(Resource):
    def post(self):
        print(request.headers)
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}, 500

        if UserModel.verify_hash(data['password'], current_user.password):
            expires = timedelta(seconds=3600)
            access_token = create_access_token(identity=data['username'],expires_delta=expires)
            refresh_token = create_refresh_token(identity=data['username'])
            return {'message': 'Logged in as {}'.format(current_user.username),
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user_id':data['username']
                    }
        else:
            return {'message': 'Wrong credentials'}, 500


'''
tokens have an expiration date.
By default, access tokens have 15 minutes lifetime,
refresh tokens — 30 days.
'''

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        #print(request.headers)
        jti = get_raw_jwt()['jti']
        print('jti-->',jti)
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1N…NzIn0.HbpqySjT3FfGpr-gzK5_pSROeAssXVPGg8PD7OWLcnA
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        print(request.headers)
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    @jwt_required
    def get(self):
        print(request.headers)
        if(request.args.get('username')):
            current_user = UserModel.find_by_username(request.args.get('username'))
            return {'username':current_user.username,
                    'password':current_user.password}
        return UserModel.return_all()

    @jwt_required
    def delete(self):
        return UserModel.delete_all()

class AllUsersWithoutToken(Resource):
    def get(self):
        print(request.headers)
        if(request.args.get('username')):
            current_user = UserModel.find_by_username(request.args.get('username'))
            return {'username':current_user.username,
                    'password':current_user.password}
        return UserModel.return_all()

class EmployeeData(Resource):
    def post(self):
        data = request.get_json(force=True)
        print(data)
        if EmployeeModel.find_by_employeeid(data['employeeid']):
            return {'message': 'Employee with employeeid {} already exists'.format(data['employeeid'])}
        new_employee = EmployeeModel(
            employeeid = data['employeeid'],
            name=data['name'],
            designation=data['designation'],
            address=data['address'],
            gender=data['gender'],
            status=data['status'],
            dob=datetime(2012, 3, 3, 10, 10, 10)
        )

        try:
            new_employee.save_to_db()
            return {
                'message': 'Employee with employee id {} has been created'.format(data['employeeid']),
            }
        except:
            return {'message': 'Something went wrong'}, 500

    def get(self):
        if(request.args.get('employeeid')):
            return EmployeeModel.return_one(request.args.get('employeeid'))
        return EmployeeModel.return_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }

'''
Think of a scenario like this. You issue user of an access token of 3600 seconds and refresh token much longer as one day.

The user is a good user, he is at home and gets on/off your website shopping and searching on his iPhone. His IP address doesn't change and have a very low load on your server. Like 3-5 page requests every minute. When his 3600 seconds on the access token is over, he requires a new one with the refresh token. We, on the server side, check his activity history and IP address, think he is a human and behaves himself. We grant him a new access token to continue using our service. The user won't need to enter again the username/password until he has reached one day life-span of refresh token itself.

The user is a careless user. He lives in New York, USA and got his virus program shutdown and was hacked by a hacker in Poland. When the hacker got the access token and refresh token, he tries to impersonate the user and use our service. But after the short-live access token expires, when the hacker tries to refresh the access token, we, on the server, has noticed a dramatic IP change in user behavior history (hey, this guy logins in USA and now refresh access in Poland after just 3600s ???). We terminate the refresh process, invalidate the refresh token itself and prompt to enter username/password again.

The user is a malicious user. He is intended to abuse our service by calling 1000 times our API each minute using a robot. He can well doing so until 3600 seconds later, when he tries to refresh the access token, we noticed his behavior and think he might not be a human. We reject and terminate the refresh process and ask him to enter username/password again. This might potentially break his robot's automatic flow. At least makes him uncomfortable.

You can see the refresh token has acted perfectly when we try to balance our work, user experience and potential risk of a stolen token. Your watch dog on the server side can check more than IP change, frequency of api calls to determine whether the user shall be a good user or not.

Another word is you can also try to limit the damage control of stolen token/abuse of service by implementing on each api call the basic IP watch dog or any other measures. But this is expensive as you have to read and write record about the user and will slow down your server response.



'''

