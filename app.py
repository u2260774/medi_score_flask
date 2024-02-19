from flask import Flask, render_template,request, redirect, url_for,flash
import pickle
from flask_wtf import FlaskForm
from wtforms import SelectField
from forms import InputForm
from medicare_function import calculate_medi_score


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Eight-Handled Sword Divergent Sila Divine General Mahoraga'

@app.route('/', methods=['GET', 'POST'])
def home():

    print_mediscore = False

    form = InputForm()

    if form.validate_on_submit():

        patient_id = form.patient_id.data
        resp_type = int(form.resp_type.data)
        conc = int(form.conc.data)
        resp_rate = form.resp_rate.data
        time_since = form.time_since.data
        spo2 = form.spo2.data
        temp = form.temp.data
        cbg = form.cbg.data

        medi_score = calculate_medi_score(resp_type, conc, resp_rate, spo2, temp, cbg, time_since)

        if medi_score[1] == True :
            flash('ALERT!!! The patient needs immediate attention , rapid change in Medi Score detected', 'error')


        print_mediscore = True

        return render_template('home.html', form=form,flag=print_mediscore,medi_score=medi_score)

    return render_template('home.html', form=form)

# if __name__ == '__main__':
#     app.run(debug=True)