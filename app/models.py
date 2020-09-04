from sqlalchemy.orm import relationship
from sqlalchemy import func, Column, String, Date, DateTime, ForeignKey, Integer

from app import db


class DoctorPlans(db.Model):
    __tablename__ = 'doctor_plans'

    doctor_id = Column(String, ForeignKey('doctor.id'), primary_key=True)
    insurance_plan_id = Column(String, ForeignKey('insurance_plan.id'), primary_key=True)


class Doctor(db.Model):

    __tablename__ = 'doctor'

    id = Column(String, unique=True, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    title = Column(String)
    created = Column(DateTime(timezone=True), server_default=func.now())
    last_modified = Column(DateTime(timezone=True), onupdate=func.now())

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}, {self.title}"


class Appointment(db.Model):

    __tablename__ = 'appointment'

    id = Column(String, unique=True, primary_key=True)
    date = Column(Date)
    reminder = Column(Integer)
    patient_id = Column(String, ForeignKey('patient.id'))
    patient = relationship('Patient', backref='appointment')

    doctor_id = Column(String, ForeignKey('doctor.id'))
    doctor = relationship('Doctor', backref='appointment')

    created = Column(DateTime(timezone=True), server_default=func.now())
    last_modified = Column(DateTime(timezone=True), onupdate=func.now())


class Patient(db.Model):

    __tablename__ = 'patient'

    id = Column(String, unique=True, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)

    created = Column(DateTime(timezone=True), server_default=func.now())
    last_modified = Column(DateTime(timezone=True), onupdate=func.now())

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def next_appointment(self):
        return ''

    def days_til_appointment(self):
        return


class InsuranceCompany(db.Model):

    __tablename__ = 'insurance_company'

    id = Column(String, unique=True, primary_key=True)
    name = Column(String)
    created = Column(DateTime(timezone=True), server_default=func.now())
    last_modified = Column(DateTime(timezone=True), onupdate=func.now())


class InsurancePlan(db.Model):

    __tablename__ = 'insurance_plan'

    id = Column(String, unique=True, primary_key=True)
    name = Column(String)
    type = Column(String)
    insurance_company_id = Column(String, ForeignKey('insurance_company.id'))
    insurance_company = relationship('InsuranceCompany', backref='insurance_plan')
    created = Column(DateTime(timezone=True), server_default=func.now())
    last_modified = Column(DateTime(timezone=True), onupdate=func.now())
