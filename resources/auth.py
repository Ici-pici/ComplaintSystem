from flask import request
from flask_restful import Resource
from managers.complainer import ComplainerManager
from utils.decorators import validate_schema
from schemas.request.auth import RegisterComplainerSchema, LoginSchemaRequest
class RegisterComplainerResource(Resource):
    @validate_schema(RegisterComplainerSchema)
    def post(self):
        data = request.get_json()
        token = ComplainerManager.register(data)
        return {'token': token}, 201


class LoginResource(Resource):
    @validate_schema(LoginSchemaRequest)
    def post(self):
        data = request.get_json()
        token = ComplainerManager.login(data)
        return {'token': token}, 200
