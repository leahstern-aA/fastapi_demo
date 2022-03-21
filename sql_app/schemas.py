from re import L
from typing import List, Optional
from pydantic import BaseModel

"""
Pydantic schemas for DB models.
These schemas are used for data validation
with CRUD features.
"""

""" 
Contains information for Role class instances
shared between RoleCreate and Role classes
"""
class RoleBase(BaseModel):
    id: int
    name: str


"""
Contains extra information needed for 
creation of a Role class instance
"""
class RoleCreate(RoleBase):
    pass


"""
Contains extra information needed for
retrieving (reading) a Role class instance
"""
class Role(RoleBase):
    users: List['User'] = []

    # This class configures Pydantic models
    # orm_mode = True tells Pydantic to read data
    # with class.attribute syntax rather than dict syntax
    class Config:
        orm_mode = True


"""
Contains information for User class instances
shared between UserCreate and User classes
"""
class UserBase(BaseModel):
    id: int
    first_name: str
    last_name: str


"""
Contains extra information needed for creating
a User class instance
"""
class UserCreate(UserBase):
    middle_name: Optional[str]
    gender: Optional[str]


"""
Contains extra information needed for
retrieving (reading) a User class instance
"""
class User(UserBase):
    roles: List[Role] = []

    class Config:
        orm_mode = True