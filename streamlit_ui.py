import streamlit as st
import streamlit.components.v1
import pandas as pd
import numpy as np
import requests
import json
from faker import Faker
import shap
import matplotlib.pyplot as plt
import joblib
import plotly.express as px
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Panel de Predicción de Abandono Fintech",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Faker
fake = Faker()

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = pd.DataFrame()
if 'selected_customer' not in st.session_state:
    st.session_state.selected_customer = None
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None
if 'llm_insights' not in st.session_state:
    st.session_state.llm_insights = ""
if 'insights_method' not in st.session_state:
    st.session_state.insights_method = ""
if 'selection_counter' not in st.session_state:
    st.session_state.selection_counter = 0
if 'shap_plot' not in st.session_state:
    st.session_state.shap_plot = None

def load_sample_data():
    """Load sample data for demonstration"""
    np.random.seed(42)
    n_samples = 100
    
    sample_data = {
        "age": np.random.randint(18, 80, n_samples),
        "housing": np.random.choice(["o", "r", "na"], n_samples),
        "credit_score": np.random.normal(650, 100, n_samples).clip(300, 850),
        "deposits": np.random.poisson(5, n_samples),
        "withdrawal": np.random.poisson(3, n_samples),
        "purchases_partners": np.random.poisson(10, n_samples),
        "purchases": np.random.poisson(25, n_samples),
        "cc_taken": np.random.binomial(1, 0.3, n_samples),
        "cc_recommended": np.random.binomial(1, 0.4, n_samples),
        "cc_disliked": np.random.binomial(1, 0.2, n_samples),
        "cc_liked": np.random.binomial(1, 0.6, n_samples),
        "cc_application_begin": np.random.binomial(1, 0.3, n_samples),
        "app_downloaded": np.random.binomial(1, 0.7, n_samples),
        "web_user": np.random.binomial(1, 0.8, n_samples),
        "app_web_user": np.random.binomial(1, 0.5, n_samples),
        "ios_user": np.random.binomial(1, 0.4, n_samples),
        "android_user": np.random.binomial(1, 0.6, n_samples),
        "registered_phones": np.random.poisson(1, n_samples),
        "payment_type": np.random.choice(["monthly", "bi-weekly", "weekly", "semi-monthly", "na"], n_samples),
        "waiting_4_loan": np.random.binomial(1, 0.1, n_samples),
        "cancelled_loan": np.random.binomial(1, 0.05, n_samples),
        "received_loan": np.random.binomial(1, 0.2, n_samples),
        "rejected_loan": np.random.binomial(1, 0.1, n_samples),
        "zodiac_sign": np.random.choice(["aries", "taurus", "gemini", "cancer", "leo", "virgo", 
                                       "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"], n_samples),
        "left_for_two_month_plus": np.random.binomial(1, 0.1, n_samples),
        "left_for_one_month": np.random.binomial(1, 0.15, n_samples),
        "rewards_earned": np.random.poisson(100, n_samples),
        "reward_rate": np.random.uniform(0.01, 0.05, n_samples),
        "is_referred": np.random.binomial(1, 0.3, n_samples)
    }
    
    df = pd.DataFrame(sample_data)
    add_personal_info_columns(df)
    return df

def add_personal_info_columns(df):
    """Add personal information columns using Faker"""
    if 'Name' not in df.columns:
        df['Name'] = [fake.first_name() for _ in range(len(df))]
    if 'Surname' not in df.columns:
        df['Surname'] = [fake.last_name() for _ in range(len(df))]
    if 'email' not in df.columns:
        df['email'] = [fake.email() for _ in range(len(df))]
    if 'phone' not in df.columns:
        df['phone'] = [fake.phone_number() for _ in range(len(df))]
    if 'address' not in df.columns:
        df['address'] = [fake.address().replace('\n', ', ') for _ in range(len(df))]

def get_display_value(column, value):
    """Get user-friendly display value for coded fields"""
    if column == 'housing':
        housing_map = {'o': 'Propia', 'r': 'Alquilada', 'na': 'No disponible'}
        return housing_map.get(value, value)
    elif column == 'payment_type':
        payment_map = {
            'monthly': 'Mensual', 
            'bi-weekly': 'Quincenal', 
            'weekly': 'Semanal', 
            'semi-monthly': 'Bimensual', 
            'na': 'No disponible'
        }
        return payment_map.get(value, value)
    return value

def get_all_required_columns():
    """Get all columns that should be present in the dataset"""
    return {
        # Personal Information
        'Name': 'string',
        'Surname': 'string', 
        'email': 'string',
        'phone': 'string',
        'address': 'string',
        
        # Demographics & Finance
        'age': 'integer',
        'housing': 'categorical',
        'credit_score': 'float',
        'payment_type': 'categorical',
        'zodiac_sign': 'categorical',
        
        # Banking Activity
        'deposits': 'integer',
        'withdrawal': 'integer',
        'purchases_partners': 'integer',
        'purchases': 'integer',
        'registered_phones': 'integer',
        
        # Credit Card Activity
        'cc_taken': 'binary',
        'cc_recommended': 'binary',
        'cc_disliked': 'binary',
        'cc_liked': 'binary',
        'cc_application_begin': 'binary',
        
        # Digital Engagement
        'app_downloaded': 'binary',
        'web_user': 'binary',
        'app_web_user': 'binary',
        'ios_user': 'binary',
        'android_user': 'binary',
        
        # Loan Activity
        'waiting_4_loan': 'binary',
        'cancelled_loan': 'binary',
        'received_loan': 'binary',
        'rejected_loan': 'binary',
        
        # Behavioral Patterns
        'left_for_two_month_plus': 'binary',
        'left_for_one_month': 'binary',
        
        # Rewards & Referrals
        'rewards_earned': 'integer',
        'reward_rate': 'float',
        'is_referred': 'binary'
    }

def generate_missing_data(df, column_name, data_type, num_rows):
    """Generate realistic data for a missing column"""
    np.random.seed(42)  # For reproducible results
    
    if data_type == 'string':
        if column_name == 'Name':
            return [fake.first_name() for _ in range(num_rows)]
        elif column_name == 'Surname':
            return [fake.last_name() for _ in range(num_rows)]
        elif column_name == 'email':
            return [fake.email() for _ in range(num_rows)]
        elif column_name == 'phone':
            return [fake.phone_number() for _ in range(num_rows)]
        elif column_name == 'address':
            return [fake.address().replace('\n', ', ') for _ in range(num_rows)]
    
    elif data_type == 'integer':
        if column_name == 'age':
            return np.random.randint(18, 80, num_rows)
        elif column_name == 'deposits':
            return np.random.poisson(5, num_rows)
        elif column_name == 'withdrawal':
            return np.random.poisson(3, num_rows)
        elif column_name == 'purchases_partners':
            return np.random.poisson(10, num_rows)
        elif column_name == 'purchases':
            return np.random.poisson(25, num_rows)
        elif column_name == 'registered_phones':
            return np.random.poisson(1, num_rows)
        elif column_name == 'rewards_earned':
            return np.random.poisson(100, num_rows)
        else:
            return np.random.randint(0, 10, num_rows)
    
    elif data_type == 'float':
        if column_name == 'credit_score':
            return np.random.normal(650, 100, num_rows).clip(300, 850)
        elif column_name == 'reward_rate':
            return np.random.uniform(0.01, 0.05, num_rows)
        else:
            return np.random.uniform(0, 1, num_rows)
    
    elif data_type == 'binary':
        # Different probabilities for different binary fields
        if column_name in ['cc_taken', 'cc_application_begin']:
            prob = 0.3
        elif column_name in ['app_downloaded', 'web_user']:
            prob = 0.7
        elif column_name in ['cc_disliked', 'cancelled_loan', 'rejected_loan']:
            prob = 0.2
        elif column_name in ['cc_liked', 'received_loan']:
            prob = 0.6
        elif column_name in ['left_for_two_month_plus', 'left_for_one_month']:
            prob = 0.1
        else:
            prob = 0.5
        return np.random.binomial(1, prob, num_rows)
    
    elif data_type == 'categorical':
        if column_name == 'housing':
            return np.random.choice(['o', 'r', 'na'], num_rows)
        elif column_name == 'payment_type':
            return np.random.choice(['monthly', 'bi-weekly', 'weekly', 'semi-monthly', 'na'], num_rows)
        elif column_name == 'zodiac_sign':
            return np.random.choice(['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
                                   'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'], num_rows)
    
    # Default fallback
    return [None] * num_rows

def complete_missing_columns(df):
    """Add missing columns and generate realistic data"""
    required_columns = get_all_required_columns()
    missing_columns = []
    num_rows = len(df)
    
    for column_name, data_type in required_columns.items():
        if column_name not in df.columns:
            missing_columns.append(column_name)
            # Generate data for missing column
            generated_data = generate_missing_data(df, column_name, data_type, num_rows)
            df[column_name] = generated_data
    
    return df, missing_columns

def validate_and_fix_csv_data(df):
    """Validate CSV data and fix any issues"""
    original_columns = list(df.columns)
    
    # Complete missing columns
    df, missing_columns = complete_missing_columns(df)
    
    # Fix data types and invalid values
    fixes_applied = []
    
    # Fix age column
    if 'age' in df.columns:
        try:
            df['age'] = pd.to_numeric(df['age'], errors='coerce')
            # Fill NaN ages with random values
            nan_count = df['age'].isna().sum()
            if nan_count > 0:
                df.loc[df['age'].isna(), 'age'] = np.random.randint(18, 80, nan_count)
                fixes_applied.append(f"Se corrigieron {nan_count} valores de edad inválidos")
            # Ensure age is within reasonable bounds
            df.loc[df['age'] < 18, 'age'] = 18
            df.loc[df['age'] > 100, 'age'] = 100
        except Exception as e:
            fixes_applied.append(f"Problema en columna de edad: {str(e)}")
    
    # Fix credit_score column
    if 'credit_score' in df.columns:
        try:
            df['credit_score'] = pd.to_numeric(df['credit_score'], errors='coerce')
            # Fill NaN credit scores
            nan_count = df['credit_score'].isna().sum()
            if nan_count > 0:
                df.loc[df['credit_score'].isna(), 'credit_score'] = np.random.normal(650, 100, nan_count).clip(300, 850)
                fixes_applied.append(f"Se corrigieron {nan_count} valores de puntaje crediticio inválidos")
            # Ensure credit score is within bounds
            df.loc[df['credit_score'] < 300, 'credit_score'] = 300
            df.loc[df['credit_score'] > 850, 'credit_score'] = 850
        except Exception as e:
            fixes_applied.append(f"Problema en puntaje crediticio: {str(e)}")
    
    # Fix categorical columns
    categorical_defaults = {
        'housing': 'r',
        'payment_type': 'monthly',
        'zodiac_sign': 'leo'
    }
    
    for col, default_val in categorical_defaults.items():
        if col in df.columns:
            # Fill missing categorical values
            missing_count = df[col].isna().sum()
            if missing_count > 0:
                df[col] = df[col].fillna(default_val)
                fixes_applied.append(f"Se corrigieron {missing_count} valores faltantes de {col}")
    
    # Fix binary columns (should be 0 or 1)
    binary_columns = [col for col, dtype in get_all_required_columns().items() if dtype == 'binary']
    for col in binary_columns:
        if col in df.columns:
            # Convert to numeric and fill NaN with 0
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            # Ensure values are 0 or 1
            df[col] = df[col].apply(lambda x: 1 if x > 0.5 else 0)
    
    # Fix integer columns
    integer_columns = [col for col, dtype in get_all_required_columns().items() if dtype == 'integer']
    for col in integer_columns:
        if col in df.columns and col not in ['age']:  # age already handled
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            # Ensure non-negative values for count-based columns
            df[col] = df[col].abs()
    
    return df, missing_columns, fixes_applied

