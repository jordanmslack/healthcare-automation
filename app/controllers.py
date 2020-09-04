from uuid import uuid4

from decouple import config
from flask import render_template, Blueprint, redirect, url_for

from app.forms import *
from app.models import *


base = Blueprint('base', __name__, url_prefix='/', template_folder='templates')


@base.route('/', methods=['GET', 'POST'])
def home():

    return render_template('home.html')


@base.route('/find-doctor', methods=['GET', 'POST'])
def find_doctor():

    form = FindDoctor()
    insurance_plans = [(i.id, i.name) for i in InsurancePlan.query.all()]
    form.insurance_plan.choices = [(None, 'Select One')] + insurance_plans

    if form.validate_on_submit():
        return redirect(url_for('base.doctor_results', insurance_plan_id=form.insurance_plan.data))

    return render_template('find_doctor.html', form=form)


@base.route('/doctor-results/<insurance_plan_id>', methods=['GET', 'POST'])
def doctor_results(insurance_plan_id):

    doctor_ids = DoctorPlans.query.filter(DoctorPlans.insurance_plan_id == insurance_plan_id).all()
    doctors = Doctor.query.filter(Doctor.id.in_((i.doctor_id) for i in doctor_ids)).all()
    number = len(doctors)

    return render_template('doctor_results.html', doctors=doctors, number=number)


@base.route('/schedule-appointment/<doctor_id>/', methods=['GET', 'POST'])
def schedule_appointment(doctor_id=None):

    form = ScheduleAppointment()

    doctors = [(i.id, i.full_name) for i in Doctor.query.all()]
    form.doctor.choices = [(None, 'Select One'), ('no-doctor', 'I do not have a doctor')] + doctors

    if doctor_id is not None:
        form.doctor.data = doctor_id

    if form.validate_on_submit():

        appointment_id = str(uuid4())
        patient_id = str(uuid4())

        patient = Patient(
            id=patient_id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )

        appointment = Appointment(
            id=appointment_id,
            doctor_id=form.doctor.data,
            patient_id=patient_id,
            date=form.date_time.data
        )

        db.session.add(patient)
        db.session.add(appointment)
        db.session.commit()

        return redirect(url_for('base.confirmation', appointment_id=appointment_id))

    return render_template('schedule_appointment.html', form=form)


@base.route('/confirmation/<appointment_id>', methods=['GET', 'POST'])
def confirmation(appointment_id):

    appointment = Appointment.query.filter(Appointment.id == appointment_id).first()

    return render_template('appointment_confirmation.html', appointment=appointment)


