from flask_restful import Resource
from flask import request
from managers.auth import auth
from utils.decorators import role_required, validate_schema
from models.enums import RoleEnum
from managers.complaint import ComplaintManager
from schemas.response.complaint import ComplaintSchemaResponse
from schemas.request.complaint import ComplaintSchemaRequest

class ComplaintResource(Resource):
    @auth.login_required
    @role_required(RoleEnum.complainer)
    @validate_schema(ComplaintSchemaRequest)
    def post(self):
        data = request.get_json()
        user = auth.current_user()
        complaint = ComplaintManager.create(data, user)
        return ComplaintSchemaResponse().dump(complaint), 201


class ApproveComplaintResource(Resource):
    @auth.login_required
    @role_required(RoleEnum.approver)
    def put(self, id):
        ComplaintManager.approve(id)
        return 204

class RejectComplaintResource(Resource):
    @auth.login_required
    @role_required(RoleEnum.approver)
    def put(self, id):
        ComplaintManager.reject(id)
        return 204
