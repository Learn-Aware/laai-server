from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from typing import Any, List, Optional, Union

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class StudentModel(BaseModel):
    """
    Container for a single student record.
    """

    # The primary key for the StudentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    full_name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    nickname: str = Field(...)
    role: str = Field(default="student")
    preferred_language: str = "English"
    grade: int = Field(...)
    school_district: str = Field(...)
    school_name: str = Field(...)
    last_math_subject_marks: int = Field(...)
    study_session_duration: int = Field(...)
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "nafufull_namell_nameme": "Jane Doe",
                "email": "jdoe@example.com",
                "nickname": "JaneFonda",
                "password": "password123",
                "role": "student",
                "preferred_language": "English",
                "grade": 12,
                "school_district": "Toronto",
                "school_name": "Central High School",
                "last_math_subject_marks": 90,
                "study_session_duration": 60,                
            }
        },
    )
    

class UpdateStudentModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    full_name: Optional[str] = Field(...)
    email: Optional[EmailStr] = Field(...)
    nickname: Optional[str] = Field(...)
    preferred_language: Optional[str] = Field(...)
    grade: Optional[int] = Field(...)
    school_district: Optional[str] = Field(...)
    school_name: Optional[str] = Field(...)
    last_math_subject_marks: Optional[int] = Field(...)
    study_session_duration: Optional[int] = Field(...)
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "full_name": "Jane Doe",
                "email": "jdoe@example.com",
                "nickname": "JaneFonda",
                "preferred_language": "English",
                "grade": 12,
                "school_district": "Toronto",
                "school_name": "Central High School",
                "last_math_subject_marks": 90,
                "study_session_duration": 60,
            }
        },
    )

class StudentCollection(BaseModel):
    """
    A container holding a list of `StudentModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    students: List[StudentModel]

class ParentModel(BaseModel):
    """
    Container for a single parent record.
    """

    # The primary key for the ParentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    full_name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    student_email: List[str] = Field(..., description="List of student emails")
    role: str = Field(default="parent")
    preferred_language: str = "English"
    relationship: str = Field(...)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "full_name": "Jane Doe",
                "email": "jdoe@example.com",
                "password": "password123",
                "role": "parent",
                "preferred_language": "English",
                "relationship": "mother",
            }
        }
    )

class ParentCollection(BaseModel):
    """
    A container holding a list of `ParentModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """
    parents: List[ParentModel]

class UserResponse(BaseModel):
    message: str
    data: Union[StudentModel, ParentModel]

    model_config = ConfigDict(
        json_encoders={ObjectId: str},
    )

class UserLoginModel(BaseModel):
    email: str = Field(max_length=60)
    password: str = Field(min_length=6)
    
