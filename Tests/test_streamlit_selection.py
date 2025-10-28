#!/usr/bin/env python3
"""
Simplified Streamlit app to test customer selection across tabs
"""

import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

# Page configuration
st.set_page_config(
    page_title="Customer Selection Test",
    page_icon="🧪",
    layout="wide"
)

# Initialize Faker
fake = Faker()

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()
if 'selected_customer' not in st.session_state:
    st.session_state.selected_customer = None

def create_sample_data():
    """Create sample customer data"""
    np.random.seed(42)
    n_samples = 20
    
    data = {
        "Name": [fake.first_name() for _ in range(n_samples)],
        "Surname": [fake.last_name() for _ in range(n_samples)],
        "age": np.random.randint(18, 80, n_samples),
        "credit_score": np.random.normal(650, 100, n_samples).clip(300, 850),
        "housing": np.random.choice(["own", "rent", "mortgage"], n_samples),
        "deposits": np.random.poisson(5, n_samples),
        "purchases": np.random.poisson(25, n_samples),
        "app_downloaded": np.random.binomial(1, 0.7, n_samples),
        "email": [fake.email() for _ in range(n_samples)]
    }
    
    return pd.DataFrame(data)

def main():
    st.title("🧪 Customer Selection Test")
    
    # Sidebar
    st.sidebar.title("Controls")
    
    if st.sidebar.button("Load Sample Data"):
        st.session_state.data = create_sample_data()
        st.sidebar.success("Data loaded!")
    
    # Show selected customer in sidebar
    if st.session_state.selected_customer is not None:
        customer = st.session_state.selected_customer
        name = customer.get('Name', 'Unknown')
        surname = customer.get('Surname', 'Customer')
        st.sidebar.success(f"🎯 Selected: {name} {surname}")
        
        if st.sidebar.button("Clear Selection"):
            st.session_state.selected_customer = None
            st.rerun()
    
    # Main content
    if st.session_state.data.empty:
        st.info("Please load sample data from the sidebar")
        return
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📊 Customer Data", "🔍 Customer Details", "📋 Summary"])
    
    with tab1:
        st.header("Customer Data")
        
        # Configure grid
        gb = GridOptionsBuilder.from_dataframe(st.session_state.data)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_selection('single', use_checkbox=True)
        gridOptions = gb.build()
        
        # Display grid
        grid_response = AgGrid(
            st.session_state.data,
            gridOptions=gridOptions,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            theme='streamlit',
            height=400
        )
        
        # Handle selection
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
            
            st.session_state.selected_customer = clean_customer
            
            name = clean_customer.get('Name', 'Unknown')
            surname = clean_customer.get('Surname', 'Customer')
            st.success(f"✅ Selected: {name} {surname}")
        else:
            if st.session_state.selected_customer is not None:
                st.info("ℹ️ No customer selected. Click on a row to select.")
    
    with tab2:
        st.header("Customer Details")
        
        if st.session_state.selected_customer is not None:
            customer = st.session_state.selected_customer
            
            st.subheader("👤 Selected Customer")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Name:** {customer.get('Name', 'N/A')} {customer.get('Surname', 'N/A')}")
                st.write(f"**Age:** {customer.get('age', 'N/A')}")
                st.write(f"**Credit Score:** {customer.get('credit_score', 'N/A'):.0f}")
                st.write(f"**Housing:** {customer.get('housing', 'N/A')}")
            
            with col2:
                st.write(f"**Email:** {customer.get('email', 'N/A')}")
                st.write(f"**Deposits:** {customer.get('deposits', 'N/A')}")
                st.write(f"**Purchases:** {customer.get('purchases', 'N/A')}")
                st.write(f"**App User:** {'Yes' if customer.get('app_downloaded') else 'No'}")
            
            st.json(customer)
        else:
            st.info("👆 Please select a customer from the Customer Data tab")
    
    with tab3:
        st.header("Summary")
        
        if st.session_state.selected_customer is not None:
            customer = st.session_state.selected_customer
            name = customer.get('Name', 'Unknown')
            surname = customer.get('Surname', 'Customer')
            
            st.success(f"🎯 Customer selected: {name} {surname}")
            
            # Show some metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Age", customer.get('age', 0))
            with col2:
                st.metric("Credit Score", f"{customer.get('credit_score', 0):.0f}")
            with col3:
                st.metric("Purchases", customer.get('purchases', 0))
            
            st.markdown("### Customer Profile")
            st.write(f"This customer is {customer.get('age', 'unknown')} years old with a credit score of {customer.get('credit_score', 0):.0f}.")
            st.write(f"They have made {customer.get('purchases', 0)} purchases and {'have' if customer.get('app_downloaded') else 'have not'} downloaded the app.")
        else:
            st.info("👆 Please select a customer to see summary")
    
    # Footer
    st.markdown("---")
    st.markdown("🧪 Customer Selection Test - Verifying cross-tab functionality")

if __name__ == "__main__":
    main()