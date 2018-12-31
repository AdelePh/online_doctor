import numpy as np
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
import pickle
import sqlite3

from retreive_data import get_all_medians_from_training_transcript,get_gender,get_YearOfBirth,get_HL7Text,get_DiagnosisDescription,get_MedicationName
my_svm = pickle.load(open("svm.pkl","rb"))
app = Flask(__name__)
api= Api(app)


class HealthCheck(Resource):
    def get(self,user_id):
        database_loc = 'compData.db'
        data = sqlite3.connect(database_loc)
        patient_id = (user_id,)
        new_features_list = get_all_medians_from_training_transcript(data,patient_id) 
        new_features_list.append(get_gender(data,patient_id)) 
        new_features_list.append(get_YearOfBirth(data,patient_id)) 
        new_features_list = new_features_list + get_HL7Text(data,patient_id) 
        new_features_list = new_features_list + get_DiagnosisDescription(data,patient_id) 
        new_features_list = new_features_list + get_MedicationName(data,patient_id)
        X_array =[]
        X_array.append(new_features_list) 
        y = my_svm.predict([X_array[0]])
        output=y[0].tolist()
        return {user_id : output}
    
api.add_resource(HealthCheck, '/<string:user_id>')

if __name__ == '__main__':
    app.run(debug = True)
    
