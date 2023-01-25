from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.user import ComplainerManager, ApproverManager
from models.enums import RoleEnum
from schemas.request.auth import RegisterComplainerSchema, LoginSchemaRequest, RegisterApproverRequest
from schemas.response.auth import ApproverResponseSchema
from utils.decorators import validate_schema, role_required


class RegisterComplainerResource(Resource):
    @validate_schema(RegisterComplainerSchema)
    def post(self):
        data = request.get_json()
        token = ComplainerManager.register(data)
        return {'token': token}, 201


class RegisterApproverResource(Resource):
    @auth.login_required
    @role_required(RoleEnum.complainer)
    @validate_schema(RegisterApproverRequest)
    def post(self):
        data = request.get_json()
        user = auth.current_user()
        approver_request = ApproverManager.create(data, user)
        return ApproverResponseSchema().dump(approver_request), 201


class LoginResource(Resource):
    @validate_schema(LoginSchemaRequest)
    def post(self):
        data = request.get_json()
        token = ComplainerManager.login(data)
        return {'token': token}, 200
