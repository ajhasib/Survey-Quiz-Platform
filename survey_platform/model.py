import enum

import Column
from sqlalchemy import (
    Boolean,
    Column,
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


class SurveyMode(str, enum.Enum):
    SURVEY = "survey"
    QUIZ = "quiz"


class QuestionType(str, enum.Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    FREE_TEXT = "free_text"
    SCALE_1_5 = "scale_1_5"

answer_options = Table(
        "answer_options",
        Base.metadata,
        Column(
            "answer_id", Integer, ForeignKey("answers.id"), primary_key=True
        ),
        Column(
            "option_id", Integer, ForeignKey("options.id"), primary_key=True
        ),
    )
