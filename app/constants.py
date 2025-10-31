from enum import Enum as PyEnum

class RoleEnum(str, PyEnum):
    admin = "admin"
    teacher = "teacher"
    student = "student"