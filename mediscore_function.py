from datetime import datetime
import json
from enum import Enum
import os
import traceback

# Create respiration and consciousness enums
class respiration(Enum):
    AIR = 0
    OXYGEN = 2


class consciousness(Enum):
    ALERT = 0
    CVPU = 3


# return respiration and consciousness values
def get_resp_type(resp):
    if resp == respiration.AIR.value or resp == respiration.OXYGEN.value:
        return resp
    else:
        raise Exception("Incorrect respiratory type. Must be AIR(0) or OXYGEN(2)")


def get_consciousness(consc):
    if consc == consciousness.ALERT.value or consc == consciousness.CVPU.value:
        return consc
    else:
        raise Exception("Incorrect consciousness type. Must be ALERT(0) or CVPU(3)")


# return respiration rate mediscore
def get_resp_rate(resp_rate):
    try:
        # make sure input was an integer
        resp_rate = int(resp_rate)
        if resp_rate < 0:
            raise Exception("Respiration rate must be in range 0-100.")
        if resp_rate <= 8 or resp_rate >= 25:
            return 3
        elif resp_rate <= 11:
            return 1
        elif resp_rate <= 20:
            return 0
        elif resp_rate <= 24:
            return 2
    except Exception:
        raise Exception("Respiration rate must be whole digits only.")


# return spo2 mediscore
def get_spo2(spo2, resp_type):
    try:
        # make sure input was an integer
        spo2 = int(spo2)
        if spo2 <= 0:
            raise Exception("SpO2 must be in range 0-100.")
        if spo2 <= 83:
            return 3
        elif spo2 <= 85:
            return 2
        elif spo2 <= 87:
            return 1
        elif resp_type == respiration.AIR.value or spo2 <= 92:
            return 0
        elif spo2 <= 94:
            return 1
        elif spo2 <= 96:
            return 2
        elif resp_type >= 97:
            return 3
    except Exception:
        raise Exception("SpO2 accepts whole digits only.")


# return temperature mediscore
def get_temp(temp):
    try:
        # make sure input was a float, round to one decimal point
        temp = round(float(temp), 1)
        # check if temperature is in Celsius (based on the most extreme survival scenarios)
        if temp > 48.0 or temp < 12.0:
            raise Exception("Temperature must be in celsius.")
        if temp <= 35.0:
            return 3
        elif temp >= 39.1:
            return 2
        elif temp <= 36.0 or temp >= 38.1:
            return 1
        elif temp <= 38.0:
            return 0
    except Exception:
        raise Exception("Temperature must be in digits.")


# return cbg mediscore
def get_cbg(cbg, timeSinceMeal):
    try:
        if cbg < 0:
            raise Exception("CBG can not be negative.")
        # make sure input was a float, round to one decimal point
        cbg = round(float(cbg), 1)
        print(cbg)
        if timeSinceMeal <= 2:
            if cbg <= 4.4 or cbg >= 9.0:
                return 3
            elif cbg <= 5.8 or cbg >= 7.9:
                return 2
            elif cbg <= 7.8:
                return 0
        else:
            if cbg <= 3.4 or cbg >= 6.0:
                return 3
            elif cbg <= 3.9 or cbg >= 5.5:
                return 2
            elif cbg <= 5.4:
                return 0
    except Exception:
        raise Exception("CBG must be in positive digits.")


def calculate_medi_score(respirationType, consc, respRate, spo2, temperature, cbg, timeSinceMeal):
    try:
        # check current time for flag
        curr_time = datetime.now()
        # assign mediscores
        resp_type = get_resp_type(respirationType)
        consc_type = get_consciousness(consc)
        resp_rate_score = get_resp_rate(respRate)
        spo2_score = get_spo2(spo2, resp_type)
        temp_score = get_temp(temperature)
        cbg_score = get_cbg(cbg, timeSinceMeal)
        # set default flag value
        flag = False
        medi_score = resp_type + consc_type + resp_rate_score + spo2_score + temp_score + cbg_score
        # check if history file exists
        if os.path.isfile('history.json'):
            with open('history.json') as history:
                history_data = json.load(history)
                # get time and mediscore from last entry
                time = datetime.strptime(history_data["history"][-1]["time"], '%Y-%m-%d %H:%M:%S.%f')
                prev_score = history_data["history"][-1]["info"][0]["medi_score"]
                delta = curr_time - time
                # check if less than 24 hours and greater than 2 difference
                if delta.seconds / 86400 < 1 and medi_score - prev_score > 2:
                    flag = True
        # construct object to insert new data
        patient_info = {
            "time": str(datetime.now()),
            "info": [
                {
                    "resp_type": resp_type,
                    "consc_type": consc_type,
                    "resp_rate_score": resp_rate_score,
                    "spo2_score": spo2_score,
                    "temp_score": temp_score,
                    "cbg_score": cbg_score,
                    "medi_score": medi_score,
                    "flag": flag
                }
            ]
        }
        # check if file exists, create one if it doesn't
        if os.path.isfile('history.json') is False:
            with open('history.json', 'w') as history:
                history.write('{"history":[]}')
        # write new data
        with open("history.json", 'r+') as history:
            history_data = json.load(history)
            history_data["history"].append(patient_info)
            history.seek(0)
            json.dump(history_data, history, indent=4)
        # return mediscore and flag
        return medi_score, flag
    except Exception as e:
        return(traceback.format_exc())


print(calculate_medi_score(respiration.OXYGEN.value, consciousness.ALERT.value, 15, 95, 37.1, 6.4, 0))
