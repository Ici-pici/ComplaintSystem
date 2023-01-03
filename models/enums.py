from enum import Enum

class RoleEnum(Enum):
    complainer = 'Complainer'
    approver = 'Approver'
    admin = 'Admin'


class StatusEnum(Enum):
    pending = 'Pending'
    approved = 'Approved'
    rejected = 'Rejected'
