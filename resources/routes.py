from resources.auth import RegisterComplainerResource, LoginResource
from resources.complaint import ComplaintResource, ApproveComplaintResource, RejectComplaintResource

routes = (
    (RegisterComplainerResource, '/complainer_register'),
    (LoginResource, '/login'),
    (ComplaintResource, '/make_complaint'),
    (ApproveComplaintResource, '/complaint/<int:id>/approve'),
    (RejectComplaintResource, '/complaint/<int:id>/reject'),
)
