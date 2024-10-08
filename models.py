from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, Boolean
from sqlalchemy.orm import relationship

# Define database table schema
Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    name = Column(String)
    description = Column(String)
    status = Column(String)
    gsf_standards_version = Column(String)
    estimated_annual_credits = Column(Float)
    crediting_period_start_date = Column(DateTime)
    crediting_period_end_date = Column(DateTime)
    methodology = Column(String)
    type = Column(String)
    size = Column(String)
    sustaincert_id = Column(Integer)
    sustaincert_url = Column(String)
    project_developer = Column(String)
    carbon_stream = Column(String)
    country = Column(String)
    country_code = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    sustainable_development_goals = relationship("SustainableDevelopmentGoal", back_populates="project",
                                                 cascade="all, delete-orphan")
    labels = Column(JSON)
    summary = relationship("Summary", back_populates="project", cascade="all, delete-orphan")
    issuance_list = relationship("IssuanceList", back_populates="project", cascade="all, delete-orphan")
    retirements = relationship("Retirement", back_populates="project", cascade="all, delete-orphan")


class SustainableDevelopmentGoal(Base):
    __tablename__ = "sustainable_development_goals"

    id = Column(Integer, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"))
    name = Column(String)
    issuable_products = Column(JSON)

    project = relationship("Project", back_populates="sustainable_development_goals")


class Summary(Base):
    __tablename__ = "summary"

    id = Column(Integer, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"))
    product = Column(String)
    status = Column(String)
    total = Column(Integer)

    project = relationship("Project", back_populates="summary")


class IssuanceList(Base):
    __tablename__ = "issuance_list"

    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    number_of_credits = Column(Integer)
    starting_credit_number = Column(Integer)
    ending_credit_number = Column(Integer)
    batch_number = Column(Integer)
    serial_number = Column(String)
    certified_date = Column(DateTime)
    monitoring_period_start_date = Column(DateTime)
    monitoring_period_end_date = Column(DateTime)
    status = Column(String)
    vintage = Column(String)
    is_active = Column(Boolean)
    product_name = Column(String)
    product_abbreviation = Column(String)
    labels = Column(JSON)

    project = relationship("Project", back_populates="issuance_list")


class Retirement(Base):
    __tablename__ = "retirements"

    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    number_of_credits = Column(Integer)
    starting_credit_number = Column(Integer)
    ending_credit_number = Column(Integer)
    batch_number = Column(Integer)
    serial_number = Column(String)
    certified_date = Column(DateTime)
    monitoring_period_start_date = Column(DateTime)
    monitoring_period_end_date = Column(DateTime)
    status = Column(String)
    vintage = Column(String)
    is_active = Column(Boolean)
    note = Column(String)
    product_name = Column(String)
    product_abbreviation = Column(String)
    labels = Column(JSON)

    project = relationship("Project", back_populates="retirements")
