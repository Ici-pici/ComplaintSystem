from flask_restful import Resource

from managers.auth import auth
from managers.user import ApproverManager
from models.enums import RoleEnum
from utils.decorators import role_required


class ApproveApproverResource(Resource):
    @auth.login_required
    @role_required(RoleEnum.admin)
    def put(self, id):
        ApproverManager.approve(id)
        return 204



class RejectApproverResource(Resource):
    @auth.login_required
    @role_required(RoleEnum.admin)
    def put(self, id):
        ApproverManager.reject(id)
        return 204

class RemoveApproverResource(Resource):
    @auth.login_required
    @role_required(RoleEnum.admin)
    def put(self, id):
        ApproverManager.remove(id)
        return 204
