import pandas as pd
import joblib

def run_model(input):
    assert input is not None
    model = joblib.load('model/dva_project.model')
    return model.predict(pd.DataFrame.from_dict([input]))