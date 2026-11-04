import enum
from sqlalchemy import (
    Boolean,
    column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)

from sqlalchemy.orm import relationship
from database import Base

class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    RESPONDENT = "respondent"

class SurveyStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"
