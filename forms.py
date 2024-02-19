from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, FloatField, SubmitField
from wtforms.validators import InputRequired

class InputForm(FlaskForm):
    resp_type = SelectField('What is the respiration type?', choices=[('', 'Please select'), ('2', 'Oxygen'), ('0', 'Air')], validators=[InputRequired()])
    conc = SelectField('Is the patient concious?', choices=[('', 'Please select'), ('0', 'Aware'), ('3', 'Unconcious')], validators=[InputRequired()])
    resp_rate = IntegerField('Respirate Rate', validators=[InputRequired()])
    time_since = IntegerField('How many hours since last meal', validators=[InputRequired()])
    spo2 = IntegerField('Oxygen Saturation (0-100)', validators=[InputRequired()])
    temp = FloatField("Patient's Body Temperature", validators=[InputRequired()])
    cbg = FloatField("Patient's Blood Glucose", validators=[InputRequired()])

    submit = SubmitField("Submit")
