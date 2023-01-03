from flask import request
from flask_restful import Resource
from managers.complainer import ComplainerManager

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        token = ComplainerManager.register(data)
        return {'token': token}, 201
