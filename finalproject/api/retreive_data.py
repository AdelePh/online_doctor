import numpy 
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pickle
import sqlite3
def get_all_medians_from_training_transcript(data,patient):
    ALL_data = data.execute("SELECT BMI,Height,Weight,SystolicBP,DiastolicBP,RespiratoryRate,HeartRate,Temperature FROM training_transcript WHERE PatientGuid= '%s'" % patient[0]).fetchall()
    features_list = []
    for x in range(0,8):
        THIS_values = []
        for each_THIS_value in ALL_data:
            if (each_THIS_value[x] != 0.0 and each_THIS_value[x] != 'NULL'):
                THIS_values.append(float(each_THIS_value[x]))
        if (len(THIS_values) > 0):
            features_list.append(numpy.median(numpy.array([THIS_values])))
        else:
            features_list.append(0)
    return features_list

def get_gender(data,patient):
    gender = data.execute("SELECT Gender FROM training_patient WHERE PatientGuid= '%s'" % patient[0]).fetchone() 
    if (gender[0] == 'M'):
        return 0
    elif (gender[0] == 'F'):
        return 1
    else:
        print ("ERROR")
        return 0

def get_YearOfBirth(data,patient):
    YearOfBirth = data.execute("SELECT YearOfBirth FROM training_patient WHERE PatientGuid= '%s'" % patient[0]).fetchone()[0]
    return (YearOfBirth)

def get_HL7Text(data,patient):
    lab_tests_list = data.execute("SELECT DISTINCT HL7Text FROM training_labs").fetchall()
        #Only consider lab_tests appear > 10 times 
    for test in lab_tests_list:
        amount = data.execute("""SELECT COUNT(HL7Text) FROM training_labs WHERE HL7Text = "%s" """ % test).fetchall()
        if (amount[0][0]<10):
            lab_tests_list.remove(test)
    code = [0]*239
    tests_done = data.execute("SELECT HL7Text FROM training_labs WHERE PatientGuid= '%s'" % patient[0]).fetchall()
    for test in tests_done:
        if (test in lab_tests_list):
            location = lab_tests_list.index(test)
            code[location] +=1
    return code

def get_DiagnosisDescription(data,patient):
    all_DiagnosisDescription_list = data.execute("SELECT DISTINCT DiagnosisDescription FROM training_diagnosis").fetchall()
    x=0
    for each_diagnosis in all_DiagnosisDescription_list:
        x+=1
        amount = data.execute("""SELECT COUNT(DiagnosisDescription) FROM training_diagnosis WHERE DiagnosisDescription = "%s" """ % each_diagnosis).fetchall()
        if (amount[0][0]<10):
            all_DiagnosisDescription_list.remove(each_diagnosis)
    code = [0]*2336
    all_DiagnosisDescription_received = data.execute("SELECT DiagnosisDescription FROM training_diagnosis WHERE PatientGuid= '%s'" % patient[0]).fetchall()
    for each_diagnosis in all_DiagnosisDescription_received:
        if (each_diagnosis in all_DiagnosisDescription_list):
            location = all_DiagnosisDescription_list.index(each_diagnosis)
            code[location] +=1
    return code

def get_MedicationName(data,patient):
    all_MedicationName_list = data.execute("SELECT DISTINCT MedicationName FROM training_allMeds").fetchall()
    x=0
    for each_medication in all_MedicationName_list:
        x+=1
        amount = data.execute("""SELECT COUNT(MedicationName) FROM training_medication WHERE MedicationName = "%s" """ % each_medication).fetchall()
        if (amount[0][0]<10):
            all_MedicationName_list.remove(each_medication)
    code = [0]*1522
    all_MedicationName_received = data.execute("SELECT MedicationName FROM training_medication WHERE PatientGuid= '%s'" % patient[0]).fetchall()
    for each_medication in all_MedicationName_received:
        if (each_medication in all_MedicationName_list):
            location = all_MedicationName_list.index(each_medication)
            code[location] +=1
    return code
