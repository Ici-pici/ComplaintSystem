from flask_restful import Resource
from flask import request
from managers.auth import auth
from utils.decorators import role_required
from models.enums import RoleEnum
from managers.complaint import ComplaintManager
from schemas.response.complaint import ComplaintSchemaResponse

class ComplaintResource(Resource):
    @auth.login_required
    @role_required(RoleEnum.complainer)
    def post(self):
        data = request.get_json()
        user = auth.current_user()
        complaint = ComplaintManager.create(data, user)
        return ComplaintSchemaResponse().dump(complaint), 201
