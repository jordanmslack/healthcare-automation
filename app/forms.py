from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField, TextAreaField


class FindDoctor(FlaskForm):

    insurance_plan = SelectField(
        'What health insurance plan do you have?',
        choices=()
    )


class ScheduleAppointment(FlaskForm):

    first_name = StringField(
        'First Name',
        render_kw={"placeholder": "First Name"}
    )

    last_name = StringField(
        'Last Name',
        render_kw={"placeholder": "Last Name"}
    )

    doctor = SelectField(
        'Which doctor would you like to see?',
        choices=()
    )

    date_time = DateField(
        'When would you like to schedule your appointment?',
        format='%Y-%m-%d', render_kw={"placeholder": "Appointment Date and Time", "type": "date"}
    )

    email = StringField(
        'Email Address',
        render_kw={'placeholder': 'What email can we use to keep in touch?'},
    )

    reminder = IntegerField(
        'How many days prior to your appointment would you like to be notified?',
    )