def apply_enhanced_filters(data, filter_params):
    """Apply enhanced filters to the data"""
    filtered = data.copy()
    
    # Demographic filters
    age_range = filter_params['age_range']
    filtered = filtered[
        (filtered['age'] >= age_range[0]) & 
        (filtered['age'] <= age_range[1])
    ]
    
    housing_filter = filter_params['housing_filter']
    if housing_filter not in ["All", "Todos"]:
        filtered = filtered[filtered['housing'] == housing_filter]
    
    payment_filter = filter_params['payment_filter']
    if payment_filter not in ["All", "Todos"]:
        filtered = filtered[filtered['payment_type'] == payment_filter]
    
    # Financial filters
    credit_range = filter_params['credit_range']
    filtered = filtered[
        (filtered['credit_score'] >= credit_range[0]) & 
        (filtered['credit_score'] <= credit_range[1])
    ]
    
    deposits_range = filter_params['deposits_range']
    filtered = filtered[
        (filtered['deposits'] >= deposits_range[0]) & 
        (filtered['deposits'] <= deposits_range[1])
    ]
    
    purchases_range = filter_params['purchases_range']
    filtered = filtered[
        (filtered['purchases'] >= purchases_range[0]) & 
        (filtered['purchases'] <= purchases_range[1])
    ]
    
    rewards_range = filter_params['rewards_range']
    filtered = filtered[
        (filtered['rewards_earned'] >= rewards_range[0]) & 
        (filtered['rewards_earned'] <= rewards_range[1])
    ]
    
    # Digital activity filters
    app_downloaded_filter = filter_params['app_downloaded_filter']
    if app_downloaded_filter == "Sí":
        filtered = filtered[filtered['app_downloaded'] == 1]
    elif app_downloaded_filter == "No":
        filtered = filtered[filtered['app_downloaded'] == 0]
    
    web_user_filter = filter_params['web_user_filter']
    if web_user_filter == "Sí":
        filtered = filtered[filtered['web_user'] == 1]
    elif web_user_filter == "No":
        filtered = filtered[filtered['web_user'] == 0]
    
    platform_filter = filter_params['platform_filter']
    if platform_filter == "iOS":
        filtered = filtered[filtered['ios_user'] == 1]
    elif platform_filter == "Android":
        filtered = filtered[filtered['android_user'] == 1]
    elif platform_filter == "Ambos":
        filtered = filtered[(filtered['ios_user'] == 1) & (filtered['android_user'] == 1)]
    elif platform_filter == "Ninguno":
        filtered = filtered[(filtered['ios_user'] == 0) & (filtered['android_user'] == 0)]
    
    # Banking product filters
    cc_taken_filter = filter_params['cc_taken_filter']
    if cc_taken_filter == "Tomada":
        filtered = filtered[filtered['cc_taken'] == 1]
    elif cc_taken_filter == "No Tomada":
        filtered = filtered[filtered['cc_taken'] == 0]
    
    loan_status_filter = filter_params['loan_status_filter']
    if loan_status_filter == "Recibido":
        filtered = filtered[filtered['received_loan'] == 1]
    elif loan_status_filter == "Rechazado":
        filtered = filtered[filtered['rejected_loan'] == 1]
    elif loan_status_filter == "Esperando":
        filtered = filtered[filtered['waiting_4_loan'] == 1]
    elif loan_status_filter == "Cancelado":
        filtered = filtered[filtered['cancelled_loan'] == 1]
    elif loan_status_filter == "Sin Actividad":
        filtered = filtered[
            (filtered['received_loan'] == 0) & 
            (filtered['rejected_loan'] == 0) & 
            (filtered['waiting_4_loan'] == 0) & 
            (filtered['cancelled_loan'] == 0)
        ]
    
    cc_sentiment_filter = filter_params['cc_sentiment_filter']
    if cc_sentiment_filter == "Positivo":
        filtered = filtered[filtered['cc_liked'] == 1]
    elif cc_sentiment_filter == "Negativo":
        filtered = filtered[filtered['cc_disliked'] == 1]
    elif cc_sentiment_filter == "Neutral":
        filtered = filtered[(filtered['cc_liked'] == 0) & (filtered['cc_disliked'] == 0)]
    
    # Risk filters
    activity_filter = filter_params['activity_filter']
    if activity_filter == "Activo":
        filtered = filtered[
            (filtered['left_for_one_month'] == 0) & 
            (filtered['left_for_two_month_plus'] == 0)
        ]
    elif activity_filter == "Inactivo 1 Mes":
        filtered = filtered[filtered['left_for_one_month'] == 1]
    elif activity_filter == "Inactivo 2+ Meses":
        filtered = filtered[filtered['left_for_two_month_plus'] == 1]
    
    referral_filter = filter_params['referral_filter']
    if referral_filter == "Referido":
        filtered = filtered[filtered['is_referred'] == 1]
    elif referral_filter == "No Referido":
        filtered = filtered[filtered['is_referred'] == 0]
    
    return filtered

def get_active_filters(filter_params):
    """Get a list of active filter descriptions"""
    active_filters = []
    
    # Check demographic filters
    age_range = filter_params['age_range']
    if age_range != (18, 80):
        active_filters.append(f"Edad: {age_range[0]}-{age_range[1]} años")
    
    if filter_params['housing_filter'] not in ["All", "Todos"]:
        active_filters.append(f"Vivienda: {filter_params['housing_filter']}")
    
    if filter_params['payment_filter'] not in ["All", "Todos"]:
        active_filters.append(f"Pago: {filter_params['payment_filter']}")
    
    # Check financial filters
    credit_range = filter_params['credit_range']
    if credit_range != (300, 850):
        active_filters.append(f"Crédito: {credit_range[0]}-{credit_range[1]}")
    
    # Check digital activity filters
    if filter_params['app_downloaded_filter'] != "Todos":
        active_filters.append(f"App: {filter_params['app_downloaded_filter']}")
    
    if filter_params['web_user_filter'] != "Todos":
        active_filters.append(f"Web: {filter_params['web_user_filter']}")
    
    if filter_params['platform_filter'] != "Todos":
        active_filters.append(f"Plataforma: {filter_params['platform_filter']}")
    
    # Check banking product filters
    if filter_params['cc_taken_filter'] != "Todos":
        active_filters.append(f"TC: {filter_params['cc_taken_filter']}")
    
    if filter_params['loan_status_filter'] != "Todos":
        active_filters.append(f"Préstamo: {filter_params['loan_status_filter']}")
    
    if filter_params['cc_sentiment_filter'] != "Todos":
        active_filters.append(f"Sentimiento TC: {filter_params['cc_sentiment_filter']}")
    
    # Check risk filters
    if filter_params['activity_filter'] != "Todos":
        active_filters.append(f"Actividad: {filter_params['activity_filter']}")
    
    if filter_params['referral_filter'] != "Todos":
        active_filters.append(f"Referido: {filter_params['referral_filter']}")
    
    return active_filters

def run_batch_analysis(filtered_data, include_predictions=True, include_insights=False, use_transformers=False):
    """Run batch analysis on filtered customer data"""
    
    results = []
    total_customers = len(filtered_data)
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        for idx, (_, customer) in enumerate(filtered_data.iterrows()):
            # Update progress
            progress = (idx + 1) / total_customers
            progress_bar.progress(progress)
            status_text.text(f"Procesando cliente {idx + 1} de {total_customers}: {customer.get('Name', 'Cliente')} {customer.get('Surname', '')}")
            
            # Prepare customer result
            customer_result = {
                'Name': customer.get('Name', 'Desconocido'),
                'Surname': customer.get('Surname', 'Cliente'),
                'email': customer.get('email', 'N/A'),
                'age': customer.get('age', 0),
                'credit_score': customer.get('credit_score', 0),
                'housing': customer.get('housing', 'N/A'),
                'app_downloaded': customer.get('app_downloaded', 0),
                'purchases': customer.get('purchases', 0),
                'deposits': customer.get('deposits', 0)
            }
            
            # Run predictions if requested
            if include_predictions:
                try:
                    prediction_result, error = predict_churn(customer.to_dict())
                    if prediction_result:
                        customer_result.update({
                            'churn_probability_XGB': prediction_result.get('churn_probability_XGB', 0),
                            'risk_level_XGB': prediction_result.get('risk_level_XGB', 'Unknown'),
                            'churn_prediction_XGB': prediction_result.get('churn_prediction_XGB', 0),
                            'churn_probability_RF': prediction_result.get('churn_probability_RF', 0),
                            'risk_level_RF': prediction_result.get('risk_level_RF', 'Unknown'),
                            'prediction_status': 'Success'
                        })
                    else:
                        customer_result.update({
                            'churn_probability_XGB': 0,
                            'risk_level_XGB': 'Error',
                            'churn_prediction_XGB': 0,
                            'churn_probability_RF': 0,
                            'risk_level_RF': 'Error',
                            'prediction_status': f'Error: {error}'
                        })
                except Exception as e:
                    customer_result.update({
                        'churn_probability_XGB': 0,
                        'risk_level_XGB': 'Error',
                        'churn_prediction_XGB': 0,
                        'churn_probability_RF': 0,
                        'risk_level_RF': 'Error',
                        'prediction_status': f'Exception: {str(e)}'
                    })
            
            # Run insights if requested
            if include_insights and include_predictions and customer_result.get('prediction_status') == 'Success':
                try:
                    # Create a mock prediction result for insights
                    mock_prediction = {
                        'churn_probability_XGB': customer_result['churn_probability_XGB'],
                        'risk_level_XGB': customer_result['risk_level_XGB'],
                        'churn_prediction_XGB': customer_result['churn_prediction_XGB']
                    }
                    
                    insights, error = get_llm_insights(customer.to_dict(), mock_prediction, use_transformers)
                    if insights:
                        # Truncate insights for table display
                        customer_result['insights'] = insights[:200] + "..." if len(insights) > 200 else insights
                        customer_result['insights_full'] = insights
                        customer_result['insights_status'] = 'Success'
                    else:
                        customer_result['insights'] = f"Error: {error}"
                        customer_result['insights_full'] = f"Error: {error}"
                        customer_result['insights_status'] = 'Error'
                except Exception as e:
                    customer_result['insights'] = f"Exception: {str(e)}"
                    customer_result['insights_full'] = f"Exception: {str(e)}"
                    customer_result['insights_status'] = 'Error'
            elif include_insights:
                customer_result['insights'] = "Requiere predicción exitosa"
                customer_result['insights_full'] = "Requiere predicción exitosa"
                customer_result['insights_status'] = 'Skipped'
            
            results.append(customer_result)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        return pd.DataFrame(results)
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"Error en análisis masivo: {str(e)}")
        return None

def prepare_batch_results_for_export(batch_results):
    """Prepare batch results for CSV export"""
    
    # Create a copy for export
    export_df = batch_results.copy()
    
    # Replace full insights if available
    if 'insights_full' in export_df.columns:
        export_df['insights'] = export_df['insights_full']
        export_df = export_df.drop('insights_full', axis=1)
    
    # Format numerical columns
    if 'churn_probability_XGB' in export_df.columns:
        export_df['churn_probability_XGB'] = export_df['churn_probability_XGB'].apply(lambda x: f"{x:.4f}" if isinstance(x, (int, float)) else x)
    
    if 'churn_probability_RF' in export_df.columns:
        export_df['churn_probability_RF'] = export_df['churn_probability_RF'].apply(lambda x: f"{x:.4f}" if isinstance(x, (int, float)) else x)
    
    # Convert to CSV
    return export_df.to_csv(index=False)

def generate_email_campaign_content(customer_data, campaign_type="retention", personalization_level="high"):
    """Generate personalized email marketing content based on customer data and risk profile"""
    
    # Extract customer information
    name = customer_data.get('Name', 'Cliente')
    age = customer_data.get('age', 30)
    credit_score = customer_data.get('credit_score', 650)
    risk_level = customer_data.get('risk_level_XGB', 'Medium')
    churn_prob = customer_data.get('churn_probability_XGB', 0.5)
    app_downloaded = customer_data.get('app_downloaded', 0)
    cc_taken = customer_data.get('cc_taken', 0)
    purchases = customer_data.get('purchases', 10)
    deposits = customer_data.get('deposits', 5)
    rewards_earned = customer_data.get('rewards_earned', 100)
    
    # Determine campaign strategy based on risk level
    if risk_level == "High":
        campaign_strategy = "urgent_retention"
        urgency_level = "alta"
        subject_prefix = "🚨 IMPORTANTE:"
    elif risk_level == "Medium":
        campaign_strategy = "proactive_engagement"
        urgency_level = "media"
        subject_prefix = "💡 Oportunidad especial:"
    else:
        campaign_strategy = "loyalty_building"
        urgency_level = "baja"
        subject_prefix = "🎁 Para ti:"
    
    # Generate personalized subject lines
    subject_lines = {
        "urgent_retention": [
            f"{subject_prefix} {name}, te extrañamos - Oferta exclusiva dentro",
            f"{subject_prefix} {name}, vuelve con nosotros - Beneficios especiales",
            f"{subject_prefix} No pierdas tus beneficios, {name} - Acción requerida"
        ],
        "proactive_engagement": [
            f"{subject_prefix} {name}, nuevas funciones que te encantarán",
            f"{subject_prefix} Maximiza tus beneficios, {name}",
            f"{subject_prefix} {name}, descubre lo que te estás perdiendo"
        ],
        "loyalty_building": [
            f"{subject_prefix} {name}, gracias por ser parte de nuestra familia",
            f"{subject_prefix} Nuevas recompensas disponibles para ti, {name}",
            f"{subject_prefix} {name}, tu experiencia premium te espera"
        ]
    }
    
    # Generate personalized email content
    if campaign_strategy == "urgent_retention":
        email_content = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #e74c3c;">¡{name}, te extrañamos!</h1>
        
        <p>Hola {name},</p>
        
        <p>Hemos notado que no has estado tan activo últimamente, y queremos asegurarnos de que tengas todo lo que necesitas para aprovechar al máximo tu cuenta.</p>
        
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #e74c3c; margin-top: 0;">🎁 Oferta Especial Solo Para Ti</h3>
            <ul>
                {"<li>Bonificación de $50 por reactivar tu cuenta</li>" if deposits < 3 else ""}
                {"<li>Descarga nuestra app y recibe $25 adicionales</li>" if not app_downloaded else ""}
                {"<li>Tarjeta de crédito sin cuota anual por 12 meses</li>" if not cc_taken and credit_score > 600 else ""}
                <li>Soporte premium gratuito por 3 meses</li>
                <li>Acceso exclusivo a nuestro programa VIP</li>
            </ul>
        </div>
        
        <p><strong>Esta oferta expira en 7 días.</strong> No queremos que te pierdas estos beneficios exclusivos.</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="#" style="background-color: #e74c3c; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">RECLAMAR OFERTA AHORA</a>
        </div>
        
        <p>Si tienes alguna pregunta o necesitas ayuda, nuestro equipo de soporte premium está disponible 24/7 para ti.</p>
        
        <p>Esperamos verte pronto,<br>
        El equipo de [Nombre de la Empresa]</p>
        
        <hr style="margin: 30px 0;">
        <p style="font-size: 12px; color: #666;">
            Si no deseas recibir estos emails, puedes <a href="#">darte de baja aquí</a>.
        </p>
    </div>
