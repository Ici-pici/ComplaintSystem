from resources.auth import RegisterResource, LoginResource
from resources.complaint import ComplaintResource

routes = (
    (RegisterResource, '/register'),
    (LoginResource, '/login'),
    (ComplaintResource, '/make_complaint')
)