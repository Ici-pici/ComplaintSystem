from flask import request
from flask_restful import Resource
from managers.complainer import ComplainerManager
from utils.decorators import validate_schema
from schemas.request.auth import RegisterSchemaRequest
class RegisterResource(Resource):
    @validate_schema(RegisterSchemaRequest)
    def post(self):
        data = request.get_json()
        token = ComplainerManager.register(data)
        return {'token': token}, 201
