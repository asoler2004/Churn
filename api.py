from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import json
import pandas as pd
import numpy as np
from typing import Optional
from sklearn.preprocessing import MinMaxScaler
import shap

# Load the trained models and metadata
try:
    XGBmodel = joblib.load('XGBoost_model.pkl')
    
    RFmodel = joblib.load('RandomForest_model.pkl')
    
    with open('XGBoost_model_metadata.json', 'r') as f:
        XGBmetadata = json.load(f)
    
    with open('RandomForest_model_metadata.json', 'r') as f:
        RFmetadata = json.load(f)

    feature_columns = XGBmetadata['feature_columns']
    scaler =  joblib.load('XGBoost_model_scaler.pkl')
    XGB_explainer = joblib.load('XGBoost_model_explainer.pkl')
    RF_explainer = joblib.load('RandomForest_model_explainer.pkl')

except FileNotFoundError:
    raise Exception("Model files not found. Please run train_model.py first.")

app = FastAPI(title="Churn Prediction API", version="1.0.0")



class CustomerData(BaseModel):
    age: int
    credit_score: float
    withdrawal: int
    deposits: int
    purchases_partners: int
    cc_recommended: int
    web_user: int
    ios_user: int
    registered_phones: int
    waiting_4_loan: int
    cancelled_loan: int
    received_loan: int
    rejected_loan: int
    left_for_two_month_plus: int
    left_for_one_month: int
    reward_rate: float
    is_referred: int

class PredictionResponse(BaseModel):
    churn_probability_XGB: float
    churn_prediction_XGB: int
    risk_level_XGB: str
    shap_values_XGB: str
    base_values_XGB: float

    churn_probability_RF: float
    churn_prediction_RF: int
    risk_level_RF: str
    shap_values_RF: str
    base_values_RF: float

    customerdata: str
    processeddata: str



def preprocess_input(customer_data: CustomerData):
    """Preprocess input data to match training format"""
    # Convert to dictionary
    data_dict = customer_data.dict()
    
    # Create DataFrame
    df = pd.DataFrame([data_dict])
    
    if scaler is not None:
        selected_cols= ["purchases_partners",
                    "reward_rate",
                    "cc_recommended",
                    "web_user",
                    "received_loan",
                    "credit_score",
                    "age",
                    "deposits",
                    "withdrawal",
                    "registered_phones" ]

        # df[selected_cols] = scaler.fit_transform(df[selected_cols])

    # if use_onehot:
    #     # Use OneHotEncoder
    #     for col in categorical_columns:
    #         if col in df.columns and col in encoders:
    #             encoder = encoders[col]
    #             try:
    #                 # Transform the categorical column
    #                 encoded_data = encoder.transform(df[[col]].astype(str))
                    
    #                 # Create column names for one-hot encoded features
    #                 feature_names = [f"{col}_{category}" for category in encoder.categories_[0][1:]]  # Skip first due to drop='first'
    #                 encoded_df = pd.DataFrame(encoded_data, columns=feature_names, index=df.index)
                    
    #                 # Drop original column and add encoded columns
    #                 df = df.drop(col, axis=1)
    #                 df = pd.concat([df, encoded_df], axis=1)
                    
    #             except Exception:
    #                 # Handle unseen categories - encoder will handle this with handle_unknown='ignore'
    #                 # Create zero columns for this categorical variable
    #                 feature_names = [f"{col}_{category}" for category in encoder.categories_[0][1:]]
    #                 zero_df = pd.DataFrame(0, columns=feature_names, index=df.index)
    #                 df = df.drop(col, axis=1)
    #                 df = pd.concat([df, zero_df], axis=1)
    # else:
    #     # Use LabelEncoder
    #     for col in categorical_columns:
    #         if col in df.columns and col in encoder_metadata:
    #             classes = encoder_metadata[col]['classes']
    #             value = str(df[col].iloc[0])
                
    #             if value in classes:
    #                 df[col] = classes.index(value)
    #             else:
    #                 # Handle unseen categories by assigning to most frequent class (index 0)
    #                 df[col] = 0
    
    # Ensure all feature columns are present and in correct order

    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0
    
    # Reorder columns to match training data
    df = df[feature_columns]
    
    return df

@app.get("/")
async def root():
    return {"message": "Churn Prediction API", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=PredictionResponse)
async def predict_churn(customer_data: CustomerData):
    """Predict churn probability for a customer"""
    try:
        # Preprocess the input data
        processed_data = preprocess_input(customer_data)
        
        # Make prediction
        churn_probability_XGB = XGBmodel.predict_proba(processed_data)[0][1]
        churn_prediction_XGB = int(churn_probability_XGB > 0.5)
        churn_probability_RF = RFmodel.predict_proba(processed_data)[0][1]
        churn_prediction_RF = int(churn_probability_RF > 0.5)

       
        # Determine risk level
        if churn_probability_XGB < 0.3:
            risk_level_XGB = "Low"
        elif churn_probability_XGB < 0.7:
            risk_level_XGB = "Medium"
        else:
            risk_level_XGB = "High"
        
        if churn_probability_RF < 0.3:
            risk_level_RF = "Low"
        elif churn_probability_RF < 0.7:
            risk_level_RF = "Medium"
        else:
            risk_level_RF = "High"
        
        # Determine shap values
        shap_values_RF = RF_explainer.shap_values(processed_data)[:,:,1].tolist()
        shap_values_XGB = XGB_explainer.shap_values(processed_data)[[0]].tolist()

        base_values_RF = RF_explainer.expected_value[1]
        base_values_XGB = XGB_explainer.expected_value

        """
        shap.waterfall_plot(shap.Explanation(
                        values = explainerRF.shap_values(unseen_data)[:,:,1],
                        base_values = explainerRF.expected_value[1],
                        data = unseen_data,
                        feature_names=X_test.columns.tolist())[0],
                    max_display=17,
                    show=True
                    )

        shap.waterfall_plot(shap.Explanation(
                        values = explainerXGB.shap_values(unseen_data)[[0]],
                        base_values = explainerXGB.expected_value,
                        data = unseen_data,
                        feature_names=X_test.columns.tolist())[0],
                    max_display=17,
                    show=True
                    )"""
        return PredictionResponse(
            churn_probability_XGB =float(churn_probability_XGB),
            churn_prediction_XGB =churn_prediction_XGB,
            risk_level_XGB=risk_level_XGB,
            shap_values_XGB = json.dumps(shap_values_XGB),
            base_values_XGB = base_values_XGB,
            churn_probability_RF = churn_probability_RF,
            churn_prediction_RF = churn_prediction_RF,
            risk_level_RF = risk_level_RF,
            shap_values_RF = json.dumps(shap_values_RF),
            base_values_RF = base_values_RF,
            customerdata =  customer_data.model_dump_json(indent=2) ,
            processeddata = processed_data.to_json()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/model-info")
async def get_model_info():
    """Get information about the loaded model"""
    return {
        "feature_columns": feature_columns,
        "scaler_type": "MinMax",
        "model_type": "XGBoost Classifier - Random Forest Classifier"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)