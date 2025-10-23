#!/usr/bin/env python3
"""
Demo script for Email Marketing Campaign functionality
Shows how to use the email marketing features with sample data
"""

import pandas as pd
import numpy as np
from faker import Faker
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from streamlit_ui import (
        generate_email_campaign_content,
        create_bulk_email_campaign,
        export_email_campaign_data,
        load_sample_data
    )
    print("✅ Email marketing functions imported successfully")
except ImportError as e:
    print(f"❌ Failed to import functions: {e}")
    sys.exit(1)

def demo_single_customer_campaign():
    """Demonstrate email campaign generation for a single customer"""
    print("\n🎯 DEMO: Single Customer Email Campaign")
    print("=" * 50)
    
    # Create a sample high-risk customer
    customer = {
        'Name': 'María',
        'Surname': 'González',
        'email': 'maria.gonzalez@email.com',
        'age': 34,
        'credit_score': 580,
        'housing': 'r',  # rented
        'app_downloaded': 0,  # hasn't downloaded app
        'cc_taken': 0,  # no credit card
        'purchases': 3,  # low activity
        'deposits': 1,  # very low deposits
        'rewards_earned': 25,  # minimal rewards
        'risk_level_XGB': 'High',
        'churn_probability_XGB': 0.82
    }
    
    print(f"Customer: {customer['Name']} {customer['Surname']}")
    print(f"Risk Level: {customer['risk_level_XGB']} ({customer['churn_probability_XGB']:.1%})")
    print(f"Credit Score: {customer['credit_score']}")
    print(f"Activity Level: {customer['purchases']} purchases, {customer['deposits']} deposits")
    
    # Generate retention campaign
    campaign = generate_email_campaign_content(
        customer,
        campaign_type='retention',
        personalization_level='high'
    )
    
    print(f"\n📧 Generated Campaign:")
    print(f"Segment: {campaign['customer_segment']}")
    print(f"Subject Line: {campaign['subject_lines'][0]}")
    print(f"Expected Open Rate: {campaign['campaign_metrics']['expected_open_rate']}")
    print(f"Urgency Level: {campaign['campaign_metrics']['urgency_level']}")
    
    return campaign

def demo_bulk_campaign():
    """Demonstrate bulk email campaign creation"""
    print("\n🚀 DEMO: Bulk Email Campaign")
    print("=" * 50)
    
    # Load sample data
    sample_data = load_sample_data()
    
    # Add prediction data for demonstration
    np.random.seed(42)
    sample_data['risk_level_XGB'] = np.random.choice(
        ['High', 'Medium', 'Low'], 
        len(sample_data), 
        p=[0.2, 0.5, 0.3]  # 20% high risk, 50% medium, 30% low
    )
    sample_data['churn_probability_XGB'] = np.where(
        sample_data['risk_level_XGB'] == 'High', 
        np.random.uniform(0.6, 0.9, len(sample_data)),
        np.where(
            sample_data['risk_level_XGB'] == 'Medium',
            np.random.uniform(0.3, 0.6, len(sample_data)),
            np.random.uniform(0.1, 0.3, len(sample_data))
        )
    )
    
    # Take first 20 customers for demo
    demo_customers = sample_data.head(20)
    
    print(f"Creating campaign for {len(demo_customers)} customers")
    print(f"Risk distribution:")
    print(demo_customers['risk_level_XGB'].value_counts().to_string())
    
    # Create bulk campaign
    campaign_settings = {
        'campaign_type': 'retention',
        'personalization_level': 'high'
    }
    
    campaign_df = create_bulk_email_campaign(demo_customers, campaign_settings)
    
    print(f"\n📊 Campaign Results:")
    print(f"Total emails generated: {len(campaign_df)}")
    print(f"Segments created: {campaign_df['customer_segment'].nunique()}")
    
    # Show sample emails by risk level
    for risk_level in ['High', 'Medium', 'Low']:
        risk_customers = campaign_df[campaign_df['risk_level'] == risk_level]
        if not risk_customers.empty:
            sample = risk_customers.iloc[0]
            print(f"\n{risk_level} Risk Sample:")
            print(f"  Customer: {sample['name']} {sample['surname']}")
            print(f"  Subject: {sample['subject_line']}")
            print(f"  Expected Open Rate: {sample['expected_open_rate']}")
    
    return campaign_df

def demo_export_options(campaign_df):
    """Demonstrate export functionality"""
    print("\n📥 DEMO: Export Options")
    print("=" * 50)
    
    # CSV Export
    csv_data = export_email_campaign_data(campaign_df, "csv")
    print(f"CSV Export: {len(csv_data)} characters")
    print("First 200 characters:")
    print(csv_data[:200] + "...")
    
    # Summary Export
    summary_data = export_email_campaign_data(campaign_df, "summary")
    print(f"\nSummary Export:")
    print(summary_data[:500] + "...")
    
    # HTML Preview (first few lines)
    html_data = export_email_campaign_data(campaign_df, "html_preview")
    print(f"\nHTML Preview: {len(html_data)} characters generated")
    
    return {
        'csv': csv_data,
        'summary': summary_data,
        'html': html_data
    }

def main():
    """Run the email marketing demo"""
    print("🎉 Email Marketing Campaign Demo")
    print("This demo shows how to create personalized email campaigns")
    print("based on customer churn risk analysis.")
    
    # Demo 1: Single customer campaign
    single_campaign = demo_single_customer_campaign()
    
    # Demo 2: Bulk campaign
    bulk_campaign = demo_bulk_campaign()
    
    # Demo 3: Export options
    exports = demo_export_options(bulk_campaign)
    
    print("\n" + "=" * 50)
    print("🎯 Demo Summary")
    print("=" * 50)
    print("✅ Single customer campaign generation")
    print("✅ Bulk campaign creation")
    print("✅ Multiple export formats")
    print("✅ Risk-based segmentation")
    print("✅ Personalized content")
    
    print(f"\n📊 Campaign Statistics:")
    print(f"- Total customers processed: {len(bulk_campaign)}")
    print(f"- Risk levels: {bulk_campaign['risk_level'].nunique()}")
    print(f"- Customer segments: {bulk_campaign['customer_segment'].nunique()}")
    print(f"- Export formats: {len(exports)}")
    
    print("\n🚀 Next Steps:")
    print("1. Load your customer data in the Streamlit app")
    print("2. Apply filters to target specific segments")
    print("3. Run batch analysis for churn predictions")
    print("4. Generate personalized email campaigns")
    print("5. Export and implement in your email platform")
    
    print("\n📧 Ready to create targeted retention campaigns!")

if __name__ == "__main__":
    main()