</body>
</html>
"""
    
    elif campaign_strategy == "proactive_engagement":
        email_content = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #3498db;">¡Hola {name}! Tenemos algo especial para ti</h1>
        
        <p>Esperamos que estés teniendo una excelente experiencia con nosotros.</p>
        
        <p>Basado en tu perfil y actividad, hemos identificado algunas oportunidades que podrían interesarte:</p>
        
        <div style="background-color: #e8f4fd; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #3498db; margin-top: 0;">💡 Recomendaciones Personalizadas</h3>
            <ul>
                {f"<li>Aumenta tus recompensas: Has ganado {rewards_earned} puntos - ¡descubre cómo ganar más!</li>" if rewards_earned > 50 else "<li>Comienza a ganar recompensas con cada compra</li>"}
                {"<li>Descarga nuestra app móvil para acceso 24/7 y notificaciones en tiempo real</li>" if not app_downloaded else "<li>Explora las nuevas funciones de nuestra app móvil</li>"}
                {f"<li>Con tu excelente puntaje crediticio ({credit_score:.0f}), calificas para productos premium</li>" if credit_score > 700 else "<li>Herramientas gratuitas para mejorar tu puntaje crediticio</li>"}
                <li>Programa de referidos: Gana $25 por cada amigo que invites</li>
            </ul>
        </div>
        
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <h4 style="margin-top: 0;">📊 Tu Actividad Este Mes</h4>
            <p>• Compras realizadas: {purchases}<br>
            • Depósitos: {deposits}<br>
            • Recompensas ganadas: {rewards_earned} puntos</p>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="#" style="background-color: #3498db; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">EXPLORAR BENEFICIOS</a>
        </div>
        
        <p>¿Tienes preguntas? Responde a este email o contáctanos en cualquier momento.</p>
        
        <p>Saludos cordiales,<br>
        Tu equipo de [Nombre de la Empresa]</p>
        
        <hr style="margin: 30px 0;">
        <p style="font-size: 12px; color: #666;">
            Puedes actualizar tus preferencias de email <a href="#">aquí</a>.
        </p>
    </div>
</body>
</html>
"""
    
    else:  # loyalty_building
        email_content = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #27ae60;">¡Gracias por ser un cliente valioso, {name}!</h1>
        
        <p>Tu lealtad significa mucho para nosotros, y queremos asegurarnos de que sigas recibiendo el mejor valor de tu cuenta.</p>
        
        <div style="background-color: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #27ae60; margin-top: 0;">🏆 Beneficios Exclusivos para Ti</h3>
            <ul>
                <li>Acceso prioritario a nuevos productos y funciones</li>
                <li>Tarifas preferenciales en servicios premium</li>
                {f"<li>Bonificación especial: {rewards_earned * 0.1:.0f} puntos adicionales este mes</li>" if rewards_earned > 100 else "<li>Programa de recompensas mejorado disponible</li>"}
                <li>Soporte al cliente dedicado</li>
                <li>Invitaciones exclusivas a eventos y webinars</li>
            </ul>
        </div>
        
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <h4 style="margin-top: 0;">🎯 Nuevas Oportunidades</h4>
            <p>Basado en tu perfil, estos productos podrían interesarte:</p>
            <ul>
                {"<li>Cuenta de ahorros de alto rendimiento</li>" if deposits > 5 else ""}
                {"<li>Servicios de inversión personalizados</li>" if credit_score > 750 else ""}
                {"<li>Programa de cashback premium</li>" if purchases > 20 else ""}
                <li>Herramientas de planificación financiera</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="#" style="background-color: #27ae60; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">DESCUBRIR MÁS</a>
        </div>
        
        <p>Continuamos innovando para ofrecerte la mejor experiencia financiera. ¡Gracias por confiar en nosotros!</p>
        
        <p>Con aprecio,<br>
        El equipo de [Nombre de la Empresa]</p>
        
        <hr style="margin: 30px 0;">
        <p style="font-size: 12px; color: #666;">
            Administra tus preferencias de comunicación <a href="#">aquí</a>.
        </p>
    </div>
</body>
</html>
"""
    
    # Generate campaign metrics and recommendations
    campaign_metrics = {
        "target_audience": f"Clientes con riesgo {risk_level.lower()}",
        "expected_open_rate": "25-35%" if risk_level == "High" else "20-30%" if risk_level == "Medium" else "15-25%",
        "expected_click_rate": "8-12%" if risk_level == "High" else "5-8%" if risk_level == "Medium" else "3-6%",
        "recommended_send_time": "Martes-Jueves, 10:00-14:00",
        "follow_up_strategy": "Email de seguimiento en 3 días si no hay respuesta" if risk_level == "High" else "Email de seguimiento en 7 días",
        "personalization_score": "Alta" if personalization_level == "high" else "Media",
        "urgency_level": urgency_level,
        "campaign_type": campaign_strategy
    }
    
    return {
        "subject_lines": subject_lines[campaign_strategy],
        "email_content": email_content,
        "campaign_metrics": campaign_metrics,
        "customer_segment": f"{risk_level} Risk - {campaign_strategy.replace('_', ' ').title()}"
    }

def create_bulk_email_campaign(filtered_customers, campaign_settings):
    """Create a bulk email campaign for filtered customers"""
    
    campaign_data = []
    
    for idx, customer in filtered_customers.iterrows():
        # Generate personalized content for each customer
        email_campaign = generate_email_campaign_content(
            customer.to_dict(),
            campaign_type=campaign_settings.get('campaign_type', 'retention'),
            personalization_level=campaign_settings.get('personalization_level', 'high')
        )
        
        # Add customer info to campaign data
        campaign_entry = {
            'customer_id': idx,
            'name': customer.get('Name', 'Cliente'),
            'surname': customer.get('Surname', ''),
            'email': customer.get('email', 'no-email@example.com'),
            'risk_level': customer.get('risk_level_XGB', 'Medium'),
            'churn_probability': customer.get('churn_probability_XGB', 0.5),
            'subject_line': email_campaign['subject_lines'][0],  # Use first subject line
            'email_content': email_campaign['email_content'],
            'customer_segment': email_campaign['customer_segment'],
            'expected_open_rate': email_campaign['campaign_metrics']['expected_open_rate'],
            'recommended_send_time': email_campaign['campaign_metrics']['recommended_send_time']
        }
        
        campaign_data.append(campaign_entry)
    
    return pd.DataFrame(campaign_data)

def export_email_campaign_data(campaign_df, format_type="csv"):
    """Export email campaign data in various formats"""
    
    if format_type == "csv":
        return campaign_df.to_csv(index=False)
    elif format_type == "html_preview":
        # Create HTML preview of first few emails
        html_preview = "<html><body>"
        for idx, row in campaign_df.head(3).iterrows():
            html_preview += f"""
            <div style="border: 1px solid #ccc; margin: 20px 0; padding: 20px;">
                <h3>Cliente: {row['name']} {row['surname']} ({row['email']})</h3>
                <h4>Asunto: {row['subject_line']}</h4>
                <div style="border-top: 1px solid #eee; padding-top: 10px;">
                    {row['email_content']}
                </div>
            </div>
            """
        html_preview += "</body></html>"
        return html_preview
    elif format_type == "summary":
        # Create campaign summary
        summary = f"""
RESUMEN DE CAMPAÑA DE EMAIL MARKETING

Total de destinatarios: {len(campaign_df)}

Segmentación por riesgo:
{campaign_df['risk_level'].value_counts().to_string()}

Segmentación por tipo de campaña:
{campaign_df['customer_segment'].value_counts().to_string()}

Métricas esperadas:
- Tasa de apertura promedio: {campaign_df['expected_open_rate'].mode().iloc[0] if not campaign_df.empty else 'N/A'}
- Mejor horario de envío: {campaign_df['recommended_send_time'].mode().iloc[0] if not campaign_df.empty else 'N/A'}