@base.route('/seed-database/<secret_key>', methods=['GET', 'POST'])
def seed_database(secret_key):

    if secret_key == config('SECRET_KEY'):

        objects = [
            Doctor(id='3f479383-89a6-453d-a4c9-ef0fe31c2cc1', first_name='Jim', last_name='Halpert', title='M.D.'),
            Doctor(id='4541a10c-f612-484b-99d9-4a71402384d6', first_name='Kevin', last_name='Malone', title='M.D.'),
            Doctor(id='a8b13ef2-9845-446a-b3e0-12c800c329d7', first_name='Bob', last_name='Vance', title='D.O.'),
            Doctor(id='75329673-c317-42fa-92e6-c20dc83b4507', first_name='Phyllis', last_name='Vance', title='M.D.'),
            Doctor(id='0a477404-a585-4904-8642-a812a4bb656a', first_name='Creed', last_name='Bratton', title='M.D.'),
            Doctor(id='5b0ff3ff-a84f-4fcf-a6fb-9084c255ca1f', first_name='Andy', last_name='Bernard', title='D.O.'),
            Doctor(id='0affbf2c-f0c0-4006-8d73-0b32e1df88ee', first_name='Pam', last_name='Beesley-Halpert', title='M.B.B.S.'),
            Doctor(id='bdd8ac9a-114f-4812-bac7-82d425f9209a', first_name='Holly', last_name='Flax-Scott', title='M.D.'),
            Doctor(id='8b1f5048-2000-490c-8d00-6c2a47d9445b', first_name='Michael', last_name='Scott', title='M.D.'),
            Doctor(id='652a059d-e21a-477c-87c0-4d246f4711ce', first_name='Oscar', last_name='Martinez', title='M.D.'),
            Doctor(id='eb5c85ab-92d2-4fbb-aea6-c2239a6314d7', first_name='Toby', last_name='Flenderman', title='D.O.'),
            Doctor(id='3819a75b-993c-4fd1-ac8d-462d3f1517c3', first_name='Erin', last_name='Hannon', title='M.D.'),
            Doctor(id='956df4fe-d135-416c-aa23-6ada74ea47a4', first_name='Ryan', last_name='Howard', title='M.D.'),
            Doctor(id='89080cf0-f73b-4688-9bf2-53f6a7701a3f', first_name='Stanley', last_name='Hudson', title='M.B.B.S.'),
            Doctor(id='28a80f98-7522-4d99-ad21-9fd01c22c13f', first_name='Dwight', last_name='Schrute', title='M.D.'),
            Doctor(id='eb9775ae-ca7a-4af7-9215-ccefffa7cb5c', first_name='David', last_name='Wallace', title='M.D.'),
            Doctor(id='8f773ef4-3ec3-4be2-8a1e-482b82b80d37', first_name='Angela', last_name='Martin-Schrute', title='M.D.'),
            Doctor(id='38175e97-f460-49e1-8675-399aee7b87f1', first_name='Meredith', last_name='Palmer', title='D.O.'),
            Doctor(id='7c76e16d-28ad-4b6f-8e6b-4b373ada6096', first_name='Robert', last_name='California', title='M.D.'),
            Doctor(id='27306b59-c26e-48c9-bdc8-6d86da832a72', first_name='Jo', last_name='Bennett', title='M.B.B.S.'),
            Doctor(id='08e9cd4e-8581-4487-8c25-7408663cd3b4', first_name='Gabe', last_name='Lewis', title='M.D.'),
            Doctor(id='df0607ab-707c-44ce-b3f0-9d1b8f6a38b6', first_name='Karen', last_name='Filippelli', title='D.O.'),
            Doctor(id='4ac5429c-e6a8-4a29-b234-ee2376a725b3', first_name='Jan', last_name='Levinson-Gould', title='M.D.'),
            Doctor(id='28f667ad-b92a-4363-a568-699905e5eccc', first_name='Urkel', last_name='Grue', title='M.B.B.S.'),
            Doctor(id='2d0335ee-a23d-429d-ad4d-d74170a4bcc4', first_name='Darryl', last_name='Philbin', title='M.D.'),
            Doctor(id='b7f9dcda-96a1-4ca0-8f74-69b316f289ff', first_name='Kelly', last_name='Kapoor', title='D.O.'),
            InsuranceCompany(id='a8637ea9-c44b-4073-bac0-81d4f8973b6b', name='Aetna'),
            InsuranceCompany(id='6dfb295b-5ca9-4bd3-ac72-79eaeb1f7419', name='Blue Cross/Blue Shield'),
            InsuranceCompany(id='0c58d4ad-2f51-46f1-9c24-24d649cd938c', name='Cigna'),
            InsuranceCompany(id='4a2ceed4-d274-44d1-87a2-f878c1b2ead0', name='Humana'),
            InsuranceCompany(id='381f0ab3-1fb8-440f-81e6-6902dc60115a', name='HealthPartners'),
            InsuranceCompany(id='0a6f07e1-98c3-4dd8-b362-c718ce36f565', name='FloridaBlue'),
            InsuranceCompany(id='bcc39f7b-7ce0-4aa7-92e1-f8faba4f4ccb', name='UnitedHealth'),
            InsuranceCompany(id='7d4492ba-9903-4d0b-9c0b-d39ad4bb4f5b', name='WellCare'),
            InsuranceCompany(id='8ed93639-2644-4559-a086-09e3bb2da9bd', name='Caresource'),
            InsuranceCompany(id='9c791ef1-d499-434e-9213-edf5ad29ccf2', name='Metropolitan'),
            InsuranceCompany(id='0dd55d91-cd65-45cb-9263-98927e23338e', name='Kaiser Foundation'),
            InsuranceCompany(id='3fe1b051-da8f-40a6-917b-edf9b82d460b', name='Anthem Inc'),
            InsurancePlan(id='6bc112c0-27b6-40a3-8ec9-57921f0868d6', name='Aetna 573', type='HMO', insurance_company_id='a8637ea9-c44b-4073-bac0-81d4f8973b6b'),
            InsurancePlan(id='c2c4166d-95c5-4bcf-9e83-f1388420bfb7', name='Aetna 574', type='HMO', insurance_company_id='a8637ea9-c44b-4073-bac0-81d4f8973b6b'),
            InsurancePlan(id='6e2c4a69-2ba1-4e3e-8fbf-01c1a8b9e2f8', name='Aetna 681', type='HSA', insurance_company_id='a8637ea9-c44b-4073-bac0-81d4f8973b6b'),
            InsurancePlan(id='cfebeba3-47e5-4461-b2ed-9208189e30f0', name='Aetna 888', type='PPO', insurance_company_id='a8637ea9-c44b-4073-bac0-81d4f8973b6b'),
            InsurancePlan(id='5ba6d769-b09d-46e7-b9f2-c92de7a37b0f', name='Blue Cross/Blue Shield 121', type='HMO', insurance_company_id='6dfb295b-5ca9-4bd3-ac72-79eaeb1f7419'),
            InsurancePlan(id='93944eaa-b5e5-458a-a52f-c8c518c6d16f', name='Blue Cross/Blue Shield 122', type='HDHP', insurance_company_id='6dfb295b-5ca9-4bd3-ac72-79eaeb1f7419'),
            InsurancePlan(id='025ee9cc-332c-4ff2-8def-9c47847c3b73', name='Blue Cross/Blue Shield 301', type='HSA', insurance_company_id='6dfb295b-5ca9-4bd3-ac72-79eaeb1f7419'),
            InsurancePlan(id='f5722164-c1dc-4c07-b69d-c01f04960ddf', name='Cigna 754', type='PPO', insurance_company_id='0c58d4ad-2f51-46f1-9c24-24d649cd938c'),
            InsurancePlan(id='ffeb87b4-5781-4f4a-8cab-25612e2912de', name='Cigna 811', type='HSA', insurance_company_id='0c58d4ad-2f51-46f1-9c24-24d649cd938c'),
            InsurancePlan(id='59a06f0a-a0cf-45f2-8597-77e364939958', name='Humana 544', type='HSA', insurance_company_id='4a2ceed4-d274-44d1-87a2-f878c1b2ead0'),
            InsurancePlan(id='db272f54-f85d-4e43-bdbb-273cadb91e5d', name='Humana 311', type='HMO', insurance_company_id='4a2ceed4-d274-44d1-87a2-f878c1b2ead0'),
            InsurancePlan(id='3b6ea032-1e4a-4a87-810d-9c22861c75cd', name='Humana 221', type='PPO', insurance_company_id='4a2ceed4-d274-44d1-87a2-f878c1b2ead0'),
            InsurancePlan(id='75c07b45-fc56-4ef1-b740-764a0627fbe9', name='Humana 712', type='HDHP', insurance_company_id='4a2ceed4-d274-44d1-87a2-f878c1b2ead0'),
            InsurancePlan(id='447bed1f-2f8b-41c1-9dd0-fe8f223ca8ec', name='Humana 312', type='HMO', insurance_company_id='4a2ceed4-d274-44d1-87a2-f878c1b2ead0'),
            InsurancePlan(id='019b1671-8cc9-4119-a79d-fb8ca4dd093e', name='HealthPartners 732', type='HDHP', insurance_company_id='381f0ab3-1fb8-440f-81e6-6902dc60115a'),
            InsurancePlan(id='30f134a7-3947-43d1-b97e-ddceba9b4f66', name='HealthPartners 613', type='HMO', insurance_company_id='381f0ab3-1fb8-440f-81e6-6902dc60115a'),
            InsurancePlan(id='00ee827a-406f-4468-8162-4522badd046c', name='HealthPartners 432', type='HSA', insurance_company_id='381f0ab3-1fb8-440f-81e6-6902dc60115a'),
            InsurancePlan(id='ab5d5419-245f-4b72-b2ce-4a4f87a95552', name='FloridaBlue 377', type='HMO', insurance_company_id='0a6f07e1-98c3-4dd8-b362-c718ce36f565'),
            InsurancePlan(id='c9f07118-77a4-47c9-ab69-3f7620aba259', name='FloridaBlue 611', type='PPO', insurance_company_id='0a6f07e1-98c3-4dd8-b362-c718ce36f565'),
            InsurancePlan(id='9c96fcae-d13d-4c4d-99c6-0726339e9777', name='FloridaBlue 721', type='HSA', insurance_company_id='0a6f07e1-98c3-4dd8-b362-c718ce36f565'),
            InsurancePlan(id='2f1c0b09-93b5-425a-8c81-e8afd953ca3c', name='FloridaBlue 378', type='HMO', insurance_company_id='0a6f07e1-98c3-4dd8-b362-c718ce36f565'),
            InsurancePlan(id='ad8850f2-1166-42f2-bcc0-63d6e4207e91', name='UnitedHealth 532', type='HMO', insurance_company_id='bcc39f7b-7ce0-4aa7-92e1-f8faba4f4ccb'),
            InsurancePlan(id='057d1dbb-a1f2-4da7-9535-8f7b4d7e7ed6', name='UnitedHealth 321', type='HDHP', insurance_company_id='bcc39f7b-7ce0-4aa7-92e1-f8faba4f4ccb'),
            InsurancePlan(id='8b1b06f1-0170-49ee-897b-004b8ba63530', name='UnitedHealth 231', type='HSA', insurance_company_id='bcc39f7b-7ce0-4aa7-92e1-f8faba4f4ccb'),
            InsurancePlan(id='33b70291-06e3-4bf3-b0db-5de07b84e0f7', name='UnitedHealth 533', type='HMO', insurance_company_id='bcc39f7b-7ce0-4aa7-92e1-f8faba4f4ccb'),
            InsurancePlan(id='b3f7c920-d49e-40f2-ad1d-d2af0bfc0fb0', name='WellCare 812', type='HMO', insurance_company_id='7d4492ba-9903-4d0b-9c0b-d39ad4bb4f5b'),
            InsurancePlan(id='60ec2c9d-0486-4bbd-8652-b6d7ea493e90', name='WellCare 643', type='HDHP', insurance_company_id='7d4492ba-9903-4d0b-9c0b-d39ad4bb4f5b'),
            InsurancePlan(id='ef42d738-95e7-4408-807f-7f54652bebe2', name='WellCare 813', type='HMO', insurance_company_id='7d4492ba-9903-4d0b-9c0b-d39ad4bb4f5b'),
            InsurancePlan(id='d7cf4005-c0f7-40e8-82bf-9deaa10951d3', name='Caresource 712', type='HMO', insurance_company_id='8ed93639-2644-4559-a086-09e3bb2da9bd'),
            InsurancePlan(id='983c8277-ec43-43b7-b1b9-aa99ba7401c1', name='Caresource 544', type='PPO', insurance_company_id='8ed93639-2644-4559-a086-09e3bb2da9bd'),
            InsurancePlan(id='ca4c9258-d254-430b-86bc-e55f75356db4', name='Caresource 713', type='HMO', insurance_company_id='8ed93639-2644-4559-a086-09e3bb2da9bd'),
            InsurancePlan(id='0cf36f63-25dc-4bf7-b564-ad0dc440b4bb', name='Caresource 714', type='HMO', insurance_company_id='8ed93639-2644-4559-a086-09e3bb2da9bd'),
            InsurancePlan(id='418e0ba1-95aa-4ddd-9157-48b4201e7ad5', name='Metropolitan 441', type='PPO', insurance_company_id='9c791ef1-d499-434e-9213-edf5ad29ccf2'),
            InsurancePlan(id='8c64bb09-1cf9-4351-b5ff-1181b1863a1f', name='Metropolitan 387', type='HMO', insurance_company_id='9c791ef1-d499-434e-9213-edf5ad29ccf2'),
            InsurancePlan(id='553fb359-c010-40f3-9ee7-9867d8ea07e3', name='Metropolitan 714', type='HDHP', insurance_company_id='9c791ef1-d499-434e-9213-edf5ad29ccf2'),
            InsurancePlan(id='aa8e1e27-84a1-4c6e-ad4b-8cd2919f4db1', name='Metropolitan 388', type='HMO', insurance_company_id='9c791ef1-d499-434e-9213-edf5ad29ccf2'),
            InsurancePlan(id='6d0f9e4c-a984-4556-adbf-a31de43d5a41', name='Kaiser Foundation 121', type='PPO', insurance_company_id='0dd55d91-cd65-45cb-9263-98927e23338e'),
            InsurancePlan(id='214e5363-cc01-4e73-b8cb-32e87d8cd9c0', name='Kaiser Foundation 289', type='HMO', insurance_company_id='0dd55d91-cd65-45cb-9263-98927e23338e'),
            InsurancePlan(id='ab79e7e6-426f-4e44-a543-f2dc19cccdd5', name='Kaiser Foundation 491', type='HDHP', insurance_company_id='0dd55d91-cd65-45cb-9263-98927e23338e'),
            InsurancePlan(id='3ad11606-b378-468a-8946-d60f48b57ba7', name='Anthem Inc 412', type='HMO', insurance_company_id='3fe1b051-da8f-40a6-917b-edf9b82d460b'),
            InsurancePlan(id='088060b0-6473-4b3b-8f8a-5b0bb44c07de', name='Anthem Inc 413', type='HMO', insurance_company_id='3fe1b051-da8f-40a6-917b-edf9b82d460b'),
            InsurancePlan(id='14bf29d9-67ae-4099-8880-ca7970a205f1', name='Anthem Inc 414', type='HMO', insurance_company_id='3fe1b051-da8f-40a6-917b-edf9b82d460b'),
            InsurancePlan(id='cec00ee6-2a28-410c-94b8-e06d6e482b44', name='Anthem Inc 415', type='HMO', insurance_company_id='3fe1b051-da8f-40a6-917b-edf9b82d460b'),
            DoctorPlans(doctor_id='b7f9dcda-96a1-4ca0-8f74-69b316f289ff', insurance_plan_id='6bc112c0-27b6-40a3-8ec9-57921f0868d6'),
            DoctorPlans(doctor_id='b7f9dcda-96a1-4ca0-8f74-69b316f289ff', insurance_plan_id='c2c4166d-95c5-4bcf-9e83-f1388420bfb7'),
            DoctorPlans(doctor_id='b7f9dcda-96a1-4ca0-8f74-69b316f289ff', insurance_plan_id='cfebeba3-47e5-4461-b2ed-9208189e30f0'),
            DoctorPlans(doctor_id='2d0335ee-a23d-429d-ad4d-d74170a4bcc4', insurance_plan_id='6bc112c0-27b6-40a3-8ec9-57921f0868d6'),
            DoctorPlans(doctor_id='2d0335ee-a23d-429d-ad4d-d74170a4bcc4', insurance_plan_id='ab79e7e6-426f-4e44-a543-f2dc19cccdd5'),
            DoctorPlans(doctor_id='2d0335ee-a23d-429d-ad4d-d74170a4bcc4', insurance_plan_id='cfebeba3-47e5-4461-b2ed-9208189e30f0'),
            DoctorPlans(doctor_id='2d0335ee-a23d-429d-ad4d-d74170a4bcc4', insurance_plan_id='ffeb87b4-5781-4f4a-8cab-25612e2912de'),
            DoctorPlans(doctor_id='2d0335ee-a23d-429d-ad4d-d74170a4bcc4', insurance_plan_id='59a06f0a-a0cf-45f2-8597-77e364939958'),
            DoctorPlans(doctor_id='28f667ad-b92a-4363-a568-699905e5eccc', insurance_plan_id='6e2c4a69-2ba1-4e3e-8fbf-01c1a8b9e2f8'),
            DoctorPlans(doctor_id='28f667ad-b92a-4363-a568-699905e5eccc', insurance_plan_id='3b6ea032-1e4a-4a87-810d-9c22861c75cd'),
            DoctorPlans(doctor_id='28f667ad-b92a-4363-a568-699905e5eccc', insurance_plan_id='75c07b45-fc56-4ef1-b740-764a0627fbe9'),
            DoctorPlans(doctor_id='28f667ad-b92a-4363-a568-699905e5eccc', insurance_plan_id='019b1671-8cc9-4119-a79d-fb8ca4dd093e'),
            DoctorPlans(doctor_id='4ac5429c-e6a8-4a29-b234-ee2376a725b3', insurance_plan_id='30f134a7-3947-43d1-b97e-ddceba9b4f66'),
            DoctorPlans(doctor_id='4ac5429c-e6a8-4a29-b234-ee2376a725b3', insurance_plan_id='00ee827a-406f-4468-8162-4522badd046c'),
            DoctorPlans(doctor_id='4ac5429c-e6a8-4a29-b234-ee2376a725b3', insurance_plan_id='ab5d5419-245f-4b72-b2ce-4a4f87a95552'),
            DoctorPlans(doctor_id='df0607ab-707c-44ce-b3f0-9d1b8f6a38b6', insurance_plan_id='6e2c4a69-2ba1-4e3e-8fbf-01c1a8b9e2f8'),
            DoctorPlans(doctor_id='08e9cd4e-8581-4487-8c25-7408663cd3b4', insurance_plan_id='019b1671-8cc9-4119-a79d-fb8ca4dd093e'),
            DoctorPlans(doctor_id='08e9cd4e-8581-4487-8c25-7408663cd3b4', insurance_plan_id='c9f07118-77a4-47c9-ab69-3f7620aba259'),
            DoctorPlans(doctor_id='08e9cd4e-8581-4487-8c25-7408663cd3b4', insurance_plan_id='75c07b45-fc56-4ef1-b740-764a0627fbe9'),
            DoctorPlans(doctor_id='27306b59-c26e-48c9-bdc8-6d86da832a72', insurance_plan_id='6bc112c0-27b6-40a3-8ec9-57921f0868d6'),
            DoctorPlans(doctor_id='27306b59-c26e-48c9-bdc8-6d86da832a72', insurance_plan_id='c2c4166d-95c5-4bcf-9e83-f1388420bfb7'),
            DoctorPlans(doctor_id='27306b59-c26e-48c9-bdc8-6d86da832a72', insurance_plan_id='025ee9cc-332c-4ff2-8def-9c47847c3b73'),
            DoctorPlans(doctor_id='27306b59-c26e-48c9-bdc8-6d86da832a72', insurance_plan_id='db272f54-f85d-4e43-bdbb-273cadb91e5d'),
            DoctorPlans(doctor_id='27306b59-c26e-48c9-bdc8-6d86da832a72', insurance_plan_id='447bed1f-2f8b-41c1-9dd0-fe8f223ca8ec'),
            DoctorPlans(doctor_id='27306b59-c26e-48c9-bdc8-6d86da832a72', insurance_plan_id='30f134a7-3947-43d1-b97e-ddceba9b4f66'),
            DoctorPlans(doctor_id='7c76e16d-28ad-4b6f-8e6b-4b373ada6096', insurance_plan_id='9c96fcae-d13d-4c4d-99c6-0726339e9777'),
            DoctorPlans(doctor_id='38175e97-f460-49e1-8675-399aee7b87f1', insurance_plan_id='2f1c0b09-93b5-425a-8c81-e8afd953ca3c'),
            DoctorPlans(doctor_id='38175e97-f460-49e1-8675-399aee7b87f1', insurance_plan_id='ad8850f2-1166-42f2-bcc0-63d6e4207e91'),
            DoctorPlans(doctor_id='38175e97-f460-49e1-8675-399aee7b87f1', insurance_plan_id='8b1b06f1-0170-49ee-897b-004b8ba63530'),
            DoctorPlans(doctor_id='8f773ef4-3ec3-4be2-8a1e-482b82b80d37', insurance_plan_id='6bc112c0-27b6-40a3-8ec9-57921f0868d6'),
            DoctorPlans(doctor_id='8f773ef4-3ec3-4be2-8a1e-482b82b80d37', insurance_plan_id='025ee9cc-332c-4ff2-8def-9c47847c3b73'),
            DoctorPlans(doctor_id='8f773ef4-3ec3-4be2-8a1e-482b82b80d37', insurance_plan_id='f5722164-c1dc-4c07-b69d-c01f04960ddf'),
            DoctorPlans(doctor_id='8f773ef4-3ec3-4be2-8a1e-482b82b80d37', insurance_plan_id='db272f54-f85d-4e43-bdbb-273cadb91e5d'),
            DoctorPlans(doctor_id='eb9775ae-ca7a-4af7-9215-ccefffa7cb5c', insurance_plan_id='447bed1f-2f8b-41c1-9dd0-fe8f223ca8ec'),
            DoctorPlans(doctor_id='eb9775ae-ca7a-4af7-9215-ccefffa7cb5c', insurance_plan_id='c9f07118-77a4-47c9-ab69-3f7620aba259'),
            DoctorPlans(doctor_id='eb9775ae-ca7a-4af7-9215-ccefffa7cb5c', insurance_plan_id='9c96fcae-d13d-4c4d-99c6-0726339e9777'),
            DoctorPlans(doctor_id='eb9775ae-ca7a-4af7-9215-ccefffa7cb5c', insurance_plan_id='057d1dbb-a1f2-4da7-9535-8f7b4d7e7ed6'),
            DoctorPlans(doctor_id='eb9775ae-ca7a-4af7-9215-ccefffa7cb5c', insurance_plan_id='8b1b06f1-0170-49ee-897b-004b8ba63530'),
            DoctorPlans(doctor_id='28a80f98-7522-4d99-ad21-9fd01c22c13f', insurance_plan_id='6e2c4a69-2ba1-4e3e-8fbf-01c1a8b9e2f8'),
            DoctorPlans(doctor_id='28a80f98-7522-4d99-ad21-9fd01c22c13f', insurance_plan_id='93944eaa-b5e5-458a-a52f-c8c518c6d16f'),
            DoctorPlans(doctor_id='28a80f98-7522-4d99-ad21-9fd01c22c13f', insurance_plan_id='025ee9cc-332c-4ff2-8def-9c47847c3b73'),
            DoctorPlans(doctor_id='28a80f98-7522-4d99-ad21-9fd01c22c13f', insurance_plan_id='db272f54-f85d-4e43-bdbb-273cadb91e5d'),
            DoctorPlans(doctor_id='28a80f98-7522-4d99-ad21-9fd01c22c13f', insurance_plan_id='2f1c0b09-93b5-425a-8c81-e8afd953ca3c'),
            DoctorPlans(doctor_id='89080cf0-f73b-4688-9bf2-53f6a7701a3f', insurance_plan_id='93944eaa-b5e5-458a-a52f-c8c518c6d16f'),
            DoctorPlans(doctor_id='89080cf0-f73b-4688-9bf2-53f6a7701a3f', insurance_plan_id='447bed1f-2f8b-41c1-9dd0-fe8f223ca8ec'),
            DoctorPlans(doctor_id='89080cf0-f73b-4688-9bf2-53f6a7701a3f', insurance_plan_id='019b1671-8cc9-4119-a79d-fb8ca4dd093e'),
            DoctorPlans(doctor_id='89080cf0-f73b-4688-9bf2-53f6a7701a3f', insurance_plan_id='30f134a7-3947-43d1-b97e-ddceba9b4f66'),
            DoctorPlans(doctor_id='89080cf0-f73b-4688-9bf2-53f6a7701a3f', insurance_plan_id='ad8850f2-1166-42f2-bcc0-63d6e4207e91'),
            DoctorPlans(doctor_id='956df4fe-d135-416c-aa23-6ada74ea47a4', insurance_plan_id='33b70291-06e3-4bf3-b0db-5de07b84e0f7'),
            DoctorPlans(doctor_id='956df4fe-d135-416c-aa23-6ada74ea47a4', insurance_plan_id='ffeb87b4-5781-4f4a-8cab-25612e2912de'),
            DoctorPlans(doctor_id='3819a75b-993c-4fd1-ac8d-462d3f1517c3', insurance_plan_id='6bc112c0-27b6-40a3-8ec9-57921f0868d6'),
            DoctorPlans(doctor_id='3819a75b-993c-4fd1-ac8d-462d3f1517c3', insurance_plan_id='6e2c4a69-2ba1-4e3e-8fbf-01c1a8b9e2f8'),
            DoctorPlans(doctor_id='3819a75b-993c-4fd1-ac8d-462d3f1517c3', insurance_plan_id='447bed1f-2f8b-41c1-9dd0-fe8f223ca8ec'),
            DoctorPlans(doctor_id='eb5c85ab-92d2-4fbb-aea6-c2239a6314d7', insurance_plan_id='2f1c0b09-93b5-425a-8c81-e8afd953ca3c'),
            DoctorPlans(doctor_id='eb5c85ab-92d2-4fbb-aea6-c2239a6314d7', insurance_plan_id='057d1dbb-a1f2-4da7-9535-8f7b4d7e7ed6'),
            DoctorPlans(doctor_id='eb5c85ab-92d2-4fbb-aea6-c2239a6314d7', insurance_plan_id='33b70291-06e3-4bf3-b0db-5de07b84e0f7'),
            DoctorPlans(doctor_id='eb5c85ab-92d2-4fbb-aea6-c2239a6314d7', insurance_plan_id='00ee827a-406f-4468-8162-4522badd046c'),
            DoctorPlans(doctor_id='652a059d-e21a-477c-87c0-4d246f4711ce', insurance_plan_id='9c96fcae-d13d-4c4d-99c6-0726339e9777'),
            DoctorPlans(doctor_id='652a059d-e21a-477c-87c0-4d246f4711ce', insurance_plan_id='60ec2c9d-0486-4bbd-8652-b6d7ea493e90'),
            DoctorPlans(doctor_id='8b1f5048-2000-490c-8d00-6c2a47d9445b', insurance_plan_id='c2c4166d-95c5-4bcf-9e83-f1388420bfb7'),
            DoctorPlans(doctor_id='8b1f5048-2000-490c-8d00-6c2a47d9445b', insurance_plan_id='019b1671-8cc9-4119-a79d-fb8ca4dd093e'),
            DoctorPlans(doctor_id='8b1f5048-2000-490c-8d00-6c2a47d9445b', insurance_plan_id='00ee827a-406f-4468-8162-4522badd046c'),
            DoctorPlans(doctor_id='8b1f5048-2000-490c-8d00-6c2a47d9445b', insurance_plan_id='ab5d5419-245f-4b72-b2ce-4a4f87a95552'),
            DoctorPlans(doctor_id='8b1f5048-2000-490c-8d00-6c2a47d9445b', insurance_plan_id='8c64bb09-1cf9-4351-b5ff-1181b1863a1f'),
            DoctorPlans(doctor_id='bdd8ac9a-114f-4812-bac7-82d425f9209a', insurance_plan_id='b3f7c920-d49e-40f2-ad1d-d2af0bfc0fb0'),
            DoctorPlans(doctor_id='bdd8ac9a-114f-4812-bac7-82d425f9209a', insurance_plan_id='983c8277-ec43-43b7-b1b9-aa99ba7401c1'),
            DoctorPlans(doctor_id='0affbf2c-f0c0-4006-8d73-0b32e1df88ee', insurance_plan_id='c2c4166d-95c5-4bcf-9e83-f1388420bfb7'),
            DoctorPlans(doctor_id='0affbf2c-f0c0-4006-8d73-0b32e1df88ee', insurance_plan_id='ef42d738-95e7-4408-807f-7f54652bebe2'),
            DoctorPlans(doctor_id='0affbf2c-f0c0-4006-8d73-0b32e1df88ee', insurance_plan_id='aa8e1e27-84a1-4c6e-ad4b-8cd2919f4db1'),
            DoctorPlans(doctor_id='5b0ff3ff-a84f-4fcf-a6fb-9084c255ca1f', insurance_plan_id='f5722164-c1dc-4c07-b69d-c01f04960ddf'),
            DoctorPlans(doctor_id='5b0ff3ff-a84f-4fcf-a6fb-9084c255ca1f', insurance_plan_id='ffeb87b4-5781-4f4a-8cab-25612e2912de'),
            DoctorPlans(doctor_id='5b0ff3ff-a84f-4fcf-a6fb-9084c255ca1f', insurance_plan_id='c9f07118-77a4-47c9-ab69-3f7620aba259'),
            DoctorPlans(doctor_id='5b0ff3ff-a84f-4fcf-a6fb-9084c255ca1f', insurance_plan_id='553fb359-c010-40f3-9ee7-9867d8ea07e3'),
            DoctorPlans(doctor_id='5b0ff3ff-a84f-4fcf-a6fb-9084c255ca1f', insurance_plan_id='ef42d738-95e7-4408-807f-7f54652bebe2'),
            DoctorPlans(doctor_id='5b0ff3ff-a84f-4fcf-a6fb-9084c255ca1f', insurance_plan_id='ad8850f2-1166-42f2-bcc0-63d6e4207e91'),
            DoctorPlans(doctor_id='5b0ff3ff-a84f-4fcf-a6fb-9084c255ca1f', insurance_plan_id='3ad11606-b378-468a-8946-d60f48b57ba7'),
            DoctorPlans(doctor_id='5b0ff3ff-a84f-4fcf-a6fb-9084c255ca1f', insurance_plan_id='d7cf4005-c0f7-40e8-82bf-9deaa10951d3'),
            DoctorPlans(doctor_id='0a477404-a585-4904-8642-a812a4bb656a', insurance_plan_id='6e2c4a69-2ba1-4e3e-8fbf-01c1a8b9e2f8'),
            DoctorPlans(doctor_id='0a477404-a585-4904-8642-a812a4bb656a', insurance_plan_id='ca4c9258-d254-430b-86bc-e55f75356db4'),
            DoctorPlans(doctor_id='0a477404-a585-4904-8642-a812a4bb656a', insurance_plan_id='0cf36f63-25dc-4bf7-b564-ad0dc440b4bb'),
            DoctorPlans(doctor_id='0a477404-a585-4904-8642-a812a4bb656a', insurance_plan_id='418e0ba1-95aa-4ddd-9157-48b4201e7ad5'),
            DoctorPlans(doctor_id='0a477404-a585-4904-8642-a812a4bb656a', insurance_plan_id='214e5363-cc01-4e73-b8cb-32e87d8cd9c0'),
            DoctorPlans(doctor_id='0a477404-a585-4904-8642-a812a4bb656a', insurance_plan_id='cec00ee6-2a28-410c-94b8-e06d6e482b44'),
            DoctorPlans(doctor_id='0a477404-a585-4904-8642-a812a4bb656a', insurance_plan_id='8b1b06f1-0170-49ee-897b-004b8ba63530'),
            DoctorPlans(doctor_id='0a477404-a585-4904-8642-a812a4bb656a', insurance_plan_id='14bf29d9-67ae-4099-8880-ca7970a205f1'),
            DoctorPlans(doctor_id='0a477404-a585-4904-8642-a812a4bb656a', insurance_plan_id='d7cf4005-c0f7-40e8-82bf-9deaa10951d3'),
            DoctorPlans(doctor_id='75329673-c317-42fa-92e6-c20dc83b4507', insurance_plan_id='f5722164-c1dc-4c07-b69d-c01f04960ddf'),
            DoctorPlans(doctor_id='75329673-c317-42fa-92e6-c20dc83b4507', insurance_plan_id='c9f07118-77a4-47c9-ab69-3f7620aba259'),
            DoctorPlans(doctor_id='75329673-c317-42fa-92e6-c20dc83b4507', insurance_plan_id='9c96fcae-d13d-4c4d-99c6-0726339e9777'),
            DoctorPlans(doctor_id='75329673-c317-42fa-92e6-c20dc83b4507', insurance_plan_id='088060b0-6473-4b3b-8f8a-5b0bb44c07de'),
            DoctorPlans(doctor_id='a8b13ef2-9845-446a-b3e0-12c800c329d7', insurance_plan_id='6e2c4a69-2ba1-4e3e-8fbf-01c1a8b9e2f8'),
            DoctorPlans(doctor_id='a8b13ef2-9845-446a-b3e0-12c800c329d7', insurance_plan_id='60ec2c9d-0486-4bbd-8652-b6d7ea493e90'),
            DoctorPlans(doctor_id='4541a10c-f612-484b-99d9-4a71402384d6', insurance_plan_id='8c64bb09-1cf9-4351-b5ff-1181b1863a1f'),
            DoctorPlans(doctor_id='4541a10c-f612-484b-99d9-4a71402384d6', insurance_plan_id='6d0f9e4c-a984-4556-adbf-a31de43d5a41'),
            DoctorPlans(doctor_id='4541a10c-f612-484b-99d9-4a71402384d6', insurance_plan_id='5ba6d769-b09d-46e7-b9f2-c92de7a37b0f'),
            DoctorPlans(doctor_id='3f479383-89a6-453d-a4c9-ef0fe31c2cc1', insurance_plan_id='418e0ba1-95aa-4ddd-9157-48b4201e7ad5'),
            DoctorPlans(doctor_id='3f479383-89a6-453d-a4c9-ef0fe31c2cc1', insurance_plan_id='0cf36f63-25dc-4bf7-b564-ad0dc440b4bb'),
            DoctorPlans(doctor_id='3f479383-89a6-453d-a4c9-ef0fe31c2cc1', insurance_plan_id='983c8277-ec43-43b7-b1b9-aa99ba7401c1'),
            DoctorPlans(doctor_id='3f479383-89a6-453d-a4c9-ef0fe31c2cc1', insurance_plan_id='3b6ea032-1e4a-4a87-810d-9c22861c75cd'),
            DoctorPlans(doctor_id='3f479383-89a6-453d-a4c9-ef0fe31c2cc1', insurance_plan_id='5ba6d769-b09d-46e7-b9f2-c92de7a37b0f'),
        ]
        db.session.bulk_save_objects(objects)
        db.session.commit()

        return redirect(url_for('base.home'))

    else:
        return redirect(url_for('base.home'))
