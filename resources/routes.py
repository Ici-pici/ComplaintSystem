from resources.auth import RegisterComplainerResource, LoginResource, RegisterApproverResource
from resources.complaint import ComplaintResource, ApproveComplaintResource, RejectComplaintResource

routes = (
    (RegisterComplainerResource, '/complainer_register'),
    (RegisterApproverResource, '/approver_register'),
    (LoginResource, '/login'),
    (ComplaintResource, '/make_complaint'),
    (ApproveComplaintResource, '/complaint/<int:id>/approve'),
    (RejectComplaintResource, '/complaint/<int:id>/reject'),
)
