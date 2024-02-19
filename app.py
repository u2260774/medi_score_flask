from flask import Flask, render_template,request, redirect, url_for,flash
import pickle
from flask_wtf import FlaskForm
from wtforms import SelectField
from forms import InputForm
from mediscore_function import calculate_medi_score


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Eight-Handled Sword Divergent Sila Divine General Mahoraga'

@app.route('/', methods=['GET', 'POST'])
def home():

    print_mediscore = False

    form = InputForm()

    if form.validate_on_submit():
        resp_type = int(form.resp_type.data)
        conc = int(form.conc.data)
        resp_rate = form.resp_rate.data
        time_since = form.time_since.data
        spo2 = form.spo2.data
        temp = form.temp.data
        cbg = form.cbg.data

        medi_score = calculate_medi_score(resp_type, conc, resp_rate, spo2, temp, cbg, time_since)
        if isinstance(medi_score[0],int):
            alert = medi_score[1]
            medi_score = "The patient's Medi score is "+str(medi_score[0])+"."
        print_mediscore = True

        return render_template('home.html', form=form,flag=print_mediscore,medi_score=medi_score,alert=alert)

    return render_template('home.html', form=form)

# if __name__ == '__main__':
#     app.run(debug=True)