Recomendaciones:
1. Enviar emails de alto riesgo primero (dentro de 24 horas)
2. Programar emails de riesgo medio para 2-3 días después
3. Emails de bajo riesgo pueden enviarse durante la semana siguiente
4. Monitorear métricas de apertura y clics para optimizar futuras campañas
5. Preparar emails de seguimiento basados en la respuesta inicial
"""
        return summary

def display_batch_results(batch_results, include_predictions, include_insights):
    """Display batch results in an interactive table"""
    
    st.markdown("---")
    st.subheader("📊 Resultados del Análisis Masivo")
    
    # Summary statistics
    total_processed = len(batch_results)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Procesados", total_processed)
    
    if include_predictions:
        with col2:
            successful_predictions = (batch_results['prediction_status'] == 'Success').sum()
            st.metric("Predicciones Exitosas", successful_predictions)
        
        with col3:
            if successful_predictions > 0:
                high_risk = (batch_results['risk_level_XGB'] == 'High').sum()
                st.metric("Alto Riesgo", high_risk)
            else:
                st.metric("Alto Riesgo", "N/A")
        
        with col4:
            if successful_predictions > 0:
                avg_churn_prob = batch_results[batch_results['prediction_status'] == 'Success']['churn_probability_XGB'].mean()
                st.metric("Prob. Promedio", f"{avg_churn_prob:.2%}")
            else:
                st.metric("Prob. Promedio", "N/A")
    
    if include_insights:
        st.markdown("### 💡 Resumen de Insights")
        successful_insights = (batch_results.get('insights_status', pd.Series()) == 'Success').sum()
        st.info(f"🧠 Insights generados exitosamente: {successful_insights} de {total_processed}")
    
    # Filter and display options
    st.markdown("### 🔍 Filtrar Resultados")
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        if include_predictions:
            risk_filter = st.selectbox(
                "Filtrar por Riesgo",
                ["Todos"] + list(batch_results['risk_level_XGB'].unique()) if 'risk_level_XGB' in batch_results.columns else ["Todos"],
                key="batch_analysis_risk_filter"
            )
        else:
            risk_filter = "Todos"
    
    with filter_col2:
        if include_predictions:
            status_filter = st.selectbox(
                "Estado de Predicción",
                ["Todos"] + list(batch_results['prediction_status'].unique()) if 'prediction_status' in batch_results.columns else ["Todos"],
                key="batch_analysis_status_filter"
            )
        else:
            status_filter = "Todos"
    
    with filter_col3:
        show_columns = st.multiselect(
            "Columnas a Mostrar",
            options=list(batch_results.columns),
            default=[col for col in ['Name', 'Surname', 'age', 'credit_score', 'churn_probability_XGB', 'risk_level_XGB', 'insights'] 
                    if col in batch_results.columns][:7]  # Show first 7 relevant columns
        )
    
    # Apply filters
    filtered_results = batch_results.copy()
    
    if risk_filter != "Todos" and 'risk_level_XGB' in filtered_results.columns:
        filtered_results = filtered_results[filtered_results['risk_level_XGB'] == risk_filter]
    
    if status_filter != "Todos" and 'prediction_status' in filtered_results.columns:
        filtered_results = filtered_results[filtered_results['prediction_status'] == status_filter]
    
    # Select columns to display
    if show_columns:
        display_df = filtered_results[show_columns]
    else:
        display_df = filtered_results
    
    # Display results table
    st.markdown(f"### 📋 Tabla de Resultados ({len(filtered_results)} filas)")
    
    if len(filtered_results) > 0:
        # Configure AgGrid for batch results
        gb = GridOptionsBuilder.from_dataframe(display_df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
        
        # Configure specific columns
        if 'churn_probability_XGB' in display_df.columns:
            gb.configure_column('churn_probability_XGB', type=["numericColumn", "numberColumnFilter"], precision=4)
        
        if 'insights' in display_df.columns:
            gb.configure_column('insights', wrapText=True, autoHeight=True, width=300)
        
        gridOptions = gb.build()
        
        # Display grid
        AgGrid(
            display_df,
            gridOptions=gridOptions,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            update_mode=GridUpdateMode.NO_UPDATE,
            fit_columns_on_grid_load=True,
            theme='streamlit',
            enable_enterprise_modules=False,
            height=500,
            width='100%'
        )
        
        # Additional analysis
        if include_predictions and len(filtered_results) > 0:
            st.markdown("### 📈 Análisis Adicional")
            
            # Risk distribution
            if 'risk_level_XGB' in filtered_results.columns:
                risk_counts = filtered_results['risk_level_XGB'].value_counts()
                fig_risk = px.pie(
                    values=risk_counts.values,
                    names=risk_counts.index,
                    title="Distribución de Niveles de Riesgo"
                )
                st.plotly_chart(fig_risk, use_container_width=True)
            
            # Churn probability distribution
            if 'churn_probability_XGB' in filtered_results.columns:
                successful_preds = filtered_results[filtered_results['prediction_status'] == 'Success']
                if len(successful_preds) > 0:
                    fig_hist = px.histogram(
                        successful_preds,
                        x='churn_probability_XGB',
                        title="Distribución de Probabilidades de Abandono",
                        nbins=20
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
    
    else:
        st.warning("⚠️ No hay resultados que coincidan con los filtros aplicados.")

# Legacy function for backward compatibility
def apply_filters(data, age_range, credit_range, housing_filter):
    """Legacy apply filters function for backward compatibility"""
    filter_params = {
        'age_range': age_range,
        'credit_range': credit_range,
        'housing_filter': housing_filter,
        'payment_filter': "Todos",
        'deposits_range': (0, data['deposits'].max() if not data.empty else 100),
        'purchases_range': (0, data['purchases'].max() if not data.empty else 100),
        'rewards_range': (0, data['rewards_earned'].max() if not data.empty else 1000),
        'app_downloaded_filter': "Todos",
        'web_user_filter': "Todos",
        'platform_filter': "Todos",
        'cc_taken_filter': "Todos",
        'loan_status_filter': "Todos",
        'cc_sentiment_filter': "Todos",
        'activity_filter': "Todos",
        'referral_filter': "Todos"
    }
    return apply_enhanced_filters(data, filter_params)

def predict_churn(customer_data):
    """Make API call to predict churn"""
    try:
        # Prepare data for API call (exclude personal information)
        api_data = {k: v for k, v in customer_data.items() 
                   if k not in ['Name', 'Surname', 'email', 'phone', 'address']}
        
        # Make API call
        response = requests.post(
            "http://localhost:8000/predict",
            json=api_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.ConnectionError:
        return None, "Error: La API de predicción de abandono no está ejecutándose. Por favor inicia api.py primero."
    except Exception as e:
        return None, f"Error realizando predicción: {str(e)}"

def check_llm_api_health():
    """Check the health status of the LLM API"""
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "transformers_available": False, "rule_based_available": False}
    except:
        return {"status": "error", "transformers_available": False, "rule_based_available": False}

def get_llm_insights(customer_data, prediction_result, use_transformers=False):
    """Get LLM insights for customer retention"""
    try:
        # Prepare data for LLM API (exclude personal information)
        api_data = {k: v for k, v in customer_data.items() 
                   if k not in ['Name', 'Surname', 'email', 'phone', 'address']}
        
        # Add prediction results with correct field names for LLM API
        # Use XGBoost results as primary
        api_data.update({
            'churn_probability': prediction_result.get('churn_probability_XGB', prediction_result.get('churn_probability', 0)),
            'churn_prediction': prediction_result.get('churn_prediction_XGB', prediction_result.get('churn_prediction', 0)),
            'risk_level': prediction_result.get('risk_level_XGB', prediction_result.get('risk_level', 'Unknown'))
        })
        
        # Add transformers option
        api_data['use_transformers'] = use_transformers
        
        # Ensure all required fields are present with defaults
        required_fields = {
            'age': 30,
            'housing': 'r',
            'credit_score': 650.0,
            'deposits': 5,
            'withdrawal': 3,
            'purchases_partners': 10,
            'purchases': 25,
            'cc_taken': 0,
            'cc_recommended': 0,
            'cc_disliked': 0,
            'cc_liked': 0,
            'cc_application_begin': 0,
            'app_downloaded': 0,
            'web_user': 0,
            'app_web_user': 0,
            'ios_user': 0,
            'android_user': 0,
            'registered_phones': 1,
            'payment_type': 'monthly',
            'waiting_4_loan': 0,
            'cancelled_loan': 0,
            'received_loan': 0,
            'rejected_loan': 0,
            'left_for_two_month_plus': 0,
            'left_for_one_month': 0,
            'rewards_earned': 100,
            'reward_rate': 0.02,
            'is_referred': 0
        }
        
        # Fill missing fields with defaults
        for field, default_value in required_fields.items():
            if field not in api_data:
                api_data[field] = default_value
        
        # Convert categorical fields to strings
        if 'housing' in api_data:
            api_data['housing'] = str(api_data['housing'])
        if 'payment_type' in api_data:
            api_data['payment_type'] = str(api_data['payment_type'])
        
        # Make API call to LLM
        response = requests.post(
            "http://localhost:8001/generate-insights",
            json=api_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['recommendations'], None
        else:
            return None, f"LLM API Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.ConnectionError:
        return None, "Error: La API LLM no está ejecutándose. Por favor inicia llm_api.py primero."
    except Exception as e:
        return None, f"Error obteniendo insights de LLM: {str(e)}"

def generate_shap_plot(customer_data):
    """Generate SHAP waterfall plot for selected customer"""
    try:
        # Load the trained model and metadata (same as API)
        model = joblib.load('XGBoost_model.pkl')
        
        # Load feature columns from metadata
        with open('XGBoost_model_metadata.json', 'r') as f:
            metadata = json.load(f)
        feature_columns = metadata['feature_columns']
        
        # Prepare customer data - only include features the model was trained on
        api_data = {}
        for col in feature_columns:
            if col in customer_data:
                api_data[col] = customer_data[col]
            else:
                # Set default values for missing features
                api_data[col] = 0
        
        # Create DataFrame with only the required features
        customer_df = pd.DataFrame([api_data])
        
        # Ensure columns are in the exact order expected by the model
        customer_df = customer_df[feature_columns]
        
        # Ensure all columns are numeric
        for col in customer_df.columns:
            customer_df[col] = pd.to_numeric(customer_df[col], errors='coerce').fillna(0)
        
        # Verify the shape matches expectations
        expected_features = len(feature_columns)
        actual_features = customer_df.shape[1]
        
        if expected_features != actual_features:
            raise ValueError(f"Feature mismatch: expected {expected_features}, got {actual_features}")
        
        # Create SHAP explainer
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(customer_df)
        
        # Create waterfall plot using modern SHAP API
        fig, ax = plt.subplots(figsize=(10, 8))
        
        try:
            # Try modern SHAP API first
            explanation = shap.Explanation(
                values=shap_values[0],
                base_values=explainer.expected_value,
                data=customer_df.iloc[0],
                feature_names=customer_df.columns.tolist()
            )
            
            # Generate waterfall plot with modern API
            shap.waterfall_plot(explanation, show=False)
            
        except Exception as modern_error:
            # Fallback to alternative modern API
            try:
                explanation = shap.Explanation(
                    values=shap_values[0],
                    base_values=explainer.expected_value,
                    data=customer_df.iloc[0],
                    feature_names=customer_df.columns.tolist()
                )
                
                # Use alternative waterfall function
                shap.plots.waterfall(explanation, show=False)
                
            except Exception as alt_error:
                # If both modern APIs fail, raise the original error
                raise Exception(f"SHAP waterfall plot failed. Modern API: {str(modern_error)}, Alternative API: {str(alt_error)}")
        
        plt.title(f"Explicación SHAP para {customer_data.get('Name', 'Cliente')}")
        plt.tight_layout()
        
        return fig, None
        
    except Exception as e:
        return None, f"Error generando gráfico SHAP: {str(e)}"

def create_customer_summary_chart(customer_data):
    """Create a summary chart for the selected customer"""
    try:
        # Prepare data for visualization with safe defaults
        features = {
            'Edad': max(0, min(100, customer_data.get('age', 30))),
            'Puntaje Crediticio': max(0, min(100, customer_data.get('credit_score', 650) / 10)),  # Scale down for visualization
            'Depósitos': max(0, min(50, customer_data.get('deposits', 5))),
            'Compras': max(0, min(100, customer_data.get('purchases', 25))),
            'Recompensas': max(0, min(100, customer_data.get('rewards_earned', 100) / 10)),  # Scale down
            'Uso de App': customer_data.get('app_downloaded', 0) * 100,  # Scale up
        }
        
        fig = go.Figure(data=go.Scatterpolar(
            r=list(features.values()),
            theta=list(features.keys()),
            fill='toself',
            name='Perfil del Cliente'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            title="Resumen del Perfil del Cliente",
            height=400
        )
        
        return fig
    except Exception as e:
        # Return a simple placeholder chart if there's an error
        fig = go.Figure()
        fig.add_annotation(
            text=f"Gráfico no disponible: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        fig.update_layout(title="Resumen del Perfil del Cliente")
        return fig

# Main Streamlit App
def main():
    st.title("🏦 Panel de Predicción de Abandono Fintech")
    st.markdown("---")
    
    # Sidebar for navigation and controls
    st.sidebar.title("🎛️ Controles")
    
    # Data Management Section
    st.sidebar.header("📊 Gestión de Datos")
    
    # Data loading options
    data_option = st.sidebar.radio(
        "Elegir fuente de datos:",
        ["Cargar Datos de Muestra", "Subir Archivo CSV"]
    )
    
    if data_option == "Cargar Datos de Muestra":
        if st.sidebar.button("🔄 Cargar Datos de Muestra"):
            with st.spinner("Cargando datos de muestra..."):
                st.session_state.data = load_sample_data()
                st.session_state.filtered_data = st.session_state.data.copy()
            st.sidebar.success("¡Datos de muestra cargados!")
    
    else:  # Upload CSV File
        uploaded_file = st.sidebar.file_uploader(
            "Elegir un archivo CSV",
            type="csv",
            help="Subir un archivo CSV con datos de clientes"
        )
        
        if uploaded_file is not None:
            try:
                with st.spinner("Cargando y procesando archivo CSV..."):
                    # Read the CSV file
                    df = pd.read_csv(uploaded_file)
                    original_shape = df.shape
                    
                    # Complete missing columns and fix data issues
                    df, missing_columns, fixes_applied = validate_and_fix_csv_data(df)
                    
                    st.session_state.data = df
                    st.session_state.filtered_data = df.copy()
                    
                # Show detailed processing results
                st.sidebar.success(f"✅ ¡CSV procesado! {len(df)} clientes cargados")
                
                if missing_columns:
                    st.sidebar.info(f"📝 Se agregaron {len(missing_columns)} columnas faltantes:")
                    for col in missing_columns[:5]:  # Show first 5
                        st.sidebar.text(f"  • {col}")
                    if len(missing_columns) > 5:
                        st.sidebar.text(f"  • ... y {len(missing_columns) - 5} más")
                
                if fixes_applied:
                    st.sidebar.info(f"🔧 Se aplicaron {len(fixes_applied)} correcciones de datos:")
                    for fix in fixes_applied[:3]:  # Show first 3
                        st.sidebar.text(f"  • {fix}")
                    if len(fixes_applied) > 3:
                        st.sidebar.text(f"  • ... y {len(fixes_applied) - 3} más")
                
                # Show before/after info
                st.sidebar.text(f"📊 Original: {original_shape[1]} columnas")
                st.sidebar.text(f"📊 Final: {df.shape[1]} columnas")
                
            except Exception as e:
                st.sidebar.error(f"❌ Error cargando CSV: {str(e)}")
    
    # Save/Download options
    st.sidebar.markdown("---")
    st.sidebar.subheader("💾 Guardar y Descargar")
    
    # Download template CSV
    template_data = {
        'age': [30, 45, 25],
        'housing': ['o', 'r', 'na'],
        'credit_score': [650, 720, 580],
        'deposits': [5, 8, 3],
        'withdrawal': [3, 5, 2],
        'purchases_partners': [10, 15, 5],
        'purchases': [25, 40, 15],
        'cc_taken': [1, 0, 1],
        'cc_recommended': [0, 1, 0],
        'cc_disliked': [0, 0, 1],
        'cc_liked': [1, 1, 0],
        'cc_application_begin': [1, 0, 0],
        'app_downloaded': [1, 1, 0],
        'web_user': [1, 1, 1],
        'app_web_user': [1, 0, 0],
        'ios_user': [1, 0, 1],
        'android_user': [0, 1, 0],
        'registered_phones': [1, 1, 2],
        'payment_type': ['monthly', 'bi-weekly', 'weekly'],
        'waiting_4_loan': [0, 0, 1],
        'cancelled_loan': [0, 0, 0],
        'received_loan': [1, 0, 0],
        'rejected_loan': [0, 1, 0],
        'zodiac_sign': ['leo', 'virgo', 'aries'],
        'left_for_two_month_plus': [0, 0, 1],
        'left_for_one_month': [0, 1, 0],
        'rewards_earned': [150, 200, 50],
        'reward_rate': [0.02, 0.03, 0.01],
        'is_referred': [1, 0, 1]
    }
    
    template_csv = pd.DataFrame(template_data).to_csv(index=False)
    st.sidebar.download_button(
        label="📋 Descargar Plantilla CSV",
        data=template_csv,
        file_name="plantilla_clientes.csv",
        mime="text/csv",
        help="Descargar un archivo CSV de ejemplo"
    )
    
    # Save current data
    if not st.session_state.data.empty:
        csv_data = st.session_state.data.to_csv(index=False)
        st.sidebar.download_button(
            label="📁 Descargar Datos Actuales",
            data=csv_data,
            file_name="datos_clientes.csv",
            mime="text/csv",
            help="Descargar los datos actuales de clientes"
        )
    
    # Show data info if data exists
    if not st.session_state.data.empty:
        st.sidebar.info(f"📈 Total de clientes: {len(st.session_state.data)}")
        
        # Show selected customer in sidebar
        if st.session_state.selected_customer is not None:
            customer = st.session_state.selected_customer
            name = customer.get('Name', 'Desconocido')
            surname = customer.get('Surname', 'Cliente')
            
            # Handle None/NaN values
            if pd.isna(name) or name is None:
                name = 'Desconocido'
            if pd.isna(surname) or surname is None:
                surname = 'Cliente'
            
            st.sidebar.success(f"🎯 Seleccionado: {name} {surname}")
            
            if st.sidebar.button("🗑️ Limpiar Selección de Cliente"):
                st.session_state.selected_customer = None
                st.session_state.prediction_result = None
                st.session_state.llm_insights = ""
                if 'shap_plot' in st.session_state:
                    del st.session_state.shap_plot
                st.rerun()
        
        # Enhanced Filters
        st.sidebar.subheader("🔍 Filtros Avanzados")
        
        # Filter reset button
        if st.sidebar.button("🔄 Restablecer Filtros"):
            st.session_state.filtered_data = st.session_state.data.copy()
            st.rerun()
        
        # Expandable filter sections
        with st.sidebar.expander("👤 Filtros Demográficos", expanded=True):
            age_range = st.slider(
                "Rango de Edad",
                min_value=18,
                max_value=80,
                value=(18, 80),
                step=1
            )
            
            housing_options = ["Todos"] + list(st.session_state.data['housing'].unique())
            housing_filter = st.selectbox("Tipo de Vivienda", housing_options, 
                                        format_func=lambda x: get_display_value('housing', x) if x != "Todos" else x,
                                        key="main_housing_filter")
            
            payment_options = ["Todos"] + list(st.session_state.data['payment_type'].unique())
            payment_filter = st.selectbox("Tipo de Pago", payment_options,
                                        format_func=lambda x: get_display_value('payment_type', x) if x != "Todos" else x,
                                        key="main_payment_filter")
        
        with st.sidebar.expander("💳 Filtros Financieros", expanded=False):
            credit_range = st.slider(
                "Rango de Puntaje Crediticio",
                min_value=300,
                max_value=850,
                value=(300, 850),
                step=10
            )
            
            deposits_range = st.slider(
                "Número de Depósitos",
                min_value=0,
                max_value=int(st.session_state.data['deposits'].max()),
                value=(0, int(st.session_state.data['deposits'].max())),
                step=1
            )
            
            purchases_range = st.slider(
                "Número de Compras",
                min_value=0,
                max_value=int(st.session_state.data['purchases'].max()),
                value=(0, int(st.session_state.data['purchases'].max())),
                step=1
            )
            
            rewards_range = st.slider(
                "Recompensas Ganadas",
                min_value=0,
                max_value=int(st.session_state.data['rewards_earned'].max()),
                value=(0, int(st.session_state.data['rewards_earned'].max())),
                step=10
            )
        
        with st.sidebar.expander("📱 Filtros de Actividad Digital", expanded=False):
            app_downloaded_filter = st.selectbox(
                "App Descargada",
                ["Todos", "Sí", "No"],
                key="main_app_downloaded_filter"
            )
            
            web_user_filter = st.selectbox(
                "Usuario Web",
                ["Todos", "Sí", "No"],
                key="main_web_user_filter"
            )
            
            platform_filter = st.selectbox(
                "Plataforma Móvil",
                ["Todos", "iOS", "Android", "Ambos", "Ninguno"],
                key="main_platform_filter"
            )
        
        with st.sidebar.expander("🏦 Filtros de Productos Bancarios", expanded=False):
            cc_taken_filter = st.selectbox(
                "Tarjeta de Crédito",
                ["Todos", "Tomada", "No Tomada"],
                key="main_cc_taken_filter"
            )
            
            loan_status_filter = st.selectbox(
                "Estado de Préstamo",
                ["Todos", "Recibido", "Rechazado", "Esperando", "Cancelado", "Sin Actividad"],
                key="main_loan_status_filter"
            )
            
            cc_sentiment_filter = st.selectbox(
                "Sentimiento hacia TC",
                ["Todos", "Positivo", "Negativo", "Neutral"],
                key="main_cc_sentiment_filter"
            )
        
        with st.sidebar.expander("⚠️ Filtros de Riesgo", expanded=False):
            activity_filter = st.selectbox(
                "Patrón de Actividad",
                ["Todos", "Activo", "Inactivo 1 Mes", "Inactivo 2+ Meses"],
                key="main_activity_filter"
            )
            
            referral_filter = st.selectbox(
                "Estado de Referido",
                ["Todos", "Referido", "No Referido"],
                key="main_referral_filter"
            )
        
        # Apply enhanced filters
        filter_params = {
            'age_range': age_range,
            'credit_range': credit_range,
            'housing_filter': housing_filter,
            'payment_filter': payment_filter,
            'deposits_range': deposits_range,
            'purchases_range': purchases_range,
            'rewards_range': rewards_range,
            'app_downloaded_filter': app_downloaded_filter,
            'web_user_filter': web_user_filter,
            'platform_filter': platform_filter,
            'cc_taken_filter': cc_taken_filter,
            'loan_status_filter': loan_status_filter,
            'cc_sentiment_filter': cc_sentiment_filter,
            'activity_filter': activity_filter,
            'referral_filter': referral_filter
        }
        
        st.session_state.filtered_data = apply_enhanced_filters(
            st.session_state.data, filter_params
        )
        
        # Filter summary
        total_customers = len(st.session_state.data)
        filtered_customers = len(st.session_state.filtered_data)
        filter_percentage = (filtered_customers / total_customers * 100) if total_customers > 0 else 0
        
        st.sidebar.info(f"🔍 Filtrados: {filtered_customers} de {total_customers} clientes ({filter_percentage:.1f}%)")
        
        # Show active filters
        active_filters = get_active_filters(filter_params)
        if active_filters:
            st.sidebar.markdown("**Filtros Activos:**")
            for filter_desc in active_filters:
                st.sidebar.markdown(f"• {filter_desc}")
    
    # Main content area
    if st.session_state.data.empty:
        st.info("👆 ¡Por favor carga datos de muestra desde la barra lateral para comenzar!")
        return
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📊 Datos de Clientes", "➕ Agregar Cliente", "📈 Dashboard Power BI", "🤖 Predicciones", "💡 Insights", "📊 Análisis Masivo", "📧 Email Marketing"])
    
    with tab1:
        st.header("📊 Datos de Clientes")
        
        if not st.session_state.filtered_data.empty:
            # Filter summary banner
            total_customers = len(st.session_state.data)
            filtered_customers = len(st.session_state.filtered_data)
            
            if filtered_customers < total_customers:
                st.info(f"📊 Mostrando {filtered_customers} de {total_customers} clientes ({filtered_customers/total_customers*100:.1f}%) - Filtros aplicados")
            
            # Enhanced summary statistics
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Total Filtrado", filtered_customers, 
                         delta=f"{filtered_customers - total_customers}" if filtered_customers != total_customers else None)
            
            with col2:
                avg_age = st.session_state.filtered_data['age'].mean()
                overall_avg_age = st.session_state.data['age'].mean()
                age_delta = avg_age - overall_avg_age
                st.metric("Edad Promedio", f"{avg_age:.1f}", 
                         delta=f"{age_delta:+.1f}" if abs(age_delta) > 0.1 else None)
            
            with col3:
                avg_credit = st.session_state.filtered_data['credit_score'].mean()
                overall_avg_credit = st.session_state.data['credit_score'].mean()
                credit_delta = avg_credit - overall_avg_credit
                st.metric("Puntaje Crediticio", f"{avg_credit:.0f}", 
                         delta=f"{credit_delta:+.0f}" if abs(credit_delta) > 1 else None)
            
            with col4:
                app_users = (st.session_state.filtered_data['app_downloaded'] == 1).sum()
                app_percentage = (app_users / filtered_customers * 100) if filtered_customers > 0 else 0
                st.metric("Usuarios de App", f"{app_users} ({app_percentage:.1f}%)")
            
            with col5:
                high_activity = (st.session_state.filtered_data['purchases'] > 20).sum()
                activity_percentage = (high_activity / filtered_customers * 100) if filtered_customers > 0 else 0
                st.metric("Alta Actividad", f"{high_activity} ({activity_percentage:.1f}%)")
            
            # Additional insights row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                cc_taken = (st.session_state.filtered_data['cc_taken'] == 1).sum()
                cc_percentage = (cc_taken / filtered_customers * 100) if filtered_customers > 0 else 0
                st.metric("Con Tarjeta Crédito", f"{cc_taken} ({cc_percentage:.1f}%)")
            
            with col2:
                loan_received = (st.session_state.filtered_data['received_loan'] == 1).sum()
                loan_percentage = (loan_received / filtered_customers * 100) if filtered_customers > 0 else 0
                st.metric("Préstamos Recibidos", f"{loan_received} ({loan_percentage:.1f}%)")
            
            with col3:
                inactive_users = ((st.session_state.filtered_data['left_for_one_month'] == 1) | 
                                (st.session_state.filtered_data['left_for_two_month_plus'] == 1)).sum()
                inactive_percentage = (inactive_users / filtered_customers * 100) if filtered_customers > 0 else 0
                st.metric("Usuarios Inactivos", f"{inactive_users} ({inactive_percentage:.1f}%)")
            
            with col4:
                referred_users = (st.session_state.filtered_data['is_referred'] == 1).sum()
                referred_percentage = (referred_users / filtered_customers * 100) if filtered_customers > 0 else 0
                st.metric("Usuarios Referidos", f"{referred_users} ({referred_percentage:.1f}%)")
            
            st.markdown("---")
            
            # Quick filters above the table
            st.subheader("🔍 Filtros Rápidos")
            
            quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
            
            with quick_col1:
                if st.button("📱 Solo Usuarios de App"):
                    # Apply quick filter for app users
                    st.session_state.filtered_data = st.session_state.filtered_data[
                        st.session_state.filtered_data['app_downloaded'] == 1
                    ]
                    st.rerun()
            
            with quick_col2:
                if st.button("💳 Solo con Tarjeta Crédito"):
                    # Apply quick filter for credit card users
                    st.session_state.filtered_data = st.session_state.filtered_data[
                        st.session_state.filtered_data['cc_taken'] == 1
                    ]
                    st.rerun()
            
            with quick_col3:
                if st.button("⭐ Alta Actividad"):
                    # Apply quick filter for high activity users
                    st.session_state.filtered_data = st.session_state.filtered_data[
                        st.session_state.filtered_data['purchases'] > 20
                    ]
                    st.rerun()
            
            with quick_col4:
                if st.button("⚠️ Usuarios Inactivos"):
                    # Apply quick filter for inactive users
                    st.session_state.filtered_data = st.session_state.filtered_data[
                        (st.session_state.filtered_data['left_for_one_month'] == 1) |
                        (st.session_state.filtered_data['left_for_two_month_plus'] == 1)
                    ]
                    st.rerun()
            
            st.markdown("---")
            
            # Interactive data table with AgGrid
            st.subheader("📋 Tabla de Clientes")
            
            # Configure grid options
            gb = GridOptionsBuilder.from_dataframe(st.session_state.filtered_data)
            gb.configure_pagination(paginationAutoPageSize=True)
            gb.configure_side_bar()
            gb.configure_selection('single', use_checkbox=True, groupSelectsChildren="Group checkbox select children")
            gb.configure_grid_options(suppressRowClickSelection=False, rowSelection='single')
            gridOptions = gb.build()
            
            # Display the grid with unique key to force updates
            grid_response = AgGrid(
                st.session_state.filtered_data,
                gridOptions=gridOptions,
                data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                fit_columns_on_grid_load=False,
                theme='streamlit',
                enable_enterprise_modules=False,
                height=400,
                width='100%',
                reload_data=True,
                key=f"customer_grid_{len(st.session_state.filtered_data)}"
            )
            
            # Handle row selection
            selected_rows = grid_response.get('selected_rows', [])
            
            # Check if selected_rows is a DataFrame or list
            if isinstance(selected_rows, pd.DataFrame):
                has_selection = not selected_rows.empty
                selected_data = selected_rows.iloc[0].to_dict() if has_selection else None
            elif isinstance(selected_rows, list):
                has_selection = len(selected_rows) > 0
                selected_data = selected_rows[0] if has_selection else None
            else:
                has_selection = False
                selected_data = None
            
            if has_selection and selected_data:
                # Store in session state with proper data conversion
                if isinstance(selected_data, dict):
                    # Convert pandas/numpy types to native Python types
                    clean_customer = {}
                    for key, value in selected_data.items():
                        if pd.isna(value):
                            clean_customer[key] = None
                        elif isinstance(value, (np.integer, np.floating)):
                            clean_customer[key] = value.item()
                        elif isinstance(value, np.bool_):
                            clean_customer[key] = bool(value)
                        else:
                            clean_customer[key] = value
                    
                    # Check if this is a different customer than currently selected
                    current_customer = st.session_state.selected_customer
                    is_different_customer = (
                        current_customer is None or 
                        clean_customer.get('Name') != current_customer.get('Name') or
                        clean_customer.get('Surname') != current_customer.get('Surname') or
                        clean_customer.get('email') != current_customer.get('email')
                    )
                    
                    if is_different_customer:
                        # Clear previous prediction results when selecting a new customer
                        st.session_state.prediction_result = None
                        st.session_state.llm_insights = ""
                        if 'shap_plot' in st.session_state:
                            del st.session_state.shap_plot
                        st.session_state.selection_counter += 1
                    
                    st.session_state.selected_customer = clean_customer
                    
                    # Display selection confirmation
                    name = clean_customer.get('Name', 'Unknown')
                    surname = clean_customer.get('Surname', 'Customer')
                    
                    # Handle None/NaN values
                    if pd.isna(name) or name is None:
                        name = 'Unknown'
                    if pd.isna(surname) or surname is None:
                        surname = 'Customer'
                    
                    st.success(f"✅ Seleccionado: {name} {surname}")
                    
                    # Show selection details in an expander
                    with st.expander("👤 Detalles del Cliente Seleccionado", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Nombre:** {name} {surname}")
                            st.write(f"**Edad:** {clean_customer.get('age', 'N/A')}")
                            st.write(f"**Puntaje Crediticio:** {clean_customer.get('credit_score', 'N/A')}")
                            st.write(f"**Vivienda:** {clean_customer.get('housing', 'N/A')}")
                        with col2:
                            st.write(f"**Email:** {clean_customer.get('email', 'N/A')}")
                            st.write(f"**Teléfono:** {clean_customer.get('phone', 'N/A')}")
                            st.write(f"**App Descargada:** {'Sí' if clean_customer.get('app_downloaded') else 'No'}")
                            st.write(f"**Compras:** {clean_customer.get('purchases', 'N/A')}")
                else:
                    st.error("❌ Formato de datos de cliente inválido")
                    st.session_state.selected_customer = None
            else:
                # No selection - only clear if we had a previous selection
                if st.session_state.selected_customer is not None:
                    st.info("ℹ️ Ningún cliente seleccionado. Haz clic en una fila para seleccionar un cliente.")
            
            # Show current selection status and controls
            if st.session_state.selected_customer is not None:
                customer = st.session_state.selected_customer
                name = customer.get('Name', 'Unknown')
                surname = customer.get('Surname', 'Customer')
                
                # Handle None/NaN values
                if pd.isna(name) or name is None:
                    name = 'Unknown'
                if pd.isna(surname) or surname is None:
                    surname = 'Customer'
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.info(f"🎯 Actualmente seleccionado: **{name} {surname}** - Disponible en las pestañas de Predicciones e Insights")
                with col2:
                    if st.button("🗑️ Limpiar Selección"):
                        st.session_state.selected_customer = None
                        st.session_state.prediction_result = None
                        st.session_state.llm_insights = ""
                        if 'shap_plot' in st.session_state:
                            del st.session_state.shap_plot
                        st.rerun()
        else:
            st.warning("Ningún cliente coincide con los filtros actuales.")
    
    with tab2:
        st.header("➕ Agregar Nuevo Cliente")
        
        with st.form("add_customer_form"):
            # Personal Information Section
            st.subheader("👤 Información Personal (Opcional)")
            st.markdown("*Dejar en blanco para generar automáticamente con datos ficticios*")
            
            personal_col1, personal_col2 = st.columns(2)
            with personal_col1:
                name = st.text_input("Nombre", placeholder="Auto-generado si está vacío")
                surname = st.text_input("Apellido", placeholder="Auto-generado si está vacío")
                email = st.text_input("Email", placeholder="Auto-generado si está vacío")
            with personal_col2:
                phone = st.text_input("Teléfono", placeholder="Auto-generado si está vacío")
                address = st.text_area("Dirección", placeholder="Auto-generado si está vacío", height=100)
            
            st.markdown("---")
            
            # Financial and Behavioral Data
            st.subheader("📊 Datos del Cliente")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Demografía y Finanzas**")
                age = st.number_input("Edad", min_value=18, max_value=100, value=30)
                housing = st.selectbox("Vivienda", ["o", "r", "na"], format_func=lambda x: {"o": "Propia", "r": "Alquilada", "na": "No disponible"}[x], key="add_customer_housing")
                credit_score = st.number_input("Puntaje Crediticio", min_value=300, max_value=850, value=650)
                payment_type = st.selectbox("Tipo de Pago", ["monthly", "bi-weekly", "weekly", "semi-monthly", "na"], format_func=lambda x: {"monthly": "Mensual", "bi-weekly": "Quincenal", "weekly": "Semanal", "semi-monthly": "Bimensual", "na": "No disponible"}[x], key="add_customer_payment_type")
                zodiac_sign = st.selectbox("Signo Zodiacal", ["aries", "taurus", "gemini", "cancer", "leo", "virgo", 
                                                         "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"], key="add_customer_zodiac")
                
                st.markdown("**Actividad Bancaria**")
                deposits = st.number_input("Depósitos", min_value=0, value=5)
                withdrawal = st.number_input("Retiros", min_value=0, value=3)
                purchases_partners = st.number_input("Compras con Socios", min_value=0, value=10)
                purchases = st.number_input("Compras Totales", min_value=0, value=25)
            
            with col2:
                st.markdown("**Actividad de Tarjeta de Crédito**")
                cc_taken = st.selectbox("Tarjeta de Crédito Tomada", [0, 1], key="add_customer_cc_taken")
                cc_recommended = st.selectbox("TC Recomendada", [0, 1], key="add_customer_cc_recommended")
                cc_disliked = st.selectbox("TC No Gustó", [0, 1], key="add_customer_cc_disliked")
                cc_liked = st.selectbox("TC Gustó", [0, 1], key="add_customer_cc_liked")
                cc_application_begin = st.selectbox("Aplicación TC Iniciada", [0, 1], key="add_customer_cc_application")
                
                st.markdown("**Compromiso Digital**")
                app_downloaded = st.selectbox("App Descargada", [0, 1], key="add_customer_app_downloaded")
                web_user = st.selectbox("Usuario Web", [0, 1], key="add_customer_web_user")
                app_web_user = st.selectbox("Usuario App y Web", [0, 1], key="add_customer_app_web_user")
                ios_user = st.selectbox("Usuario iOS", [0, 1], key="add_customer_ios_user")
                android_user = st.selectbox("Usuario Android", [0, 1], key="add_customer_android_user")
                registered_phones = st.number_input("Teléfonos Registrados", min_value=0, value=1)
            
            with col3:
                st.markdown("**Actividad de Préstamos**")
                waiting_4_loan = st.selectbox("Esperando Préstamo", [0, 1], key="add_customer_waiting_loan")
                cancelled_loan = st.selectbox("Préstamo Cancelado", [0, 1], key="add_customer_cancelled_loan")
                received_loan = st.selectbox("Préstamo Recibido", [0, 1], key="add_customer_received_loan")
                rejected_loan = st.selectbox("Préstamo Rechazado", [0, 1], key="add_customer_rejected_loan")
                
                st.markdown("**Patrones de Comportamiento**")
                left_for_two_month_plus = st.selectbox("Inactivo 2+ Meses", [0, 1], key="add_customer_left_2months")
                left_for_one_month = st.selectbox("Inactivo 1 Mes", [0, 1], key="add_customer_left_1month")
                
                st.markdown("**Recompensas y Referencias**")
                rewards_earned = st.number_input("Recompensas Ganadas", min_value=0, value=100)
                reward_rate = st.number_input("Tasa de Recompensa", min_value=0.0, max_value=1.0, value=0.02, step=0.01)
                is_referred = st.selectbox("Es Referido", [0, 1], key="add_customer_is_referred")
            
            submitted = st.form_submit_button("➕ Agregar Cliente", type="primary")
            
            if submitted:
                try:
                    # Use provided personal info or generate fake data
                    customer_name = name.strip() if name.strip() else fake.first_name()
                    customer_surname = surname.strip() if surname.strip() else fake.last_name()
                    customer_email = email.strip() if email.strip() else fake.email()
                    customer_phone = phone.strip() if phone.strip() else fake.phone_number()
                    customer_address = address.strip() if address.strip() else fake.address().replace('\n', ', ')
                    
                    new_customer = {
                        "age": age, "housing": housing, "credit_score": credit_score,
                        "deposits": deposits, "withdrawal": withdrawal, "purchases_partners": purchases_partners,
                        "purchases": purchases, "cc_taken": cc_taken, "cc_recommended": cc_recommended,
                        "cc_disliked": cc_disliked, "cc_liked": cc_liked, "cc_application_begin": cc_application_begin,
                        "app_downloaded": app_downloaded, "web_user": web_user, "app_web_user": app_web_user,
                        "ios_user": ios_user, "android_user": android_user, "registered_phones": registered_phones,
                        "payment_type": payment_type, "waiting_4_loan": waiting_4_loan, "cancelled_loan": cancelled_loan,
                        "received_loan": received_loan, "rejected_loan": rejected_loan, "zodiac_sign": zodiac_sign,
                        "left_for_two_month_plus": left_for_two_month_plus, "left_for_one_month": left_for_one_month,
                        "rewards_earned": rewards_earned, "reward_rate": reward_rate, "is_referred": is_referred,
                        "Name": customer_name, "Surname": customer_surname, "email": customer_email,
                        "phone": customer_phone, "address": customer_address
                    }
                    
                    # Add to dataframe
                    new_df = pd.DataFrame([new_customer])
                    st.session_state.data = pd.concat([st.session_state.data, new_df], ignore_index=True)
                    
                    # Reapply filters
                    if 'age_range' in locals() and 'credit_range' in locals() and 'housing_filter' in locals():
                        st.session_state.filtered_data = apply_filters(st.session_state.data, age_range, credit_range, housing_filter)
                    else:
                        st.session_state.filtered_data = st.session_state.data.copy()
                    
                    # Show success message with personal info status
                    personal_info_status = "con información proporcionada" if name.strip() or surname.strip() else "con información auto-generada"
                    st.success(f"✅ Nuevo cliente agregado: {customer_name} {customer_surname} ({personal_info_status})")
                    
                except Exception as e:
                    st.error(f"❌ Error agregando cliente: {str(e)}")
    
    with tab3:
        st.header("📈 Dashboard Power BI")
        
        # Power BI Dashboard Section
        st.markdown("""
        ### 📊 Dashboard Interactivo de Análisis de Clientes
        
        Este dashboard de Power BI proporciona visualizaciones avanzadas y análisis en tiempo real 
        de los datos de clientes y métricas de abandono.
        """)
        
        # File upload for Power BI file
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Option to upload a .pbix file or provide a Power BI embed URL
            dashboard_option = st.radio(
                "Selecciona el tipo de dashboard:",
                ["URL de Power BI Embed", "Archivo .pbix Local"]
            )
            
            if dashboard_option == "URL de Power BI Embed":
                # Power BI Embed URL input
                powerbi_url = st.text_input(
                    "URL de Embed de Power BI:",
                    placeholder="https://app.powerbi.com/reportEmbed?reportId=...",
                    help="Pega aquí la URL de embed de tu reporte de Power BI"
                )
                
                if powerbi_url:
                    if powerbi_url.startswith("https://app.powerbi.com/"):
                        # Display the Power BI dashboard in an iframe
                        st.markdown("### 📊 Dashboard Power BI")
                        
                        # Create iframe HTML
                        iframe_html = f"""
                        <iframe 
                            title="Power BI Dashboard" 
                            width="100%" 
                            height="600" 
                            src="{powerbi_url}" 
                            frameborder="0" 
                            allowFullScreen="true">
                        </iframe>
                        """
                        
                        # Display the iframe
                        st.components.v1.html(iframe_html, height=620)
                        
                        # Additional controls
                        st.markdown("---")
                        col_refresh, col_fullscreen = st.columns(2)
                        
                        with col_refresh:
                            if st.button("🔄 Actualizar Dashboard"):
                                st.rerun()
                        
                        with col_fullscreen:
                            st.markdown(f"[🔗 Abrir en Nueva Ventana]({powerbi_url})")
                    else:
                        st.error("❌ Por favor ingresa una URL válida de Power BI (debe comenzar con https://app.powerbi.com/)")
                else:
                    st.info("👆 Ingresa la URL de embed de tu dashboard de Power BI para visualizarlo aquí.")
            
            else:  # Local .pbix file option
                uploaded_pbix = st.file_uploader(
                    "Subir archivo .pbix",
                    type="pbix",
                    help="Sube tu archivo de Power BI (.pbix) para visualizarlo"
                )
                
                if uploaded_pbix is not None:
                    st.warning("⚠️ Los archivos .pbix no pueden ser visualizados directamente en el navegador.")
                    st.markdown("""
                    ### 📋 Opciones para archivos .pbix:
                    
                    1. **Publicar en Power BI Service:**
                       - Abre el archivo en Power BI Desktop
                       - Publica el reporte en Power BI Service
                       - Obtén la URL de embed y úsala en la opción anterior
                    
                    2. **Descargar archivo:**
                       - Puedes descargar el archivo subido para abrirlo en Power BI Desktop
                    """)
                    
                    # Option to download the uploaded file
                    st.download_button(
                        label="📥 Descargar archivo .pbix",
                        data=uploaded_pbix.getvalue(),
                        file_name=uploaded_pbix.name,
                        mime="application/octet-stream"
                    )
                else:
                    st.info("👆 Sube un archivo .pbix para más opciones.")
        
        with col2:
            st.markdown("### 💡 Consejos")
            st.markdown("""
            **Para obtener la URL de embed:**
            
            1. Abre tu reporte en Power BI Service
            2. Ve a **Archivo** → **Insertar reporte**
            3. Copia la URL del iframe
            4. Pégala en el campo de arriba
            
            **Permisos necesarios:**
            - El reporte debe ser público o compartido
            - Tu organización debe permitir embeds
            """)
            
            # Sample dashboard option
            st.markdown("---")
            st.markdown("### 🎯 Dashboard de Ejemplo")
            
            if st.button("📊 Mostrar Dashboard de Ejemplo"):
                # Create a sample dashboard using Plotly
                st.markdown("### 📈 Dashboard de Ejemplo - Análisis de Abandono")
                
                if not st.session_state.data.empty:
                    # Create sample visualizations
                    data = st.session_state.filtered_data
                    
                    # Age distribution
                    fig_age = px.histogram(data, x='age', title='Distribución por Edad', 
                                         color_discrete_sequence=['#1f77b4'])
                    st.plotly_chart(fig_age, use_container_width=True)
                    
                    # Credit score vs purchases
                    fig_scatter = px.scatter(data, x='credit_score', y='purchases', 
                                           title='Puntaje Crediticio vs Compras',
                                           color='housing')
                    st.plotly_chart(fig_scatter, use_container_width=True)
                    
                    # Housing type distribution
                    housing_counts = data['housing'].value_counts()
                    fig_pie = px.pie(values=housing_counts.values, names=housing_counts.index,
                                   title='Distribución por Tipo de Vivienda')
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.warning("⚠️ No hay datos disponibles para el dashboard de ejemplo.")
    
    with tab4:
        st.header("🤖 Predicción de Abandono")
        
        if st.session_state.selected_customer is not None:
            customer = st.session_state.selected_customer
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("👤 Cliente Seleccionado")
                
                # Safely extract customer information
                name = customer.get('Name', 'Unknown')
                surname = customer.get('Surname', 'Customer')
                age = customer.get('age', 'N/A')
                credit_score = customer.get('credit_score', 0)
                housing = customer.get('housing', 'N/A')
                email = customer.get('email', 'N/A')
                
                # Handle None/NaN values
                if pd.isna(name) or name is None:
                    name = 'Unknown'
                if pd.isna(surname) or surname is None:
                    surname = 'Customer'
                if pd.isna(email) or email is None:
                    email = 'N/A'
                if pd.isna(housing) or housing is None:
                    housing = 'N/A'
                
                st.write(f"**Nombre:** {name} {surname}")
                st.write(f"**Edad:** {age}")
                
                # Handle credit score display
                try:
                    if pd.isna(credit_score) or credit_score is None:
                        st.write("**Puntaje Crediticio:** N/A")
                    else:
                        st.write(f"**Puntaje Crediticio:** {float(credit_score):.0f}")
                except (ValueError, TypeError):
                    st.write(f"**Puntaje Crediticio:** {credit_score}")
                
                st.write(f"**Vivienda:** {get_display_value('housing', housing)}")
                st.write(f"**Email:** {email}")
                
                # Additional customer metrics
                st.markdown("---")
                st.markdown("**Métricas Clave:**")
                deposits = customer.get('deposits', 0)
                purchases = customer.get('purchases', 0)
                app_downloaded = customer.get('app_downloaded', 0)
                
                st.write(f"• Depósitos: {deposits}")
                st.write(f"• Compras: {purchases}")
                st.write(f"• Usuario de App: {'Sí' if app_downloaded else 'No'}")
                
                # Customer profile chart
                try:
                    fig = create_customer_summary_chart(customer)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as chart_error:
                    st.warning(f"No se pudo generar el gráfico del cliente: {str(chart_error)}")
            
            with col2:
                st.subheader("🔮 Predicción")
                
                # Prediction button
                if st.button("🚀 Predecir Abandono", type="primary"):
                    with st.spinner("Realizando predicción..."):
                        result, error = predict_churn(customer)
                        
                        if result:
                            st.session_state.prediction_result = result
                            st.success("✅ Predicción completada exitosamente!")
                        else:
                            st.error(f"❌ {error}")
                            st.session_state.prediction_result = None
                
                # Display prediction results persistently (outside button handler)
                if st.session_state.prediction_result is not None:
                    result = st.session_state.prediction_result
                    
                    # Extract results from API response (using XGB model as primary)
                    prob = result.get('churn_probability_XGB', result.get('churn_probability', 0))
                    risk = result.get('risk_level_XGB', result.get('risk_level', 'Unknown'))
                    prediction = result.get('churn_prediction_XGB', result.get('churn_prediction', False))
                    
                    # Also get RF results for comparison
                    prob_rf = result.get('churn_probability_RF', 0)
                    risk_rf = result.get('risk_level_RF', 'Unknown')
                    
                    # Color coding based on risk
                    if risk == "High":
                        color = "🔴"
                    elif risk == "Medium":
                        color = "🟡"
                    else:
                        color = "🟢"
                    
                    st.markdown("---")
                    st.markdown(f"""
                    ### {color} Resultados de Predicción (Modelo XGBoost)
                    
                    **Probabilidad de Abandono:** {prob:.2%}
                    
                    **Nivel de Riesgo:** {risk}
                    
                    **Predicción:** {'Abandonará' if prediction else 'Se Quedará'}
                    """)
                    
                    # Progress bar for probability
                    st.progress(prob)
                    
                    # Show comparison with Random Forest
                    with st.expander("📊 Comparación de Modelos", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Modelo XGBoost**")
                            st.write(f"Probabilidad: {prob:.2%}")
                            st.write(f"Riesgo: {risk}")
                        with col2:
                            st.markdown("**Modelo Random Forest**")
                            st.write(f"Probabilidad: {prob_rf:.2%}")
                            st.write(f"Riesgo: {risk_rf}")
                    
                    # Show raw JSON response
                    with st.expander("🔍 Respuesta Cruda de la API", expanded=False):
                        st.text_area(
                            "Respuesta JSON:",
                            value=json.dumps(result, indent=2),
                            height=300,
                            help="Respuesta cruda de la API de predicción de abandono"
                        )
                    
                    # SHAP Plot Generation
                    st.markdown("---")
                    st.subheader("📊 Explicación SHAP")
                    
                    col_shap1, col_shap2 = st.columns([3, 1])
                    
                    with col_shap1:
                        if st.button("📊 Generar Gráfico SHAP"):
                            with st.spinner("Generando explicación SHAP..."):
                                fig, error = generate_shap_plot(customer)
                                
                                if fig:
                                    st.session_state.shap_plot = fig
                                    st.success("✅ Gráfico SHAP generado exitosamente!")
                                else:
                                    st.error(f"❌ {error}")
                                    if 'shap_plot' in st.session_state:
                                        del st.session_state.shap_plot
                    
                    with col_shap2:
                        if st.button("🗑️ Limpiar Gráfico SHAP"):
                            if 'shap_plot' in st.session_state:
                                del st.session_state.shap_plot
                                st.success("✅ Gráfico SHAP eliminado")
                    
                    # Display SHAP plot persistently if it exists
                    if 'shap_plot' in st.session_state:
                        st.pyplot(st.session_state.shap_plot)
                        st.markdown("💡 **Interpretación:** Las barras rojas aumentan el riesgo de abandono, las azules lo disminuyen.")
                
                else:
                    st.info("👆 Haz clic en 'Predecir Abandono' para obtener resultados de predicción.")
                
                # Option to clear prediction results
                if st.session_state.prediction_result is not None:
                    st.markdown("---")
                    if st.button("🗑️ Limpiar Resultados de Predicción"):
                        st.session_state.prediction_result = None
                        if 'shap_plot' in st.session_state:
                            del st.session_state.shap_plot
                        st.success("✅ Resultados de predicción eliminados")
                        st.rerun()
        else:
            st.info("👆 Por favor selecciona un cliente de la pestaña **Datos de Clientes** primero.")
            st.markdown("### Cómo seleccionar un cliente:")
            st.markdown("1. Ve a la pestaña **Datos de Clientes**")
            st.markdown("2. Haz clic en cualquier fila de la tabla de clientes")
            st.markdown("3. Regresa a esta pestaña para hacer predicciones")
            
            if not st.session_state.data.empty:
                st.markdown("---")
                st.markdown(f"**Clientes disponibles:** {len(st.session_state.filtered_data)}")
            else:
                st.warning("⚠️ No hay datos de clientes cargados. Por favor carga datos de muestra o sube un archivo CSV primero.")
    
    with tab5:
        st.header("💡 Insights de Cliente Impulsados por IA")
        
        # Check if we have both customer selection and prediction
        if st.session_state.selected_customer is not None:
            customer = st.session_state.selected_customer
            
            # Safely extract customer name
            name = customer.get('Name', 'Desconocido')
            surname = customer.get('Surname', 'Cliente')
            
            # Handle None/NaN values
            if pd.isna(name) or name is None:
                name = 'Desconocido'
            if pd.isna(surname) or surname is None:
                surname = 'Cliente'
            
            customer_name = f"{name} {surname}"
            st.subheader(f"🎯 Insights para {customer_name}")
            
            # Show customer summary
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Resumen del Cliente:**")
                st.write(f"• Edad: {customer.get('age', 'N/A')}")
                st.write(f"• Vivienda: {customer.get('housing', 'N/A')}")
                st.write(f"• Puntaje Crediticio: {customer.get('credit_score', 'N/A')}")
            with col2:
                st.markdown("**Nivel de Actividad:**")
                st.write(f"• Depósitos: {customer.get('deposits', 0)}")
                st.write(f"• Compras: {customer.get('purchases', 0)}")
                st.write(f"• Usuario de App: {'Sí' if customer.get('app_downloaded') else 'No'}")
            
            # Check if prediction has been made
            if st.session_state.prediction_result is not None:
                st.markdown("---")
                
                # Show prediction summary (using XGBoost results as primary)
                prob = st.session_state.prediction_result.get('churn_probability_XGB', 
                       st.session_state.prediction_result.get('churn_probability', 0))
                risk = st.session_state.prediction_result.get('risk_level_XGB', 
                       st.session_state.prediction_result.get('risk_level', 'Unknown'))
                
                st.markdown(f"**Predicción Actual:** Riesgo {risk} ({prob:.1%} probabilidad de abandono)")
            else:
                st.info("💡 Ejecuta una predicción de abandono primero para obtener insights personalizados.")
                st.markdown("---")
            
            # Insights generation options
            st.markdown("### 🤖 Opciones de Generación de Insights")
            
            # Check API health first
            api_health = check_llm_api_health()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🔧 Análisis Basado en Reglas**")
                st.markdown("• Rápido y confiable")
                st.markdown("• Basado en patrones establecidos")
                st.markdown("• Siempre disponible")
                
                if st.button("📊 Generar Insights (Reglas)", type="secondary"):
                    with st.spinner("Generando insights basados en reglas..."):
                        insights, error = get_llm_insights(customer, st.session_state.prediction_result, use_transformers=False)
                        
                        if insights:
                            st.session_state.llm_insights = insights
                            st.session_state.insights_method = "Reglas"
                            st.success("✅ Insights generados usando análisis basado en reglas")
                        else:
                            st.error(f"❌ {error}")
            
            with col2:
                st.markdown("**🧠 IA con Transformers**")
                st.markdown("• Análisis más sofisticado")
                st.markdown("• Respuestas más naturales")
                st.markdown(f"• Estado: {'🟢 Disponible' if api_health.get('transformers_available') else '🔴 No disponible'}")
                
                transformers_disabled = not api_health.get('transformers_available', False)
                
                if st.button("🤖 Generar Insights (IA)", type="primary", disabled=transformers_disabled):
                    with st.spinner("Generando insights con IA (esto puede tomar unos momentos)..."):
                        insights, error = get_llm_insights(customer, st.session_state.prediction_result, use_transformers=True)
                        
                        if insights:
                            st.session_state.llm_insights = insights
                            st.session_state.insights_method = "Transformers IA"
                            st.success("✅ Insights generados usando IA con Transformers")
                        else:
                            st.error(f"❌ {error}")
                            # Show fallback option
                            st.info("💡 Prueba el análisis basado en reglas como alternativa")
            
            # Show API status
            if not api_health.get('status') == 'saludable':
                st.warning("⚠️ La API LLM no está disponible. Solo se pueden generar insights básicos.")
            
            # Display generated insights
            if st.session_state.llm_insights:
                method_used = getattr(st.session_state, 'insights_method', 'Desconocido')
                
                st.markdown("---")
                st.markdown(f"### 📋 Estrategia de Retención (Método: {method_used})")
                st.markdown(st.session_state.llm_insights)
                
                # Additional visualization (using XGBoost results)
                if st.session_state.prediction_result:
                    risk_level = st.session_state.prediction_result.get('risk_level_XGB', 
                               st.session_state.prediction_result.get('risk_level', 'Unknown'))
                    prob = st.session_state.prediction_result.get('churn_probability_XGB', 
                           st.session_state.prediction_result.get('churn_probability', 0))
                    
                    # Risk gauge
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = prob * 100,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Riesgo de Abandono %"},
                        delta = {'reference': 50},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 30], 'color': "lightgreen"},
                                {'range': [30, 70], 'color': "yellow"},
                                {'range': [70, 100], 'color': "red"}],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 90}}))
                    
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Option to clear insights
                if st.button("🗑️ Limpiar Insights"):
                    st.session_state.llm_insights = ""
                    if hasattr(st.session_state, 'insights_method'):
                        delattr(st.session_state, 'insights_method')
                    st.rerun()
            
            # Display existing insights if available
            if st.session_state.llm_insights:
                st.markdown("### 📝 Insights Anteriores")
                st.markdown(st.session_state.llm_insights)
                
        elif st.session_state.selected_customer is None:
            st.info("👆 Por favor selecciona un cliente de la pestaña **Datos de Clientes** primero.")
            st.markdown("### Cómo obtener insights:")
            st.markdown("1. Ve a la pestaña **Datos de Clientes**")
            st.markdown("2. Haz clic en cualquier fila de la tabla de clientes")
            st.markdown("3. Ve a la pestaña **Predicciones** y ejecuta una predicción")
            st.markdown("4. Regresa aquí para generar insights de IA")
        else:
            st.info("🤖 Por favor ejecuta una predicción de abandono primero para generar insights.")
            st.markdown("Ve a la pestaña **Predicciones** y haz clic en **Predecir Abandono** para comenzar.")
    
    with tab6:
        st.header("📊 Análisis Masivo de Clientes")
        
        if st.session_state.data.empty:
            st.info("👆 Por favor carga datos de clientes primero desde la pestaña **Datos de Clientes**.")
            return
        
        # Show current filter status
        total_customers = len(st.session_state.data)
        filtered_customers = len(st.session_state.filtered_data)
        
        st.markdown(f"""
        ### 🎯 Análisis Masivo de Predicciones e Insights
        
        Esta herramienta procesará **{filtered_customers} clientes** (de {total_customers} total) 
        aplicando los filtros actuales de la pestaña **Datos de Clientes**.
        
        **Proceso:**
        1. 🤖 Ejecutar predicciones de abandono para todos los clientes filtrados
        2. 🧠 Generar insights de retención personalizados (opcional)
        3. 📊 Mostrar resultados en tabla interactiva
        4. 💾 Exportar resultados completos a CSV
        """)
        
        if filtered_customers == 0:
            st.warning("⚠️ No hay clientes en el conjunto filtrado. Ajusta los filtros en la pestaña **Datos de Clientes**.")
            return
        
        # Batch processing options
        st.markdown("---")
        st.subheader("⚙️ Opciones de Procesamiento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            include_predictions = st.checkbox("🤖 Incluir Predicciones de Abandono", value=True)
            if include_predictions:
                st.markdown("• Probabilidad de abandono")
                st.markdown("• Nivel de riesgo")
                st.markdown("• Predicción binaria")
        
        with col2:
            include_insights = st.checkbox("🧠 Incluir Insights de IA", value=False)
            if include_insights:
                use_transformers_batch = st.checkbox("🤖 Usar Transformers (más lento)", value=False)
                st.markdown("• Recomendaciones personalizadas")
                st.markdown("• Estrategias de retención")
                st.markdown("• Acciones sugeridas")
        
        # Processing controls
        st.markdown("---")
        st.subheader("🚀 Ejecutar Análisis Masivo")
        
        # Estimate processing time
        estimated_time_predictions = filtered_customers * 0.5  # ~0.5 seconds per prediction
        estimated_time_insights = filtered_customers * 2 if include_insights else 0  # ~2 seconds per insight
        total_estimated_time = estimated_time_predictions + estimated_time_insights
        
        st.info(f"⏱️ Tiempo estimado: {total_estimated_time:.0f} segundos para {filtered_customers} clientes")
        
        # Batch processing button
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("🚀 Iniciar Análisis Masivo", type="primary", disabled=not (include_predictions or include_insights)):
                # Initialize batch results in session state
                if 'batch_results' not in st.session_state:
                    st.session_state.batch_results = None
                
                # Run batch processing
                batch_results = run_batch_analysis(
                    st.session_state.filtered_data,
                    include_predictions=include_predictions,
                    include_insights=include_insights,
                    use_transformers=use_transformers_batch if include_insights else False
                )
                
                if batch_results is not None:
                    st.session_state.batch_results = batch_results
                    st.success(f"✅ Análisis completado para {len(batch_results)} clientes!")
                else:
                    st.error("❌ Error en el análisis masivo. Verifica que las APIs estén ejecutándose.")
        
        with col2:
            if st.button("🗑️ Limpiar Resultados"):
                if 'batch_results' in st.session_state:
                    del st.session_state.batch_results
                st.success("✅ Resultados eliminados")
                st.rerun()
        
        with col3:
            if st.session_state.get('batch_results') is not None:
                # CSV export button
                csv_data = prepare_batch_results_for_export(st.session_state.batch_results)
                st.download_button(
                    label="📥 Exportar CSV",
                    data=csv_data,
                    file_name=f"analisis_masivo_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        # Display batch results
        if st.session_state.get('batch_results') is not None:
            display_batch_results(st.session_state.batch_results, include_predictions, include_insights)
    
    with tab7:
        st.header("📧 Campaña de Email Marketing Personalizada")
        
        if st.session_state.data.empty:
            st.info("👆 Por favor carga datos de clientes primero desde la pestaña **Datos de Clientes**.")
            return
        
        # Show current filter status
        total_customers = len(st.session_state.data)
        filtered_customers = len(st.session_state.filtered_data)
        
        st.markdown(f"""
        ### 🎯 Campaña de Marketing Basada en Análisis de Abandono
        
        Crea campañas de email personalizadas para **{filtered_customers} clientes** (de {total_customers} total) 
        usando los filtros y análisis de la pestaña **Datos de Clientes**.
        
        **Características:**
        - 📊 Segmentación automática por nivel de riesgo
        - 🎨 Contenido personalizado basado en perfil del cliente
        - 📈 Métricas de campaña estimadas
        - 📧 Plantillas HTML listas para usar
        - 📋 Exportación para plataformas de email marketing
        """)
        
        if filtered_customers == 0:
            st.warning("⚠️ No hay clientes en el conjunto filtrado. Ajusta los filtros en la pestaña **Datos de Clientes**.")
            return
        
        # Campaign configuration
        st.markdown("---")
        st.subheader("⚙️ Configuración de Campaña")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            campaign_type = st.selectbox(
                "🎯 Tipo de Campaña",
                ["retention", "engagement", "loyalty"],
                format_func=lambda x: {
                    "retention": "🚨 Retención (Alto Riesgo)",
                    "engagement": "💡 Engagement (Riesgo Medio)", 
                    "loyalty": "🏆 Fidelización (Bajo Riesgo)"
                }[x],
                key="email_campaign_type"
            )
        
        with col2:
            personalization_level = st.selectbox(
                "🎨 Nivel de Personalización",
                ["high", "medium", "basic"],
                format_func=lambda x: {
                    "high": "🎯 Alta (Datos completos)",
                    "medium": "📊 Media (Datos básicos)",
                    "basic": "📝 Básica (Solo nombre)"
                }[x],
                key="email_personalization_level"
            )
        
        with col3:
            include_predictions_email = st.checkbox("🤖 Usar Predicciones de Abandono", value=True)
            if include_predictions_email and st.session_state.get('batch_results') is None:
                st.warning("⚠️ Ejecuta el análisis masivo primero")
        
        # Campaign preview and generation
        st.markdown("---")
        st.subheader("👀 Vista Previa de Campaña")
        
        # Show sample customer for preview
        if not st.session_state.filtered_data.empty:
            sample_customer = st.session_state.filtered_data.iloc[0].to_dict()
            
            # Add prediction data if available
            if include_predictions_email and st.session_state.get('batch_results') is not None:
                batch_results = st.session_state.batch_results
                if not batch_results.empty:
                    sample_prediction = batch_results.iloc[0]
                    sample_customer.update({
                        'risk_level_XGB': sample_prediction.get('risk_level_XGB', 'Medium'),
                        'churn_probability_XGB': sample_prediction.get('churn_probability_XGB', 0.5)
                    })
            
            # Generate sample email
            sample_campaign = generate_email_campaign_content(
                sample_customer,
                campaign_type=campaign_type,
                personalization_level=personalization_level
            )
            
            # Display sample email info
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📧 Líneas de Asunto Sugeridas:**")
                for i, subject in enumerate(sample_campaign['subject_lines'], 1):
                    st.markdown(f"{i}. {subject}")
            
            with col2:
                st.markdown("**📊 Métricas Estimadas:**")
                metrics = sample_campaign['campaign_metrics']
                st.markdown(f"• Tasa de apertura: {metrics['expected_open_rate']}")
                st.markdown(f"• Tasa de clics: {metrics['expected_click_rate']}")
                st.markdown(f"• Mejor horario: {metrics['recommended_send_time']}")
                st.markdown(f"• Urgencia: {metrics['urgency_level'].title()}")
            
            # Show email preview
            with st.expander("📧 Vista Previa del Email", expanded=False):
                st.markdown("**Cliente de muestra:** " + sample_customer.get('Name', 'Cliente') + " " + sample_customer.get('Surname', ''))
                st.markdown("**Segmento:** " + sample_campaign['customer_segment'])
                st.markdown("---")
                st.components.v1.html(sample_campaign['email_content'], height=600, scrolling=True)
        
        # Campaign generation
        st.markdown("---")
        st.subheader("🚀 Generar Campaña Completa")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("🚀 Generar Campaña de Email", type="primary"):
                # Prepare campaign settings
                campaign_settings = {
                    'campaign_type': campaign_type,
                    'personalization_level': personalization_level,
                    'include_predictions': include_predictions_email
                }
                
                # Use filtered data with predictions if available
                campaign_data = st.session_state.filtered_data.copy()
                
                if include_predictions_email and st.session_state.get('batch_results') is not None:
                    # Merge with prediction results
                    batch_results = st.session_state.batch_results
                    # Add prediction columns to campaign data
                    for idx, row in batch_results.iterrows():
                        if idx < len(campaign_data):
                            campaign_data.loc[campaign_data.index[idx], 'risk_level_XGB'] = row.get('risk_level_XGB', 'Medium')
                            campaign_data.loc[campaign_data.index[idx], 'churn_probability_XGB'] = row.get('churn_probability_XGB', 0.5)
                
                # Generate bulk campaign
                with st.spinner("Generando campaña personalizada..."):
                    campaign_df = create_bulk_email_campaign(campaign_data, campaign_settings)
                    st.session_state.email_campaign = campaign_df
                
                st.success(f"✅ Campaña generada para {len(campaign_df)} clientes!")
        
        with col2:
            if st.button("🗑️ Limpiar Campaña"):
                if 'email_campaign' in st.session_state:
                    del st.session_state.email_campaign
                st.success("✅ Campaña eliminada")
                st.rerun()
        
        # Campaign results and export
        if st.session_state.get('email_campaign') is not None:
            campaign_df = st.session_state.email_campaign
            
            st.markdown("---")
            st.subheader("📊 Resumen de Campaña Generada")
            
            # Campaign statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Emails", len(campaign_df))
            
            with col2:
                high_risk_count = (campaign_df['risk_level'] == 'High').sum()
                st.metric("Alto Riesgo", high_risk_count)
            
            with col3:
                medium_risk_count = (campaign_df['risk_level'] == 'Medium').sum()
                st.metric("Riesgo Medio", medium_risk_count)
            
            with col4:
                low_risk_count = (campaign_df['risk_level'] == 'Low').sum()
                st.metric("Bajo Riesgo", low_risk_count)
            
            # Segmentation breakdown
            st.markdown("### 📈 Segmentación de Campaña")
            segment_counts = campaign_df['customer_segment'].value_counts()
            
            fig_segments = px.pie(
                values=segment_counts.values,
                names=segment_counts.index,
                title="Distribución por Segmento de Campaña"
            )
            st.plotly_chart(fig_segments, use_container_width=True)
            
            # Export options
            st.markdown("### 📥 Opciones de Exportación")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # CSV export
                csv_data = export_email_campaign_data(campaign_df, "csv")
                st.download_button(
                    label="📊 Exportar CSV",
                    data=csv_data,
                    file_name=f"email_campaign_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # HTML preview export
                html_preview = export_email_campaign_data(campaign_df, "html_preview")
                st.download_button(
                    label="🌐 Vista HTML",
                    data=html_preview,
                    file_name=f"email_preview_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html"
                )
            
            with col3:
                # Campaign summary
                summary_data = export_email_campaign_data(campaign_df, "summary")
                st.download_button(
                    label="📋 Resumen",
                    data=summary_data,
                    file_name=f"campaign_summary_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            
            with col4:
                # Mailchimp format (simplified CSV)
                mailchimp_df = campaign_df[['name', 'surname', 'email', 'subject_line', 'customer_segment', 'risk_level']].copy()
                mailchimp_df.columns = ['FNAME', 'LNAME', 'EMAIL', 'SUBJECT', 'SEGMENT', 'RISK_LEVEL']
                mailchimp_csv = mailchimp_df.to_csv(index=False)
                st.download_button(
                    label="📮 Formato Mailchimp",
                    data=mailchimp_csv,
                    file_name=f"mailchimp_import_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            # Campaign preview table
            st.markdown("### 📋 Vista Previa de Campaña")
            
            # Filter options for campaign preview
            col1, col2 = st.columns(2)
            
            with col1:
                risk_filter_email = st.selectbox(
                    "Filtrar por Riesgo",
                    ["Todos"] + list(campaign_df['risk_level'].unique()),
                    key="email_risk_filter"
                )
            
            with col2:
                segment_filter_email = st.selectbox(
                    "Filtrar por Segmento",
                    ["Todos"] + list(campaign_df['customer_segment'].unique()),
                    key="email_segment_filter"
                )
            
            # Apply filters
            filtered_campaign = campaign_df.copy()
            
            if risk_filter_email != "Todos":
                filtered_campaign = filtered_campaign[filtered_campaign['risk_level'] == risk_filter_email]
            
            if segment_filter_email != "Todos":
                filtered_campaign = filtered_campaign[filtered_campaign['customer_segment'] == segment_filter_email]
            
            # Display filtered campaign data
            display_columns = ['name', 'surname', 'email', 'risk_level', 'subject_line', 'customer_segment', 'expected_open_rate']
            
            if not filtered_campaign.empty:
                st.dataframe(
                    filtered_campaign[display_columns],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Show individual email preview
                st.markdown("### 👀 Vista Previa Individual")
                selected_customer_idx = st.selectbox(
                    "Seleccionar cliente para vista previa:",
                    range(len(filtered_campaign)),
                    format_func=lambda x: f"{filtered_campaign.iloc[x]['name']} {filtered_campaign.iloc[x]['surname']} ({filtered_campaign.iloc[x]['email']})",
                    key="email_customer_preview_selector"
                )
                
                if selected_customer_idx is not None:
                    selected_customer = filtered_campaign.iloc[selected_customer_idx]
                    
                    st.markdown(f"**Cliente:** {selected_customer['name']} {selected_customer['surname']}")
                    st.markdown(f"**Email:** {selected_customer['email']}")
                    st.markdown(f"**Asunto:** {selected_customer['subject_line']}")
                    st.markdown(f"**Segmento:** {selected_customer['customer_segment']}")
                    st.markdown("---")
                    
                    # Display the email content
                    st.components.v1.html(selected_customer['email_content'], height=600, scrolling=True)
            else:
                st.info("No hay clientes que coincidan con los filtros seleccionados.")
            
            # Campaign execution recommendations
            st.markdown("---")
            st.markdown("### 🎯 Recomendaciones de Ejecución")
            
            st.markdown("""
            **📅 Cronograma Sugerido:**
            1. **Clientes de Alto Riesgo**: Enviar inmediatamente (dentro de 24 horas)
            2. **Clientes de Riesgo Medio**: Enviar en 2-3 días
            3. **Clientes de Bajo Riesgo**: Enviar durante la próxima semana
            
            **📊 Monitoreo:**
            - Revisar métricas de apertura después de 48 horas
            - Preparar emails de seguimiento para no respondedores
            - Analizar tasas de clics y conversiones semanalmente
            
            **🔄 Seguimiento:**
            - Email de seguimiento automático después de 7 días para alto riesgo
            - Encuesta de satisfacción para respondedores positivos
            - Análisis de efectividad después de 30 días
            """)
        
        
    st.markdown("---")
    st.markdown("🏦 **Panel de Predicción de Abandono Fintech** | Construido con Streamlit")

if __name__ == "__main__":
    main()