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


class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False)
  email = Column(String, unique=True, index=True, nullable=False)
  password_hash = Column(String, nullable=False)
  role = Column(
      Enum(RoleEnum), default=RoleEnum.RESPONDENT, nullable=False
  )

  surveys = relationship(
      "Survey", back_populates="author", cascade="all, delete-orphan"
  )
  submissions = relationship(
      "Submission", back_populates="respondent", cascade="all, delete-orphan"
  )


class Survey(Base):
  __tablename__ = "surveys"
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, nullable=False)
  description = Column(Text, nullable=True)
  mode = Column(Enum(SurveyMode), default=SurveyMode.SURVEY, nullable=False)
  status = Column(
      Enum(SurveyStatus), default=SurveyStatus.DRAFT, nullable=False
  )
  start_date = Column(DateTime, nullable=True)
  end_date = Column(DateTime, nullable=True)
  author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  access_code = Column(String, nullable=True)

  author = relationship("User", back_populates="surveys")
  questions = relationship(
      "Question",
      back_populates="survey",
      cascade="all, delete-orphan",
      order_by="Question.position",
  )
  submissions = relationship(
      "Submission", back_populates="survey", cascade="all, delete-orphan"
  )


class Question(Base):
  __tablename__ = "questions"
  id = Column(Integer, primary_key=True, index=True)
  survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
  text = Column(Text, nullable=False)
  type = Column(Enum(QuestionType), nullable=False)
  required = Column(Boolean, default=True, nullable=False)
  points = Column(Integer, default=1, nullable=False)
  position = Column(Integer, default=0, nullable=False)

  survey = relationship("Survey", back_populates="questions")
  options = relationship(
      "Option", back_populates="question", cascade="all, delete-orphan"
  )
  answers = relationship(
      "Answer", back_populates="question", cascade="all, delete-orphan"
  )


class Option(Base):
  __tablename__ = "options"
  id = Column(Integer, primary_key=True, index=True)
  question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
  text = Column(String, nullable=False)
  correct = Column(Boolean, default=False, nullable=False)

  question = relationship("Question", back_populates="options")


class Submission(Base):
  __tablename__ = "submissions"
  id = Column(Integer, primary_key=True, index=True)
  survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
  respondent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  submitted_at = Column(DateTime, nullable=False)
  score = Column(Float, nullable=True)

  survey = relationship("Survey", back_populates="submissions")
  respondent = relationship("User", back_populates="submissions")
  answers = relationship(
      "Answer", back_populates="submission", cascade="all, delete-orphan"
  )


class Answer(Base):
  __tablename__ = "answers"
  id = Column(Integer, primary_key=True, index=True)
  submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
  question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
  text_value = Column(Text, nullable=True)

  submission = relationship("Submission", back_populates="answers")
  question = relationship("Question", back_populates="answers")
  selected_options = relationship("Option", secondary=answer_options)