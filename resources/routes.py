from resources.auth import RegisterResource, LoginResource
from resources.complaint import ComplaintResource, ApproveComplaintResource, RejectComplaintResource

routes = (
    (RegisterResource, '/register'),
    (LoginResource, '/login'),
    (ComplaintResource, '/make_complaint'),
    (ApproveComplaintResource, '/complaint/<int:id>/approve'),
    (RejectComplaintResource, '/complaint/<int:id>/reject'),
)