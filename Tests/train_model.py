import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import xgboost as xgb
import joblib
import json

def load_and_preprocess_data(csv_file_path):

    df = pd.read_csv(csv_file_path)
    
    # Remove user column as it's just an ID
    if 'user' in df.columns:
        df = df.drop('user', axis=1)
    
    # Separate features and target
    X = df.drop('churn', axis=1)
    y = df['churn']
    
    # Handle categorical variables
    categorical_columns = ['housing', 'payment_type', 'zodiac_sign']
    selected_features = [   "purchases_partners",
                            "reward_rate",
                            "cc_recommended",
                            "web_user",
                            "received_loan",
                            "credit_score", 
                            "age",
                            "deposits",
                            "withdrawal",
                            "is_referred",
                            "registered_phones",
                            "ios_user",
                            "waiting_4_loan",
                            "cancelled_loan",
                            "rejected_loan",
                            "left_for_two_month_plus",
                            "left_for_one_month"]
    X = X[selected_features]
    return X, y

def train_xgboost_model(X, y):
    """Train XGBoost classifier"""
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Create XGBoost classifier
    model = xgb.XGBClassifier(
        objective='binary:logistic',
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        eval_metric='logloss'
    )
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    auc_score = roc_auc_score(y_test, y_pred_proba)
    
    print(f"Model Performance:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"AUC Score: {auc_score:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    return model, X.columns.tolist()

def train_rf_model(X, y):
    """Train Random Forest classifier"""
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Create RF classifier
    model = RandomForestClassifier()
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    auc_score = roc_auc_score(y_test, y_pred_proba)
    model.feature_importances_
    
    print(f"Model Performance:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"AUC Score: {auc_score:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    return model, X.columns.tolist()    

def save_model_and_metadata(model, feature_columns ,modelname):
    """Save the trained model and preprocessing metadata"""
    # Save the models
    joblib.dump(model, f'Modelos/{modelname}.pkl')
    
    
    # Save feature columns 
    
    metadata = {
        'feature_columns': feature_columns        
    }
    
    with open(f'Modelos/{modelname}_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("Model and metadata saved successfully!")

if __name__ == "__main__":
    # Configuration
    csv_file = "Fintech_user_limpio.csv"  # Update this path to your CSV file
    try:
        X, y = load_and_preprocess_data(csv_file)
        print(f"Data loaded successfully. Shape: {X.shape}")
        
        # Train the models
        print(f"XGBoost model training...")
        modelXGB, feature_columnsXGB = train_xgboost_model(X, y)
        print(f"Random Forest model training...")
        modelRF, feature_columnsRF = train_rf_model(X, y)
        
        # Save model and metadata
        save_model_and_metadata(modelXGB, feature_columnsXGB,"XGB")
        save_model_and_metadata(modelRF, feature_columnsRF,"RF")
        
    except FileNotFoundError:
        print(f"Error: Could not find {csv_file}")
        print("Please ensure your CSV file is in the same directory and named 'churn_data.csv'")
    except Exception as e:
        print(f"Error during training: {str(e)}")