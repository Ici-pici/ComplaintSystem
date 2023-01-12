from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.complaint import ComplaintManager
from models.enums import RoleEnum
from schemas.request.complaint import ComplaintSchemaRequest
from schemas.response.complaint import ComplaintSchemaResponse
from utils.decorators import role_required, validate_schema


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
