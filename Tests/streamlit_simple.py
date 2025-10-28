import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from faker import Faker
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Fintech Churn Prediction Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Faker
fake = Faker()

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()
if 'selected_customer_idx' not in st.session_state:
    st.session_state.selected_customer_idx = None
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None
if 'llm_insights' not in st.session_state:
    st.session_state.llm_insights = ""

def load_sample_data():
    """Load sample data for demonstration"""
    np.random.seed(42)
    n_samples = 50
    
    sample_data = {
        "age": np.random.randint(18, 80, n_samples),
        "housing": np.random.choice(["own", "rent", "mortgage"], n_samples),
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
        "payment_type": np.random.choice(["credit_card", "debit_card", "bank_transfer"], n_samples),
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
    
    # Add personal info
    df['Name'] = [fake.first_name() for _ in range(len(df))]
    df['Surname'] = [fake.last_name() for _ in range(len(df))]
    df['email'] = [fake.email() for _ in range(len(df))]
    df['phone'] = [fake.phone_number() for _ in range(len(df))]
    df['address'] = [fake.address().replace('\n', ', ') for _ in range(len(df))]
    
    return df

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
            return None, f"API Error: {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return None, "Error: Churn prediction API is not running. Please start api.py first."
    except Exception as e:
        return None, f"Error making prediction: {str(e)}"

def get_llm_insights(customer_data, prediction_result):
    """Get LLM insights for customer retention"""
    try:
        # Prepare data for LLM API (exclude personal information)
        api_data = {k: v for k, v in customer_data.items() 
                   if k not in ['Name', 'Surname', 'email', 'phone', 'address']}
        
        # Add prediction results
        api_data.update(prediction_result)
        
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
            return None, f"LLM API Error: {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return None, "Error: LLM API is not running. Please start llm_api.py first."
    except Exception as e:
        return None, f"Error getting LLM insights: {str(e)}"

def create_customer_chart(customer_data):
    """Create a radar chart for customer profile"""
    try:
        features = {
            'Age': min(100, customer_data.get('age', 30)),
            'Credit Score': min(100, customer_data.get('credit_score', 650) / 10),
            'Deposits': min(50, customer_data.get('deposits', 5)) * 2,
            'Purchases': min(100, customer_data.get('purchases', 25)),
            'Rewards': min(100, customer_data.get('rewards_earned', 100) / 10),
            'Digital': customer_data.get('app_downloaded', 0) * 100,
        }
        
        fig = go.Figure(data=go.Scatterpolar(
            r=list(features.values()),
            theta=list(features.keys()),
            fill='toself',
            name='Customer Profile'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            title="Customer Profile",
            height=400
        )
        
        return fig
    except:
        return None

def main():
    st.title("🏦 Fintech Churn Prediction Dashboard")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("🎛️ Controls")
    
    # Data Management Section
    st.sidebar.header("� Data Managmement")
    
    # Data loading options
    data_option = st.sidebar.radio(
        "Choose data source:",
        ["Load Sample Data", "Upload CSV File"]
    )
    
    if data_option == "Load Sample Data":
        if st.sidebar.button("🔄 Load Sample Data"):
            with st.spinner("Loading sample data..."):
                st.session_state.data = load_sample_data()
            st.sidebar.success("Sample data loaded!")
    
    else:  # Upload CSV File
        uploaded_file = st.sidebar.file_uploader(
            "Choose a CSV file",
            type="csv",
            help="Upload a CSV file with customer data"
        )
        
        if uploaded_file is not None:
            try:
                with st.spinner("Loading CSV file..."):
                    # Read the CSV file
                    df = pd.read_csv(uploaded_file)
                    
                    # Check if personal info columns exist, if not add them
                    personal_columns = ['Name', 'Surname', 'email', 'phone', 'address']
                    missing_columns = [col for col in personal_columns if col not in df.columns]
                    
                    if missing_columns:
                        st.sidebar.info(f"Adding missing personal info columns: {', '.join(missing_columns)}")
                        # Add missing personal info columns
                        for i in range(len(df)):
                            if 'Name' not in df.columns:
                                df.loc[i, 'Name'] = fake.first_name()
                            if 'Surname' not in df.columns:
                                df.loc[i, 'Surname'] = fake.last_name()
                            if 'email' not in df.columns:
                                df.loc[i, 'email'] = fake.email()
                            if 'phone' not in df.columns:
                                df.loc[i, 'phone'] = fake.phone_number()
                            if 'address' not in df.columns:
                                df.loc[i, 'address'] = fake.address().replace('\n', ', ')
                    
                    st.session_state.data = df
                    
                st.sidebar.success(f"✅ CSV loaded! {len(df)} customers imported")
                
            except Exception as e:
                st.sidebar.error(f"❌ Error loading CSV: {str(e)}")
    
    # Save/Download options
    st.sidebar.markdown("---")
    st.sidebar.subheader("💾 Save & Download")
    
    # Download template CSV
    template_data = {
        'age': [30, 45, 25],
        'housing': ['own', 'rent', 'mortgage'],
        'credit_score': [650, 720, 580],
        'deposits': [5, 8, 3],
        'purchases': [25, 40, 15],
        'app_downloaded': [1, 1, 0],
        'payment_type': ['credit_card', 'debit_card', 'bank_transfer'],
        'zodiac_sign': ['leo', 'virgo', 'aries'],
        'rewards_earned': [150, 200, 50],
        'is_referred': [1, 0, 1]
    }
    
    template_csv = pd.DataFrame(template_data).to_csv(index=False)
    st.sidebar.download_button(
        label="📋 Download CSV Template",
        data=template_csv,
        file_name="customer_template.csv",
        mime="text/csv",
        help="Download a sample CSV file format"
    )
    
    # Save current data
    if not st.session_state.data.empty:
        csv_data = st.session_state.data.to_csv(index=False)
        st.sidebar.download_button(
            label="📁 Download Current Data",
            data=csv_data,
            file_name="customer_data.csv",
            mime="text/csv",
            help="Download the current customer data"
        )
    
    if st.session_state.data.empty:
        st.info("👆 Please load sample data from the sidebar to get started!")
        return
    
    # Show data info
    st.sidebar.info(f"📊 Total customers: {len(st.session_state.data)}")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Customer Data", "➕ Add Customer", "🤖 Predictions", "💡 Insights"])
    
    with tab1:
        st.header("📊 Customer Data")
        
        # Display data
        st.dataframe(st.session_state.data, use_container_width=True)
        
        # Customer selection
        st.subheader("Select Customer")
        
        try:
            customer_options = []
            for idx, row in st.session_state.data.iterrows():
                # Convert to string to avoid DataFrame boolean issues
                name = str(row.get('Name', 'Unknown')).strip()
                surname = str(row.get('Surname', 'Customer')).strip()
                age = str(row.get('age', 'N/A')).strip()
                
                # Clean up any 'nan' or 'None' values
                if name.lower() in ['nan', 'none']:
                    name = 'Unknown'
                if surname.lower() in ['nan', 'none']:
                    surname = 'Customer'
                if age.lower() in ['nan', 'none']:
                    age = 'N/A'
                    
                customer_options.append(f"{name} {surname} (Age: {age})")
            
            selected_option = st.selectbox("Choose a customer:", ["None"] + customer_options)
            
            if selected_option != "None":
                try:
                    st.session_state.selected_customer_idx = customer_options.index(selected_option)
                    selected_customer = st.session_state.data.iloc[st.session_state.selected_customer_idx]
                    name = str(selected_customer.get('Name', 'Unknown')).strip()
                    surname = str(selected_customer.get('Surname', 'Customer')).strip()
                    st.success(f"✅ Selected: {name} {surname}")
                except Exception as e:
                    st.error(f"❌ Error selecting customer: {str(e)}")
                    st.session_state.selected_customer_idx = None
            else:
                st.session_state.selected_customer_idx = None
                
        except Exception as e:
            st.error(f"❌ Error loading customer list: {str(e)}")
            st.session_state.selected_customer_idx = None
    
    with tab2:
        st.header("➕ Add New Customer")
        
        with st.form("add_customer"):
            # Personal Information Section
            st.subheader("👤 Personal Information (Optional)")
            st.markdown("*Leave blank to auto-generate with fake data*")
            
            personal_col1, personal_col2 = st.columns(2)
            with personal_col1:
                name = st.text_input("First Name", placeholder="Auto-generated if empty")
                surname = st.text_input("Last Name", placeholder="Auto-generated if empty")
                email = st.text_input("Email", placeholder="Auto-generated if empty")
            with personal_col2:
                phone = st.text_input("Phone", placeholder="Auto-generated if empty")
                address = st.text_area("Address", placeholder="Auto-generated if empty", height=80)
            
            st.markdown("---")
            
            # Customer Data Section
            st.subheader("📊 Customer Data")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Demographics & Finance**")
                age = st.number_input("Age", 18, 100, 30)
                housing = st.selectbox("Housing", ["own", "rent", "mortgage"])
                credit_score = st.number_input("Credit Score", 300, 850, 650)
                payment_type = st.selectbox("Payment Type", ["credit_card", "debit_card", "bank_transfer"])
                zodiac_sign = st.selectbox("Zodiac Sign", ["aries", "taurus", "gemini", "cancer", "leo", "virgo"])
                
                st.markdown("**Banking Activity**")
                deposits = st.number_input("Deposits", 0, 100, 5)
                purchases = st.number_input("Purchases", 0, 200, 25)
            
            with col2:
                st.markdown("**Digital & Engagement**")
                app_downloaded = st.selectbox("App Downloaded", [0, 1])
                rewards_earned = st.number_input("Rewards Earned", 0, 1000, 100)
                is_referred = st.selectbox("Is Referred", [0, 1])
            
            if st.form_submit_button("➕ Add Customer", type="primary"):
                # Use provided personal info or generate fake data
                customer_name = name.strip() if name.strip() else fake.first_name()
                customer_surname = surname.strip() if surname.strip() else fake.last_name()
                customer_email = email.strip() if email.strip() else fake.email()
                customer_phone = phone.strip() if phone.strip() else fake.phone_number()
                customer_address = address.strip() if address.strip() else fake.address().replace('\n', ', ')
                
                new_customer = {
                    "age": age, "housing": housing, "credit_score": credit_score,
                    "deposits": deposits, "withdrawal": 3, "purchases_partners": 10,
                    "purchases": purchases, "cc_taken": 0, "cc_recommended": 0,
                    "cc_disliked": 0, "cc_liked": 1, "cc_application_begin": 0,
                    "app_downloaded": app_downloaded, "web_user": 1, "app_web_user": 1,
                    "ios_user": 1, "android_user": 0, "registered_phones": 1,
                    "payment_type": payment_type, "waiting_4_loan": 0, "cancelled_loan": 0,
                    "received_loan": 0, "rejected_loan": 0, "zodiac_sign": zodiac_sign,
                    "left_for_two_month_plus": 0, "left_for_one_month": 0,
                    "rewards_earned": rewards_earned, "reward_rate": 0.02, "is_referred": is_referred,
                    "Name": customer_name, "Surname": customer_surname, 
                    "email": customer_email, "phone": customer_phone, 
                    "address": customer_address
                }
                
                st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_customer])], ignore_index=True)
                
                # Show success message with personal info status
                personal_info_status = "with provided" if name.strip() or surname.strip() else "with auto-generated"
                st.success(f"✅ Added: {customer_name} {customer_surname} ({personal_info_status} personal info)")
    
    with tab3:
        st.header("🤖 Churn Prediction")
        
        if st.session_state.selected_customer_idx is not None:
            try:
                customer = st.session_state.data.iloc[st.session_state.selected_customer_idx]
            except (IndexError, KeyError) as e:
                st.error(f"❌ Error accessing customer data: {str(e)}")
                st.session_state.selected_customer_idx = None
                return
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("👤 Selected Customer")
                # Convert all values to strings to avoid DataFrame boolean issues
                name = str(customer.get('Name', 'Unknown')).strip()
                surname = str(customer.get('Surname', 'Customer')).strip()
                age = str(customer.get('age', 'N/A')).strip()
                credit_score = customer.get('credit_score', 0)
                housing = str(customer.get('housing', 'N/A')).strip().title()
                
                st.write(f"**Name:** {name} {surname}")
                st.write(f"**Age:** {age}")
                try:
                    st.write(f"**Credit Score:** {float(credit_score):.0f}")
                except (ValueError, TypeError):
                    st.write(f"**Credit Score:** {credit_score}")
                st.write(f"**Housing:** {housing}")
                
                # Customer chart
                fig = create_customer_chart(customer)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("🔮 Prediction")
                
                if st.button("🚀 Predict Churn", type="primary"):
                    with st.spinner("Making prediction..."):
                        result, error = predict_churn(customer.to_dict())
                        
                        if result:
                            st.session_state.prediction_result = result
                            
                            prob = result['churn_probability']
                            risk = result['risk_level']
                            prediction = result['churn_prediction']
                            
                            # Color coding
                            if risk == "High":
                                color = "🔴"
                            elif risk == "Medium":
                                color = "🟡"
                            else:
                                color = "🟢"
                            
                            st.markdown(f"""
                            ### {color} Prediction Results
                            **Churn Probability:** {prob:.2%}
                            **Risk Level:** {risk}
                            **Prediction:** {'Will Churn' if prediction else 'Will Stay'}
                            """)
                            
                            st.progress(prob)
                        else:
                            st.error(f"❌ {error}")
        else:
            st.info("👆 Please select a customer from the Customer Data tab first.")
    
    with tab4:
        st.header("💡 AI-Powered Insights")
        
        if (st.session_state.selected_customer_idx is not None and 
            st.session_state.prediction_result is not None):
            
            try:
                customer = st.session_state.data.iloc[st.session_state.selected_customer_idx]
            except (IndexError, KeyError) as e:
                st.error(f"❌ Error accessing customer data: {str(e)}")
                st.session_state.selected_customer_idx = None
                return
            
            # Convert to strings to avoid DataFrame boolean issues
            name = str(customer.get('Name', 'Unknown')).strip()
            surname = str(customer.get('Surname', 'Customer')).strip()
            st.subheader(f"🎯 Insights for {name} {surname}")
            
            if st.button("🧠 Generate AI Insights", type="primary"):
                with st.spinner("Generating insights..."):
                    insights, error = get_llm_insights(customer.to_dict(), st.session_state.prediction_result)
                    
                    if insights:
                        st.session_state.llm_insights = insights
                        st.markdown("### 📋 Retention Strategy")
                        st.markdown(insights)
                        
                        # Risk gauge
                        prob = st.session_state.prediction_result['churn_probability']
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=prob * 100,
                            title={'text': "Churn Risk %"},
                            gauge={
                                'axis': {'range': [None, 100]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 30], 'color': "lightgreen"},
                                    {'range': [30, 70], 'color': "yellow"},
                                    {'range': [70, 100], 'color': "red"}
                                ]
                            }
                        ))
                        fig.update_layout(height=300)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error(f"❌ {error}")
            
            if st.session_state.llm_insights:
                st.markdown("### 📝 Previous Insights")
                st.markdown(st.session_state.llm_insights)
        else:
            st.info("👆 Please select a customer and run prediction first.")
    
    # Footer
    st.markdown("---")
    st.markdown("🏦 **Fintech Churn Prediction Dashboard** | Built with Streamlit")

if __name__ == "__main__":
    main()