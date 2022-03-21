from sqlalchemy.orm import Session
from .models import User, Role

# Commented out, there was an issue earlier with overlapping names from models
# from .schemas import Role, RoleBase, RoleCreate, User, UserBase, UserCreate

def seed(db: Session):
    admin_role = Role(name="admin")
    student_role = Role(name="student")
    user_role = Role(name="user")

    db.add(admin_role)
    db.add(student_role)
    db.add(user_role)

    user1 = User(
        first_name="Jamila", 
        last_name="Ahmed",
        gender="woman",
        roles=[student_role, user_role]
    )

    user2 = User(
        first_name="Alex",
        last_name="Smith",
        gender="nonbinary",
        roles=[admin_role]
    )

    db.add(user1)
    db.add(user2)
    
    db.commit()